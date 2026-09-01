#!/usr/bin/env python3
"""Write the condition-code CSVs and CONDITION-CODES.md.

Every instruction description in the M68000 Family Programmer's Reference
Manual carries a "Condition Codes:" block saying what the instruction does to
X, N, Z, V and C. The block is either a five-cell table over the manual's own
alphabet - "*" see the explanation, "U" undefined, "0" always cleared, "1"
always set, em dash not affected - followed by one sentence per bit, or a
single sentence standing in for the whole table.

This reads all 139 descriptions in Sections 4, 6 and 7, drops the 13 that
belong to the MC68851 and MC68881/MC68882 coprocessors and the 4 that are
CPU32-only, and writes the remaining 122 out as one row each. The "*" cells
become footnote numbers: identical explanations share a number, so 193
asterisk cells collapse to 60 notes, and the seven notes that stand for a
whole block bring the total to 67.

Table 3-18 of Section 3 states the same facts for 30 grouped rows in a
different notation. It is written out as well, because check-condition-codes.py
uses it as the independent corroboration of everything here.

Everything is read from the split parts in this directory, not from
../M68000PRM.pdf, which is deliberately untracked - so this runs on a fresh
clone.
"""
import collections
import csv
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# The three parts holding instruction descriptions, with each part's first
# page in M68000PRM.pdf so a row can cite the source page as well as the
# split file. Section 5 is the floating-point coprocessor and is out of scope.
PARTS = [('4', '07-section-04-integer-instructions.pdf', 105),
         ('6', '09-section-06-supervisor-instructions.pdf', 455),
         ('7', '10-section-07-cpu32-instructions.pdf', 541)]
SUMMARY = '06-section-03-instruction-set-summary.pdf'

RUNNING_HEADS = ('Integer Instructions', 'Supervisor (Privileged) Instructions',
                 'CPU32 Instructions')

BITS = 'XNZVC'

# The two asterisks are one symbol. The manual sets 151 of them in Symbol
# (U+2217 ASTERISK OPERATOR) and 48 in Helvetica (U+002A), with no
# difference in meaning; Table 3-1 defines the symbol once, as "General Case".
GLYPHS = {'∗': '*', '*': '*', '—': '—',
          '0': '0', '1': '1', 'U': 'U'}

# What the four unconditional glyphs say in words. The manual is completely
# consistent about this: all 126 such cells read one of these four sentences,
# and no "*" cell ever reads one of them.
CANONICAL = {'—': 'Not affected.', '0': 'Always cleared.',
             '1': 'Always set.', 'U': 'Undefined.'}

# A head line naming one of these continues the line above rather than naming
# a sibling instruction: ANDI + "to CCR" is one instruction, where CAS + CAS2
# is two.
MNEMONIC_SUFFIXES = ('to CCR', 'to SR', 'from CCR', 'from SR', 'USP')

# Coprocessor instructions, excluded by request. The test is the processor
# annotation printed under the title: a description goes only when every part
# it names is the MC68851 PMMU or the MC68881/MC68882 FPU. That keeps PLOAD
# "(MC68030 only, MC68851)" and the MC68030/MC68040 forms of PFLUSH, PMOVE
# and PTEST, which are those processors' own on-chip MMU instructions, and it
# keeps the cpXXX instructions, which are MC68020/MC68030 CPU instructions for
# driving a coprocessor rather than coprocessor instructions themselves.
COPROCESSOR = re.compile(r'^\((?:MC68851|M68851)\)$'
                         r'|^\(MC68881, MC68882, MC68040 only\)$')

# CPU32-only instructions, excluded by request to match INSTRUCTIONS-BY-CPU.md.
# They are exactly Section 7; the CPU32 named in a Section 4 or 6 annotation is
# one processor among several and does not exclude anything.
CPU32_SECTION = '7'

# The text layer flattens superscripts. pdftotext -bbox shows the "23" of
# TBLS and TBLU set in an 8.9 pt box against 11.1 pt for the digits beside
# it, i.e. 2 to the 23rd. check-condition-codes.py proves this list is
# complete by measuring every explanation line in the manual.
SUPERSCRIPT_FIXUPS = {
    '– (223) ≤ Result ≤ (223) – 1':
        '−(2^23) ≤ Result ≤ (2^23) − 1',
}

# The one place the source's own line breaking has to be repaired: the NOTE
# under MULS and MULU breaks "high-order" across lines and sets "low- order"
# with a stray space.
NOTE_FIXUPS = [('high- order', 'high-order'), ('low- order', 'low-order')]

CC_COLS = ['mnemonic', 'title', 'processors', 'section', 'printed_page',
           'pdf_page', 'form', 'x', 'n', 'z', 'v', 'c',
           'x_note', 'n_note', 'z_note', 'v_note', 'c_note', 'qualifier']
NOTE_COLS = ['note', 'glyph', 'sentence', 'uses', 'cells']
T318_COLS = ['row', 'operations', 'qualifier', 'x', 'n', 'z', 'v', 'c',
             'special_definition']

CC_ANCHOR = re.compile(r'(?:^|\.\s)Condition Codes:\s*$')
HEADER_ROW = re.compile(r'^\s+X\s+N\s+Z\s+V\s+C\s*$')
EXPLANATION = re.compile(r'^(\s*)([XNZVC])\s*—\s*(\S.*)$')
HEAD_TITLED = re.compile(r'^\s*(\S+(?:\s\S+)*?)\s{2,}(\S.*?\S)\s{2,}\1\s*$')
HEAD_BARE = re.compile(r'^\s*(\S+(?:\s\S+)*?)\s{2,}\1\s*$')
HEAD_COLLAPSED = re.compile(r'^\s*(\S+)\s+(\S.*?\S)\s+\1\s*$')
FOLIO = re.compile(r'(?:^|\s)(\d+-\d+)(?:\s|$)')


def pages(name):
    """Every page of one split part, as a list of lines."""
    out = subprocess.run(['pdftotext', '-layout', os.path.join(HERE, name), '-'],
                         capture_output=True, text=True, check=True).stdout
    chunks = out.split('\f')
    if chunks and not chunks[-1].strip():
        chunks.pop()
    return [c.split('\n') for c in chunks]


def parse_head(page):
    """(mnemonic, title, processors) from a description's first page.

    The head is MNEM<spaces>Title<spaces>MNEM, but the title may run onto a
    second line, the mnemonic may be two lines ("ANDI" / "to CCR"), and a
    wide title collapses the separator to single spaces, so three patterns
    are tried in turn. The processor annotation is parenthesised and may
    itself wrap, so it is accumulated until the parentheses balance.
    """
    mnemonics, title, processors = [], [], ''
    i, started = 0, False
    while i < len(page):
        line = page[i]
        if line.startswith('Operation:'):
            break
        text = line.strip()
        if not text or text in RUNNING_HEADS:
            i += 1
            continue
        if text.startswith('('):
            processors = text
            while processors.count('(') > processors.count(')'):
                i += 1
                processors += ' ' + page[i].strip()
            break
        m = (HEAD_TITLED.match(line) or HEAD_BARE.match(line)
             or HEAD_COLLAPSED.match(line))
        if m:
            mnemonics.append(m.group(1))
            if m.lastindex > 1:
                title.append(m.group(2))
            started = True
        elif started:
            title.append(text)
        i += 1
    key = mnemonics[0]
    for extra in mnemonics[1:]:
        key += (' ' if extra in MNEMONIC_SUFFIXES else ', ') + extra
    return key, ' '.join(title), processors


def folio(page):
    """The printed page number, off the running footer."""
    for line in page:
        if 'M68000 FAMILY PROGRAMMER' in line:
            m = FOLIO.search(line)
            if m:
                return m.group(1)
    return ''


def join_wrapped(lines, k, indent, text):
    """Absorb continuation lines until the sentence ends in a period.

    Sixteen explanations wrap. The continuation carries no bit letter, so it
    is recognised by being indented past the letter it continues; a fragment
    left ending in a hyphen is a split word and rejoins with no space.
    Bounded at two continuations so a missing period cannot run away.
    """
    joins = 0
    while not text.endswith('.') and joins < 2:
        k += 1
        cont = lines[k]
        if not cont.strip() or len(cont) - len(cont.lstrip()) <= len(indent):
            break
        text = (text[:-1] + cont.strip() if text.endswith('-')
                else text + ' ' + cont.strip())
        joins += 1
    return k, text, joins


def parse_block(lines):
    """(form, glyphs, sentences, joins, end) for one description.

    form is 'table' when the manual prints the five-cell table, 'prose' when
    it prints one sentence instead, and 'absent' when there is no Condition
    Codes block at all. end is the line after the block, so the qualifier
    scan can start there rather than guessing.
    """
    anchors = [i for i, l in enumerate(lines) if CC_ANCHOR.search(l)]
    if not anchors:
        return 'absent', None, None, 0, 0
    assert len(anchors) == 1, anchors
    i = anchors[0] + 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    if not HEADER_ROW.match(lines[i]):
        body = []
        while i < len(lines) and lines[i].strip():
            body.append(lines[i].strip())
            i += 1
        return 'prose', None, [' '.join(body)], 0, i

    values = lines[i + 1].split()
    assert len(values) == 5, values
    glyphs = [GLYPHS[v] for v in values]

    sentences, k, joins = [], i + 2, 0
    while k < len(lines) and len(sentences) < 5:
        m = EXPLANATION.match(lines[k])
        if m:
            indent, bit, text = m.group(1), m.group(2), m.group(3).rstrip()
            assert bit == BITS[len(sentences)], (bit, len(sentences))
            k, text, n = join_wrapped(lines, k, indent, text)
            joins += n
            sentences.append(SUPERSCRIPT_FIXUPS.get(text, text))
        k += 1
    assert len(sentences) == 5, sentences
    return 'table', glyphs, sentences, joins, k


def parse_qualifier(lines, start):
    """The NOTE block or trailing sentence printed after the table, if any.

    Nine descriptions add something after the five explanations. Eight are a
    centred NOTE and one - ADDQ - is a bare sentence. The scan runs from the
    end of the block to Instruction Format:, which for a table falling at the
    foot of a page is overleaf, so the page furniture skipped here includes
    the repeated instruction head and its processor annotation.
    """
    out = []
    for line in lines[start:]:
        text = line.strip()
        if text.startswith('Instruction Format:'):
            break
        if (not text or text == 'NOTE' or text.startswith('*.')
                or text in RUNNING_HEADS or 'MOTOROLA' in text
                or 'M68000 FAMILY' in text or re.fullmatch(r'\d+-\d+', text)
                or re.fullmatch(r'\(.*\)', text)
                or HEAD_TITLED.match(line) or HEAD_BARE.match(line)
                or HEAD_COLLAPSED.match(line)):
            continue
        out.append(text)
    text = ' '.join(out)
    for old, new in NOTE_FIXUPS:
        text = text.replace(old, new)
    return text


def read_descriptions():
    """All 139 descriptions of Sections 4, 6 and 7, in printed order."""
    out = []
    for section, name, first_page in PARTS:
        book = pages(name)
        starts = [i for i, p in enumerate(book)
                  if any(l.startswith('Operation:') for l in p)]
        for n, i in enumerate(starts):
            end = starts[n + 1] if n + 1 < len(starts) else len(book)
            flat = [l for p in book[i:end] for l in p]
            mnemonic, title, processors = parse_head(book[i])
            form, glyphs, sentences, joins, end = parse_block(flat)
            out.append({
                'section': section, 'pdf_page': first_page + i,
                'printed_page': folio(book[i]), 'mnemonic': mnemonic,
                'title': title, 'processors': processors, 'form': form,
                'glyphs': glyphs, 'sentences': sentences, 'joins': joins,
                'qualifier': parse_qualifier(flat, end) if form == 'table' else '',
            })
        assert len(starts) == {'4': 97, '6': 38, '7': 4}[section], starts
    return out


# ------------------------------------------------- Table 3-18, section 3 ----
T318_ROW = re.compile(r'^\s(\S.*?)\s{2,}([*?—0U1])\s+([*?—0U1])'
                      r'\s+([*?—0U1])\s+([*?—0U1])'
                      r'\s+([*?—0U1])(\s*)(.*)$')
T318_SKIP = re.compile(r'^\s*(MOTOROLA|M68000 FAMILY|Instruction Set Summary'
                       r'|Table 3-18|Operations\s+X|\f)|^\s*\d+-\d+\s')
T318_QUALIFIED = re.compile(r'^(.*?)\s*\((r = 0)\)$')


def read_table_3_18():
    """Table 3-18, Integer Unit Condition Code Computations.

    The same facts as the instruction pages, for 30 grouped rows, in a
    different notation: "*" set by the standard definition, "?" see the
    Special Definition column. Mnemonic lists and formulas both wrap, and a
    single continuation line can carry one of each, so the two are split at
    the column where the Special Definition text starts - taken from the data
    rather than from the header, which is centred over its column.
    """
    out = subprocess.run(['pdftotext', '-layout', os.path.join(HERE, SUMMARY), '-'],
                         capture_output=True, text=True, check=True).stdout
    lines = out.split('\n')
    start = next(i for i, l in enumerate(lines)
                 if 'Table 3-18. Integer Unit Condition Code' in l)
    stop = next(i for i, l in enumerate(lines)
                if 'Table 3-19. Conditional Tests' in l)
    seg = lines[start:stop]
    seg = seg[:next(i for i, l in enumerate(seg)
                    if l.strip().startswith('? = Other'))]

    column = min(m.start(7) for m in (T318_ROW.match(l) for l in seg)
                 if m and m.group(8).strip())

    rows = []
    for line in seg:
        if T318_SKIP.match(line):
            continue
        m = T318_ROW.match(line)
        if m:
            rows.append([m.group(1).strip()] + [m.group(i) for i in range(2, 7)]
                        + [m.group(8).strip()])
        elif rows and line.strip():
            left, right = line[:column].strip(), line[column:].strip()
            if left:
                rows[-1][0] += ' ' + left
            if right:
                sep = '; ' if re.match(r'^[XNZVC] =', right) else ' '
                rows[-1][6] += (sep if rows[-1][6] else '') + right
    assert len(rows) == 30, len(rows)
    return rows


# ------------------------------------------------------ note assignment ----
def assign_notes(descriptions):
    """Number the explanations, in document order, X through C.

    A number is given only where the cell needs one: an asterisk cell, a
    prose block that says something conditional, or a description with no
    Condition Codes block at all. The em dash, 0, 1 and U print themselves,
    so their sentences never become notes. Identical sentences share a
    number by construction.
    """
    order, notes, uses = {}, [], collections.defaultdict(list)

    def note(sentence):
        if sentence not in order:
            order[sentence] = len(notes) + 1
            notes.append(sentence)
        return order[sentence]

    for d in descriptions:
        cells = []
        if d['form'] == 'table':
            for bit, glyph, sentence in zip(BITS, d['glyphs'], d['sentences']):
                n = note(sentence) if glyph == '*' else ''
                cells.append((glyph, n, sentence))
        elif d['form'] == 'prose':
            body = d['sentences'][0]
            if body == CANONICAL['—']:
                cells = [('—', '', body)] * 5
            else:
                cells = [('*', note(body), body)] * 5
        else:
            body = ('The manual prints no Condition Codes section for this '
                    'description.')
            cells = [('', note(body), body)] * 5
        d['cells'] = cells
        for bit, (glyph, n, _) in zip(BITS, cells):
            if n:
                uses[n].append('%s:%s' % (d['mnemonic'], bit))
    return notes, uses


# ------------------------------------------------------------- rendering ----
def cell(glyph, note):
    """A table cell: a bare glyph, or a linked superscript note number.

    The distinction matters. CLR's Z is the glyph 1 - the manual's own value,
    meaning always set - and note 1 is a different thing entirely.
    """
    if note:
        return '<sup>[%d](#n%d)</sup>' % (note, note)
    return glyph if glyph else '—​'


def write_csvs(descriptions, notes, uses, t318):
    rows = []
    for d in descriptions:
        row = {k: d[k] for k in ('mnemonic', 'title', 'processors', 'section',
                                 'printed_page', 'pdf_page', 'form', 'qualifier')}
        for bit, (glyph, note, _) in zip(BITS, d['cells']):
            row[bit.lower()] = glyph
            row['%s_note' % bit.lower()] = note
        rows.append(row)
    with open(os.path.join(HERE, 'condition-codes.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, CC_COLS)
        w.writeheader()
        w.writerows(rows)
    print('%-42s %d rows' % ('condition-codes.csv:', len(rows)))

    glyph_of = {}
    for d in descriptions:
        for glyph, note, _ in d['cells']:
            if note:
                glyph_of[note] = glyph
    with open(os.path.join(HERE, 'condition-code-notes.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(NOTE_COLS)
        for i, sentence in enumerate(notes, 1):
            w.writerow([i, glyph_of[i], sentence, len(uses[i]), ';'.join(uses[i])])
    print('%-42s %d notes' % ('condition-code-notes.csv:', len(notes)))

    with open(os.path.join(HERE, 'table-3-18-condition-code-computations.csv'),
              'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(T318_COLS)
        for n, r in enumerate(t318, 1):
            m = T318_QUALIFIED.match(r[0])
            ops, qual = (m.group(1), m.group(2)) if m else (r[0], '')
            w.writerow([n, ops, qual] + r[1:6] + [r[6]])
    print('%-42s %d rows' % ('table-3-18-….csv:', len(t318)))


# ------------------------------------------------- the document's own prose ----
# Everything below is authored rather than extracted: the extraction can find
# the disagreements, but not say which side is right. Each was checked against
# the page it cites.

HEADER = """# M68000 Family — Condition Codes by Instruction

Derived from `../M68000PRM.pdf` — Motorola *M68000 Family Programmer's Reference Manual*, 1992
(see [`README.md`](README.md) for the split of that manual into per-section PDFs).

This document lists, for every MC680xx instruction, what it does to the five condition-code bits
X, N, Z, V and C. It is the per-instruction fact that the manual states only inside each
individual instruction description, 122 of them, and never gathers in one place.

**Coprocessor instructions are excluded.** That drops all 47 floating-point descriptions of
Section 5 — which have no `X N Z V C` table at all, but a `Floating-Point Status Register:` block
of a different shape — and 13 descriptions in Section 6 whose processor annotation names only the
MC68851 PMMU or the MC68881/MC68882 FPU. **CPU32-only instructions are excluded** as well
(`BGND`, `LPSTOP`, `TBLS`/`TBLSN`, `TBLU`/`TBLUN`), matching
[`INSTRUCTIONS-BY-CPU.md`](INSTRUCTIONS-BY-CPU.md).

Two kinds of description are deliberately kept. The `cpXXX` instructions (`cpBcc`, `cpDBcc`,
`cpGEN`, `cpRESTORE`, `cpSAVE`, `cpScc`, `cpTRAPcc`) are MC68020/MC68030 *CPU* instructions for
driving a coprocessor, not coprocessor instructions, and the manual prints them in Sections 4 and
6 accordingly. So are the MC68030 and MC68040 forms of `PFLUSH`, `PLOAD`, `PMOVE` and `PTEST`,
which drive those processors' own on-chip MMU.

**See also:** [`INSTRUCTIONS-BY-CPU.md`](INSTRUCTIONS-BY-CPU.md) — which processor supports which
instruction.
"""

READING = """## Reading the table

The alphabet is the manual's own. Table 3-1, *Notational Conventions*, defines it on printed page
3-3, under the heading *Register Codes*:

| Symbol | Table 3-1's definition | Here |
|---|---|---|
| `*` | General Case | replaced by a note number — see below |
| `U` | Undefined, Reserved for Motorola Use. | `U` |
| `—` | Not Affected or Applicable. | `—` |
| `0` | *(not defined in Table 3-1)* | `0`, always cleared |
| `1` | *(not defined in Table 3-1)* | `1`, always set |

The manual's `*` means "read the sentence printed under the table". Those sentences are the
substance of the whole thing, so each one becomes a numbered note below and the `*` is replaced by
its number, set as a superscript link: <sup>[4](#n4)</sup>. Identical sentences share a number —
the commonest is used 28 times — so the 193 asterisk cells reduce to 60 notes.

**A superscript number is a note reference; a plain digit is the manual's own value.** The two can
only be confused in one place: `CLR`'s Z cell prints `1`, meaning *always set*, and it is the only
`1` in the manual. It is set as a plain digit, and note 1 is set as a superscript.

`—`, `0`, `1` and `U` need no note: every one of the 117 table cells carrying them reads exactly
*Not affected.*, *Always cleared.*, *Always set.* or *Undefined.* respectively, with no
exceptions, and no `*` cell ever reads one of those four sentences.

Where the manual prints one sentence in place of the whole table, the `Form` is *prose*. *Not
affected.* is the exact prose equivalent of five em dashes and is shown as such; the six
conditional bodies get one note, repeated across all five bits, because that is precisely what the
manual says — the sentence covers the register, not a bit.
"""

CROSSCHECK = """## Cross-check against Table 3-18

Table 3-18, *Integer Unit Condition Code Computations* (printed pages 3-18 and 3-19), states the
same facts a second time, in a different notation and with the instructions grouped: `*` there
means *set by the standard definition*, `?` means *see the Special Definition column*, and the
column then gives the boolean formula. Both map onto the instruction pages' `*`; `—`, `0` and `U`
map onto themselves.

That makes it a genuine independent statement rather than a restatement, and
[`check-condition-codes.py`](check-condition-codes.py) compares the two cell by cell.
It is carried here as
[`table-3-18-condition-code-computations.csv`](table-3-18-condition-code-computations.csv).

The seven shift-count-qualified rows — `ASL (r = 0)`, `ROXL (r = 0)` and so on — are finer-grained
than the instruction pages, which fold the zero-count case into the sentence rather than giving it
a row. They corroborate the *sentences*: Table 3-18 gives `ASL (r = 0)` an X of `—` and a C of
`0`, which is exactly what `ASL`'s own notes say happens when the shift count is zero.

**The Special Definition column's formulas are transcribed but should not be relied on.** They
come out of the text layer as, for instance, `V = Sm Λ Dm Λ Rm V Sm Λ Dm Λ Rm` — the same term
twice, which cannot be what is meant. The two differ by complement bars that the extraction drops,
and there is no way to recover an overbar from a text layer. The value columns are unaffected;
only the formulas are.
"""

DISCREPANCIES = [
 ('Table 3-18 gives `CLR` a computed N and Z where its own page gives constants', 'substantive',
  """Table 3-18 groups `CLR` into the fourteen-instruction row
`AND, ANDI, EOR, EORI, MOVEQ, MOVE, OR, ORI, CLR, EXT, EXTB, NOT, TAS, TST` and gives the whole
group N = `*` and Z = `*` — set from the result in the standard way. `CLR`'s own description
(printed page 4-73) gives N = `0` and Z = `1`.

Both describe the same behaviour, since the result of a clear is always zero, so the standard
computation always yields N = 0 and Z = 1. But only the instruction page says so as a constant,
which is the more useful statement and the one a reader wants. Read as an artefact of grouping
`CLR` with thirteen instructions whose result is not constant. This document follows the
instruction page.""" ),

 ('Table 3-18 splits `ASL` from `ASR` on V, where the shared description cannot', 'substantive',
  """`ASL` and `ASR` are documented together, in one description with one table, which gives V = `*`
and the sentence *"Set if the most significant bit is changed at any time during the shift
operation; cleared otherwise."*

Table 3-18 gives them separate rows and different values: `ASL` has V = `?`, with an overflow
formula in the Special Definition column, while `ASR, LSR, ROXR` has V = `0`.

Table 3-18 is right, and the shared table cannot express it. An arithmetic shift right replicates
the sign bit, so the most significant bit never changes and V is always cleared — which is what
`LSR`, `ROR` and `ROXR` all print as a flat `0` on their own pages. `ASR` gets a conditional V
only because it shares a table with `ASL`, where the condition is real. This is the one cell where
the two sources genuinely disagree.""" ),

 ('`PTEST (MC68EC040)` has no condition-code section at all', 'substantive',
  """Alone among the 139 instruction descriptions in Sections 4, 6 and 7, the MC68EC040 form of
`PTEST` (printed page 6-72) carries neither a `Condition Codes:` block nor any status-register
block in its place. Its four sibling `PTEST` descriptions all carry one: the MC68030, MC68EC030
and MC68040/MC68LC040 forms print `Condition Codes: / Not affected.`, and the MC68851 form prints
a `PMMU Status Register:` table.

There is no reason to think the MC68EC040 form behaves differently from the other three; the
statement is simply missing. Shown here with all five bits carrying a note saying so, rather than
guessed at.""" ),

 ('`PLOAD` never states its effect on the condition codes', 'substantive',
  """`PLOAD (MC68030 only, MC68851)` (printed page 6-43) documents only the PMMU status register.
Its neighbour `PFLUSH (MC68030 only)`, an instruction of the same kind on the same processor, does
print `Condition Codes: / Not affected.`

So for the MC68030 form of `PLOAD` — an instruction of the CPU, not of a coprocessor — the effect
on the CCR is never stated anywhere in the manual.""" ),

 ('Table 3-18 spells a row label `DIVS, DUVU`', 'typo',
  """The row giving the divide instructions their condition codes is labelled `DIVS, DUVU`.
It is `DIVU`. The row's values match both `DIVS, DIVSL` and `DIVU, DIVUL` on their own pages.""" ),

 ('Table 3-18 loses `LSL (r = 0)` and lists `LSR` twice', 'typo',
  """The continued half of Table 3-18 opens with a row `LSR (r = 0)`. Four rows later comes
`ASR, LSR (r = 0)`, so `LSR`'s zero-count case is given twice, with identical values.

The first of the two should be `LSL (r = 0)`: the preceding half ends with `LSL, ROXL`, every
other shift and rotate in the table has its `(r = 0)` companion, and without it `LSL` is the only
one that does not. As printed, `LSL`'s zero-count case is undocumented in Table 3-18 — though
`LSL`'s own page covers it, in the sentence *"Set according to the last bit shifted out of the
operand; cleared for a shift count of zero."*""" ),

 ('Table 3-18\'s `CHK2`/`CMP2` carry formula has a stray letter and an unbalanced bracket', 'typo',
  """The Special Definition for `CHK2, CMP2` reads

> C = (LB ≤ UB) Λ (IR < LB) V (R > UB)) V (UB < LB) Λ (R > UB) Λ (R < LB)

`(IR < LB)` is `(R < LB)` — `R` is defined in the table's own legend as *Register Tested*, and
`IR` is not defined anywhere. `(R > UB))` has one closing bracket too many.""" ),

 ('Table 3-18\'s `ASL` overflow formula mixes two spellings in one expression', 'typo',
  """The Special Definition for `ASL` reads

> V = Dm Λ Dm–1 V…V Dm– r V Dm Λ (DM –1 V …+ Dm – r)

`DM` is `Dm`, and `V …+` uses `V` and `+` for the same OR within a single expression — the rest of
the table uses `V` throughout.""" ),

 ('`DIVS` sets one explanation line without spaces around the dash', 'typo',
  """`DIVS, DIVSL`'s X line is set `X—Not affected.` where its own N, Z, V and C lines four lines
below, `DIVU, DIVUL` on the facing pages, and all 58 other Section 4 tables are set
`X — Not affected.` with spaces.

It is the only such line in Section 4. Section 6 sets all fifteen of its explanation lines the
compressed way, so the manual is inconsistent between sections as well as within `DIVS`.""" ),

 ('`DIVS` and `DIVU` state one rule in opposite clause order', 'imprecision',
  """`DIVS, DIVSL`'s V reads *"Set if division overflow occurs; undefined if divide by zero
occurs; cleared otherwise."* and `DIVU, DIVUL`'s reads *"Set if division overflow occurs; cleared
otherwise; undefined if divide by zero occurs."*

Same rule, clauses swapped, so two notes exist below where one would do.""" ),

 ('The carry, borrow and overflow sentences split without a pattern', 'imprecision',
  """The same event is *generated* in some descriptions and *occurs* in others, with no
distinction that the manual explains:

| Sentence | Instructions |
|---|---|
| Set if an overflow **is generated**; cleared otherwise. | `ADD`, `ADDI`, `CAS, CAS2`, `CMPA`, `CMPM`, `SUB` |
| Set if an overflow **occurs**; cleared otherwise. | `ADDQ`, `ADDX`, `CMP`, `CMPI`, `NEG`, `NEGX`, `SUBI`, `SUBQ`, `SUBX` |
| Set if a carry **is generated**; cleared otherwise. | `ADD`, `ADDI`, `ADDX` |
| Set if a carry **occurs**; cleared otherwise. | `ADDQ` |
| Set if a borrow **is generated**; cleared otherwise. | `CAS, CAS2`, `CMPA`, `CMPM`, `SUB` |
| Set if a borrow **occurs**; cleared otherwise. | `CMP`, `CMPI`, `NEGX`, `SUBI`, `SUBQ`, `SUBX` |

`ADD` and `ADDQ` differ on both bits; `ADDX` takes *is generated* for C and *occurs* for V, in the
same table.""" ),

 ('The X bit splits the same way, cleanly along add against subtract', 'imprecision',
  """*"Set the same as the carry bit."* is used by `ABCD`, `ADD`, `ADDI`, `ADDQ`, `ADDX`, `NBCD`,
`NEG` and `NEGX`; *"Set to the value of the carry bit."* by `SUB`, `SUBI`, `SUBQ` and `SUBX`.

Unlike the previous entry this one is at least consistent — every subtract uses the second form
and nothing else does — but the two sentences say the same thing.""" ),

 ('`MULS` and `MULU` give the only condition-code sentence with no verb', 'imprecision',
  """Both read *"Set if overflow; cleared otherwise."* for V. Every other overflow sentence in the
manual is *"Set if an overflow occurs"* or *"…is generated"*.""" ),

 ('`BFEXTU` says *source field* where its seven siblings say *field*', 'imprecision',
  """`BFEXTU`'s N reads *"Set if the most significant bit of the source field is set; cleared
otherwise."* `BFCHG`, `BFCLR`, `BFEXTS`, `BFFFO`, `BFINS`, `BFSET` and `BFTST` all read *"…of the
field…"*, `BFEXTS` — its signed twin, doing the same thing to the same operand — included.""" ),

 ('The three BCD carry sentences are all different', 'imprecision',
  """`ABCD` reads *"Set if a decimal carry was generated; cleared otherwise."* — the only past
tense in any condition-code sentence in the manual. `NBCD` reads *"Set if a decimal borrow occurs;
cleared otherwise."* `SBCD` reads *"Set if a borrow (decimal) is generated; cleared otherwise."*
Three instructions of one family, three constructions.""" ),

 ('The NOTE about presetting Z is printed in three versions', 'imprecision',
  """Eight instructions carry the same NOTE about setting Z before a multiple-precision operation,
in three wordings: *"Normally, the Z condition code bit … of an operation."* (`ABCD`, `ADDX`),
*"Normally the Z condition code bit … of an operation."* (`SBCD`, `SUBX`), and *"Normally the Z
condition code bit … of the operation."* (`NBCD`, `NEGX`). The comma and the article each vary
independently.""" ),

 ('Table 3-18 defines `?` and leaves the rest of its alphabet to Table 3-1', 'imprecision',
  """The legend under Table 3-18 defines `? = Other—See Special Definition` and then goes on to
the operand abbreviations. `*`, `—`, `U` and `0` — four of the five symbols in its own value
columns — are not defined there at all. They are defined in Table 3-1, fifteen printed pages
earlier, under the heading *Register Codes*, where `*` is given as *General Case*, which is not
the sense Table 3-18 uses it in.""" ),

 ('The three `… to CCR` instructions have three styles of title', 'imprecision',
  """`ANDI to CCR` is titled *CCR AND Immediate*, `EORI to CCR` is *Exclusive-OR Immediate to
Condition Code* (singular), and `ORI to CCR` is *Inclusive-OR Immediate to Condition Codes*
(plural). The three are the same instruction over three operations, and their `… to SR`
counterparts in Section 6 are titled uniformly.""" ),

]

NOT_DISCREPANCIES = """### Not discrepancies

Things that look wrong in a mechanical comparison and are not.

- **`BGND` prints a full table of five em dashes** where the 52 other instructions whose codes are untouched
  print the sentence *Not affected.* The two are the same statement in the manual's two available forms.
- **`MOVE from SR` is documented twice** — in Section 4 as `(MC68000, MC68008)` and in Section 6 as
  `(MC68EC000, MC68010, MC68020, MC68030, MC68040, CPU32)` — because it is unprivileged on the
  first two parts and privileged on the rest. Both say *Not affected.*, as do all three `PFLUSH`
  descriptions, both non-coprocessor `PMOVE`s and the three `PTEST`s that state anything.
- **`CHK`'s N cell is `*` while X, Z, V and C are `U`.** The sentence is a three-way one, *"Set if
  Dn < 0; cleared if Dn > effective address operand; undefined otherwise."* — so N is genuinely
  conditional and `*` is right. Table 3-18 independently prints `CHK` as `— * U U U`.
- **`TAS` says *"was zero"* and *"is currently set"*** where other instructions use the present
  tense, because `TAS` writes the operand it has just tested; the tense is carrying real meaning.
- **`SWAP` says *"the 32-bit result"*** rather than *"the result"* because `SWAP` is long-only.
- **`ANDI to CCR`, `EORI to CCR` and `ORI to CCR` use three different sentences** — *Cleared if bit
  n of immediate operand is zero*, *Changed if bit n … is one*, *Set if bit n … is one*. Each is
  correct for its own operation, and each is shared exactly with the corresponding `… to SR`
  instruction in Section 6.
- **`∗` and `*` are one symbol.** The manual sets 151 of its asterisks in Symbol (U+2217 ASTERISK
  OPERATOR) and 48 in Helvetica (U+002A). The split follows the font, never the meaning.
"""

METHOD = """## Method and caveats

Everything in the table and the notes was extracted mechanically by
[`make-condition-codes.py`](make-condition-codes.py) from the split PDFs in this directory, and
checked by [`check-condition-codes.py`](check-condition-codes.py) against three independent
readings. Nothing was transcribed by hand. Both scripts read the tracked split parts rather than
`../M68000PRM.pdf`, which is deliberately untracked, so they run on a fresh clone.

- Descriptions are delimited by their `Operation:` line — 139 of them across Sections 4, 6 and 7.
  The mnemonic, title and processor annotation come from the running head, which needs three
  patterns: the ordinary `MNEM  Title  MNEM`, the two-line form where the mnemonic itself wraps
  (`ANDI` / `to CCR`), and the form where a wide title squeezes the separators down to single
  spaces (`cpTRAPcc Trap on Coprocessor Condition cpTRAPcc`).
- The `Condition Codes:` anchor has to allow the label mid-line: in `MOVE`, alone among the 139, it
  is run on to the end of the preceding paragraph — `…or long. Condition Codes:`. Requiring the
  line to *end* at `Codes:` is what keeps the `Operation:` lines, the `RTR Return and Restore
  Condition Codes RTR` running head and the `ORI to CCR` title out.
- Values are read **by token order, never by column**: the value row is not always aligned under
  its header. Binding the table to the `X N Z V C` header row is also what keeps the `MMUSR:`,
  `MMU Status Register:` and `ACUSR:` tables out — they use the same `*` and `0` alphabet, but a
  different header.
- Sixteen explanation sentences wrap onto a second line. They are rejoined by reading on until the
  sentence ends in a full stop; a fragment left ending in a hyphen is a split word and rejoins with
  no space, which happens once — `DIVS`'s *"cleared oth-"* / *"erwise."*

**Superscripts are lost by the text layer.** The V sentence of `TBLS` and `TBLU` extracts as
`– (223) ≤ Result ≤ (223) – 1`, which is `−(2^23) ≤ Result ≤ (2^23) − 1`. Those two are CPU32-only
and so fall outside the table above, but the extraction repairs them anyway, and that they are the
only affected sentences is not assumed: `pdftotext -bbox` measures every explanation line in all
three sections and finds sub-size digits on exactly those two.

**Overbars are lost too**, which is why Table 3-18's Special Definition column is carried but not
relied on — see [Cross-check against Table 3-18](#cross-check-against-table-3-18) above.

One count worth reconciling. [`README.md`](README.md) describes Sections 4–7 as *"175 instruction
descriptions"*, counting the entries in its own reconstructed bookmark lists. Segmenting by
`Operation:` gives 186 across those four sections — the difference being the mnemonics documented
more than once, which the bookmark list names once and this count reaches separately.
"""


SOURCES = """## Sources and how this was checked

| # | Source | Where |
|---|---|---|
| 1 | The `Condition Codes:` block of each instruction description | Sections 4 and 6 — PDF pp. 105–302, 455–540 (Section 7, pp. 541–556, is read and checked but excluded) |
| 2 | Table 3-18, *Integer Unit Condition Code Computations* | Section 3 — printed pp. 3-18…3-19 |
| 3 | Table 3-1, *Notational Conventions*, which defines the alphabet | Section 3 — printed p. 3-3 |
| 4 | A second extraction of the same pages with the layout preserver turned off, plus `pdftotext -bbox` for raised glyphs | same pages as 1 |

Source 2 is what makes this more than one reading of one table: it states the same facts for 30
grouped rows in a different notation, so agreement between it and the instruction pages is real
corroboration. Source 4 is the same glyphs read by a different code path in poppler — without
`-layout` the table serialises into runs of bit letters and runs of values instead of two aligned
rows, which is enough of a different problem that a mistake in one parse will not repeat in the
other.

[`check-condition-codes.py`](check-condition-codes.py) runs all of it:

```
%s
```

The two disagreements it reports — Table 3-18's `CLR` row and its `ASR` V — are the first two
entries under [Documentation discrepancies](#documentation-discrepancies) below. Everything else
corroborates.
"""


def write_markdown(descriptions, notes, uses, check_output):
    seen = collections.Counter(d['mnemonic'] for d in descriptions)
    out = [HEADER, SOURCES % check_output, READING,
           '## Condition codes by instruction\n',
           '122 instructions, in the manual\'s own order: Section 4 alphabetically, then'
           '\nSection 6. `Form` is *table* where the manual prints the five cells, *prose* where'
           '\nit prints one sentence instead, and *absent* where it prints nothing at all.\n',
           '| Instruction | Description | Form | X | N | Z | V | C |',
           '|---|---|---|:-:|:-:|:-:|:-:|:-:|']
    for d in descriptions:
        title = d['title']
        if seen[d['mnemonic']] > 1:
            title += ' %s' % d['processors']
        cells = ' | '.join(cell(g, n) for g, n, _ in d['cells'])
        out.append('| `%s` | %s | %s | %s |'
                   % (d['mnemonic'], title, d['form'], cells))

    out.append('\n## Notes\n')
    out.append('The sentence the manual prints under the table for each `*` cell. Identical'
               '\nsentences share a number; `uses` is how many cells point here.\n')
    out.append('| # | Explanation | Uses |')
    out.append('|--:|---|--:|')
    for i, sentence in enumerate(notes, 1):
        out.append('| <a id="n%d"></a>%d | %s | %d |' % (i, i, sentence, len(uses[i])))

    quals = [d for d in descriptions if d['qualifier']]
    out.append('\n## Qualifications printed with the table\n')
    out.append('Nine descriptions print something further under the explanations — eight a centred'
               '\n`NOTE`, and `ADDQ` a bare sentence. They qualify the table above them, so they are'
               '\ncarried here verbatim.\n')
    out.append('| Instruction | Printed under the table |')
    out.append('|---|---|')
    for d in quals:
        out.append('| `%s` | %s |' % (d['mnemonic'], d['qualifier']))

    out.append('\n' + CROSSCHECK)
    out.append('## Documentation discrepancies\n')
    out.append('Eighteen places where the manual contradicts itself, misprints something, or says'
               '\none thing two ways. Each was checked against the page it cites. Nothing here is'
               '\ncorrected in the table or the CSVs — what the manual prints is what lands there.\n')
    for i, (title, kind, body) in enumerate(DISCREPANCIES, 1):
        out.append('### %d. %s — *%s*\n' % (i, title, kind))
        out.append(body + '\n')
    out.append(NOT_DISCREPANCIES)
    out.append(METHOD)
    out.append("""## Regenerating

```sh
python3 make-condition-codes.py    # rewrites the three CSVs and this document
python3 check-condition-codes.py   # re-reads the PDFs and checks them
```
""")
    text = '\n'.join(out)
    with open(os.path.join(HERE, 'CONDITION-CODES.md'), 'w') as f:
        f.write(text)
    print('%-42s %d instructions, %d notes'
          % ('CONDITION-CODES.md:', len(descriptions), len(notes)))


def main():
    descriptions = read_descriptions()
    assert len(descriptions) == 139, len(descriptions)
    kept = [d for d in descriptions
            if not COPROCESSOR.match(d['processors'])
            and d['section'] != CPU32_SECTION]
    assert len(kept) == 122, len(kept)

    census = collections.Counter(g for d in descriptions if d['form'] == 'table'
                                 for g in d['glyphs'])
    assert census == {'*': 199, '—': 58, '0': 54, 'U': 13, '1': 1}, census
    assert sum(d['joins'] for d in descriptions) == 16
    assert len([d for d in kept if d['qualifier']]) == 9

    notes, uses = assign_notes(kept)
    assert len(notes) == 67, len(notes)

    t318 = read_table_3_18()
    write_csvs(kept, notes, uses, t318)

    check = os.path.join(HERE, 'check-condition-codes.py')
    if os.path.exists(check):
        output = subprocess.run(['python3', check], capture_output=True,
                                text=True).stdout.rstrip()
    else:
        output = '(check-condition-codes.py has not been written yet)'
    write_markdown(kept, notes, uses, output)


if __name__ == '__main__':
    main()
