#!/usr/bin/env python3
"""Write INSTRUCTIONS-BY-CPU.md and instructions-by-cpu.csv.

Appendix A's Table A-1 is the manual's cross-reference of which processor
supports which instruction. It is a nine-column matrix spread over seven
pages, and it is awkward to read mechanically: the column widths shift from
page to page, footnote markers are set as superscripts that the text layer
drops onto whichever line it likes, and a mnemonic too wide for its column is
broken across two or three lines with the marks stranded on the line between.

So it is not read from the text layer at all. pdftotext -bbox gives every
word's bounding box; words are clustered into rows by their bottom edge, which
puts a raised footnote marker back on the row it belongs to, and assigned to
columns by their centre against the header row of their own page. All four row
layouts then come out the same way, with no special cases.

Table A-2 supplies the descriptions and Tables A-3 to A-13 the per-processor
instruction sets, which check-instructions-by-cpu.py uses as an independent
statement of the same facts.

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

APPENDIX = '12-appendix-a-processor-instruction-summary.pdf'

# Table A-1's columns, in printed order, with the name this document uses.
# CPU32 is read so that an instruction supported only by it can be recognised
# and dropped, but it gets no column of its own.
COLUMNS = [('68000', 'MC68000'), ('68008', 'MC68008'), ('68010', 'MC68010'),
           ('68020', 'MC68020'), ('68030', 'MC68030'), ('68040', 'MC68040'),
           ('68882', 'MC68881/2'), ('68851', 'MC68851')]
CPU32 = 'CPU32'
HEADINGS = [c for c, _ in COLUMNS] + [CPU32]

# Table A-1's own footnotes, printed under the last page of the table, in the
# words this document uses for them.
FOOTNOTES = {
    '1': 'privileged',
    '2': 'not on EC/LC040',
    '3': '68040: software (FPSP)',
    '4': 'not privileged on 68000/68008',
    '5': 'not on EC030',
}

# A head line beginning with one of these continues the mnemonic above rather
# than naming the next instruction: MOVE + "from SR" is one instruction.
CONTINUATIONS = ('to', 'from')

# Where this document departs from Table A-1. Each is written up under
# Documentation discrepancies, and nothing else is changed.
CORRECTIONS = {
    ('FLOGNP1', '68882'): 'X',
    ('PFLUSHA', '68040'): 'X',
}

# Table A-2 spells two mnemonics with a stray F. The description is A-2's,
# and it is the only place the description can come from.
DESCRIPTION_ALIASES = {'FSABS': 'FSFABS', 'FDABS': 'FDFABS'}

# Table A-1 fuses a footnote marker to this mnemonic. The marker is an
# asterisk, which that table never defines - see the discrepancies.
MNEMONIC_MARKERS = {'FSAVE*': 'FSAVE'}

COLS = ['mnemonic', 'description'] + [n for _, n in COLUMNS] + ['notes']

WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" '
                  r'yMax="([\d.]+)">(.*?)</word>')
LIST_ROW = re.compile(r'^\s{4,}(\S.*?\S|\S)\s{3,}(\S.*?)\s*$')

# Body text in these tables is set at about 8.3 pt and a superscript at about
# 6 pt, so anything this short is a footnote marker rather than a word.
SUPERSCRIPT = 7.0


def bbox_pages(name):
    xml = subprocess.run(['pdftotext', '-bbox', os.path.join(HERE, name), '-'],
                         capture_output=True, text=True, check=True).stdout
    return xml.split('<page ')[1:]


def lines_of(page):
    """The page's words, clustered into lines by their bottom edge.

    Clustering on the bottom edge rather than the top is what puts a raised
    footnote marker back on its own line: a superscript's top is further from
    its line's than the gap to the line above, but its bottom is not.
    """
    words = [(float(a), float(b), float(c), float(d), e)
             for a, b, c, d, e in WORD.findall(page)]
    words.sort(key=lambda w: w[1])
    out, cur = [], []
    for w in words:
        if cur and w[1] - cur[0][1] > 5.0:
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    for line in out:
        line.sort(key=lambda w: w[0])
    return out


def read_table_a1():
    """Table A-1, as one record per printed row.

    Each record is the mnemonic as printed, the footnote markers attached to
    it, and for every column whether it carries a mark and which footnotes
    hang off it.
    """
    rows = []
    for page in bbox_pages(APPENDIX)[:7]:
        lines = lines_of(page)
        header = next(l for l in lines if l and l[0][4] == 'Mnemonic')
        centre = {w[4]: (w[0] + w[2]) / 2 for w in header if w[4] in HEADINGS}
        assert len(centre) == len(HEADINGS), sorted(centre)
        edge = min(centre.values()) - 22
        for line in lines:
            if line[0][1] <= header[0][1] + 2:
                continue
            text = ' '.join(w[4] for w in line)
            if text.startswith('NOTES:') or 'MOTOROLA' in text or 'PROGRAMMER' in text:
                break
            names = [w for w in line if w[0] < edge]
            marks = [w for w in line if w[0] >= edge]
            words = [w for w in names if w[3] - w[1] > SUPERSCRIPT]
            markers = [w for w in names if w[3] - w[1] <= SUPERSCRIPT]
            if words and not (rows and (rows[-1]['mnemonic'].endswith(',')
                                        or words[0][4] in CONTINUATIONS)):
                rows.append({'mnemonic': '', 'footnotes': [], 'cells': {}})
            if words:
                text = ' '.join(w[4] for w in words)
                have = rows[-1]['mnemonic']
                rows[-1]['mnemonic'] = (have + text if have.endswith(',')
                                        else (have + ' ' + text if have else text))
            for w in markers:
                rows[-1]['footnotes'] += w[4].split(',')
            for w in marks:
                column = min(centre, key=lambda k: abs(centre[k] - (w[0] + w[2]) / 2))
                cell = rows[-1]['cells'].setdefault(column, {'mark': False,
                                                             'footnotes': []})
                if w[3] - w[1] <= SUPERSCRIPT:
                    cell['footnotes'] += w[4].split(',')
                else:
                    cell['mark'] = True
    for r in rows:
        r['mnemonic'] = MNEMONIC_MARKERS.get(r['mnemonic'], r['mnemonic'])
    return rows


def read_lists():
    """Tables A-2 to A-13: mnemonic to description, one dict per table.

    All of them are two plain columns, so the layout-preserving extraction is
    enough. Grouped entries are expanded, and the footnote markers Tables A-8
    and A-10 fuse to their mnemonics are stripped - but only where what is
    left is a mnemonic Table A-2 already knows, so that the genuine trailing
    digits of CMP2, MOVE16 and FLOG10 survive.
    """
    text = subprocess.run(['pdftotext', '-layout', os.path.join(HERE, APPENDIX), '-'],
                          capture_output=True, text=True, check=True).stdout
    lines = text.split('\n')
    tables, current = {}, None
    for line in lines:
        m = re.search(r'Table (A-\d+)\. ', line)
        if m:
            current = m.group(1)
            tables.setdefault(current, {})
            continue
        if re.match(r'^\s*(The |Table A-\d+ )', line):
            current = None
        if current is None:
            continue
        m = LIST_ROW.match(line)
        if not m or m.group(1).startswith('Mnemonic'):
            continue
        for one in re.split(r',\s*', m.group(1).strip()):
            if one:
                tables[current][one] = m.group(2).strip()
    known = set(tables.get('A-2', {}))
    for tag, entries in tables.items():
        for name in list(entries):
            bare = name.rstrip('0123456789*')
            if bare != name and bare in known and name not in known:
                entries[bare] = entries.pop(name)
    return tables


def build(rows, tables):
    """One row per instruction, with grouped mnemonics split apart."""
    descriptions = tables['A-2']
    out = []
    for r in rows:
        footnotes = list(r['footnotes'])
        for column, _ in COLUMNS:
            if column in r['cells']:
                footnotes += r['cells'][column]['footnotes']
        notes, seen = [], set()
        for f in footnotes:
            if f in FOOTNOTES and FOOTNOTES[f] not in seen:
                seen.add(FOOTNOTES[f])
                notes.append(FOOTNOTES[f])
        for name in re.split(r',\s*', r['mnemonic']):
            marks = {}
            for column, label in COLUMNS:
                cell = r['cells'].get(column)
                if (name, column) in CORRECTIONS:
                    marks[label] = CORRECTIONS[(name, column)]
                elif not cell:
                    marks[label] = ''
                elif '3' in cell['footnotes']:
                    marks[label] = 'S'
                elif cell['mark'] or cell['footnotes']:
                    marks[label] = 'X'
                else:
                    marks[label] = ''
            if not any(marks.values()):
                continue                      # supported by CPU32 alone
            key = DESCRIPTION_ALIASES.get(name, name)
            out.append({'mnemonic': name, 'description': descriptions[key],
                        'notes': '; '.join(notes), **marks})
    return out


# --------------------------------------------- the document's own prose ----
# Authored, not extracted: the extraction finds the disagreements, it cannot
# say which side is right. Each write-up cites the page it was checked against.

HEADER = """# M68000 Family — Instruction Support by Processor

Derived from `../M68000PRM.pdf` — Motorola *M68000 Family Programmer's Reference Manual*, 1992
(see [`README.md`](README.md) for the split of that manual into per-section PDFs).

This document lists, for every processor and coprocessor in the family, which instructions it
supports. Per your request, **CPU32 is excluded** — only the 68xxx processors and the two
coprocessors are covered. (The manual's own Table A-1 has a CPU32 column; the four CPU32-only
instructions BGND, LPSTOP, TBLS and TBLU are therefore omitted here.)
"""

SOURCES = """## Sources and how this was checked

The support data is taken from **Table A-1, "M68000 Family Instruction Set and Processor
Cross-Reference"** (PDF pp. 597–603 of the source; Appendix A, printed pp. A-1…A-7). Because a
single OCR-adjacent table is easy to mis-read, every entry was cross-checked against two
independent statements of the same fact elsewhere in the manual:

| # | Source | Where |
|---|--------|-------|
| 1 | Table A-1 cross-reference matrix | PDF pp. 597–603 |
| 2 | The per-processor instruction lists — Tables A-3 (MC68000/08), A-4 (MC68010), A-6 (MC68020), A-8 (MC68030), A-10 (MC68040), A-12 (MC68881/2), A-13 (MC68851) | PDF pp. 608–627 |
| 3 | The processor annotation printed in the header of each instruction description, e.g. `(M68000 Family)`, `(MC68020, MC68030, MC68040)`, `(MC6888X, M68040FPSP)` | Sections 4, 5 and 6 — PDF pp. 105–540 |

The corroboration is broad: the seven per-processor tables between them confirm 729 of Table A-1's
marks, and the instruction descriptions confirm 629 processor claims. Seven instructions are where
the three sources genuinely disagree — `BKPT`, `cpTRAPcc`, `DIVSL`, `DIVUL`, `EXTB`, `FLOGNP1` and
`PFLUSHA`. Those, with three misprints found along the way, are the ten entries under
[Documentation discrepancies](#documentation-discrepancies) below, and the only places where this
document departs from, or annotates, Table A-1.

[`check-instructions-by-cpu.py`](check-instructions-by-cpu.py) runs the comparison:

```
%s
```
"""

READING = """## Reading the tables

| Symbol | Meaning |
|---|---|
| `X` | Supported |
| `S` | Supported on the MC68040 **in software only**, via the M68040FPSP floating-point support package (Table A-1 footnote 3) |
| `X`⚠ | Supported, but **Table A-1 omits the mark** — added here on the evidence of the other two sources (see discrepancies 1 and 2) |
| *(blank)* | Not supported |

Footnote conditions from Table A-1 are carried into the Notes column: *privileged*, *not on
EC/LC040* (MC68EC040 and MC68LC040), *not on EC030* (MC68EC030), and *not privileged on
68000/68008*.

Throughout, `MC68881/2` means the MC68881 and MC68882 floating-point coprocessors (the manual
writes this `MC6888X`), and per Appendix A's own preamble, references to the MC68000, MC68020 and
MC68030 include the embedded MC68EC000, MC68EC020 and MC68EC030 unless a footnote says otherwise.
"""

COUNTS_NOTE = """The MC68040's total is much larger than the MC68030's chiefly because it absorbs the
floating-point instruction set: of its 176 instructions, 63 are the FPU set, and 29 of those are
provided by the software FPSP rather than in hardware.
"""

DISCREPANCIES = """## Documentation discrepancies

Ten places where the manual contradicts itself or is imprecise. Each was verified by reading the
relevant page directly; page numbers are **PDF pages of `M68000PRM.pdf`**, with the split file in
brackets.

### 1. Table A-1 omits MC68881/MC68882 support for `FLOGNP1` — *substantive*

Table A-1 (p. 600) gives the `FLOGNP1` row a `2,3` mark in the MC68040 column and **leaves the
68881/68882 column blank**. Every adjacent transcendental row (`FMOD`, `FMOVECR`, `FREM`, `FSCALE`,
`FSGLDIV`, …) has an `X` there. Both other sources say the coprocessors do support it:

- Table A-12, MC68881/MC68882 Instruction Set (p. 626), lists `FLOGNP1`.
- The Section 5 description of `FLOGNP1` (p. 369) is headed `(MC6888X, M68040FPSP)`.

Read as a dropped mark in Table A-1. Marked `X`⚠ for MC68881/2 in this document.

### 2. Table A-1 omits MC68040 support for `PFLUSHA` — *substantive*

Table A-1 (p. 602) marks `PFLUSHA` for the MC68030 (`X`, footnote 5) and the MC68851 only. But
Table A-10, MC68040 Instruction Set (p. 624), lists `PFLUSHA`; and the neighbouring `PFLUSH` row in
Table A-1 *does* carry an MC68040 mark. Marked `X`⚠ for MC68040 here.

### 3. `cpTRAPcc` is misspelled `cpTRACPcc` in Table A-6 — *typo*

Table A-6, MC68020 Instruction Set Summary (p. 614), reads `cpTRACPcc` — the `P` and `C` are
transposed. The instruction is spelled `cpTRAPcc` in Table A-1 (p. 598), in Table A-2 (p. 605), in
Table A-8 for the MC68030 (p. 618), and in its own description (p. 193).

### 4. `BKPT` — Section 4 claims MC68EC000, the tables do not

The Section 4 description of `BKPT` (p. 157) is headed
`(MC68EC000, MC68010, MC68020, MC68030, MC68040, CPU32)`. But Table A-1 leaves the 68000 column
blank for `BKPT`, and Table A-3, the MC68000/MC68008 instruction set (pp. 608–609), does not list
it — `BKPT` first appears in Table A-4, for the MC68010 (p. 610).

Appendix A states that references to the MC68000 include the MC68EC000, so the two cannot both be
right. This document follows the tables (no MC68000/MC68008 support), but the conflict is
unresolved in the manual and the MC68EC000 is a later part than the tables' vintage.

### 5. `DIVSL`, `DIVUL` and `EXTB` inherit an over-broad header — *imprecision*

`DIVS` and `DIVSL` share one description (pp. 196–199), as do `DIVU` and `DIVUL` (pp. 200–203) and
`EXT` and `EXTB` (p. 210). Every one of those pages is headed `(M68000 Family)`. But the long forms
`DIVSL`, `DIVUL` and `EXTB` are all MC68020-and-later, as Table A-1 and Tables A-3/A-4 state.

Only `EXT, EXTB` says so anywhere on the page, and it says it in the Assembler Syntax block rather
than in the header:

> `EXTB.L Dn` extend byte to long word (MC68020, MC68030 MC68040, CPU32)

`DIVS`/`DIVSL` and `DIVU`/`DIVUL` leave the restriction to the body prose. In all three cases the
header, read alone, claims MC68000 support the instruction does not have.

### 6. Malformed processor list on `EXTB` — *typo*

That Assembler Syntax annotation reads `(MC68020, MC68030 MC68040, CPU32)` — the comma between
`MC68030` and `MC68040` is missing. It is the only processor list in the manual that runs two part
numbers together.

### 7. Malformed header on `PTRAPcc` — *typo*

The Section 6 description of `PTRAPcc` (p. 532) is headed `(M68851)`. Every other PMMU instruction
uses the part number `(MC68851)`; `M68851` is not a Motorola part designation.

### 8. `FSABS`/`FDABS` appear as `FSFABS`/`FDFABS` in Table A-2 — *typo*

Table A-2 (p. 605) lists `FSFABS, FDFABS — Floating-Point Absolute Value (Single/Double
Precision)`. The instructions are `FSABS`/`FDABS`: that is the spelling in Table A-1 (p. 600), in
Table A-10 (MC68040), and in the Section 5 `FABS` description. The stray `F` is unique to
Table A-2.

### 9. `FSAVE` carries a footnote marker Table A-1 never defines — *typo*

Table A-1 (p. 603) prints the row as `FSAVE*`. The table's own NOTES list runs 1 to 5 and has no
asterisk in it, so the marker points at nothing.

It should be footnote 1, *Privileged (Supervisor) Instruction*. `FSAVE` is privileged — it is
documented in Section 6, Supervisor (Privileged) Instructions (p. 468) — and `FRESTORE`, its twin
on the line above, does carry footnote 1. The consequence is visible in the table below: `FSAVE`
is the one privileged instruction in the manual whose Notes cell does not say so, because the
marker it was given cannot be resolved.

### 10. Table A-2 gives `ADDA` the description `Address` — *typo*

Table A-2 (p. 604) lists `ADDA — Address`. It is *Add Address*, which is what Table A-3 (p. 608),
Table A-4, Table A-6, Table A-8 and Table A-10 all print, and what the Section 4 description
(p. 111) is titled. The verb has simply dropped out.

Descriptions in the table below come from Table A-2 verbatim, so this one reads `Address`.

### Not discrepancies

Three differences that look like conflicts but are correct as printed:

- **`MOVE from SR` is documented twice** — in Section 4 (p. 229, headed `(MC68000, MC68008)`) and
  again in Section 6 (p. 471, headed `(MC68EC000, MC68010, MC68020, MC68030, MC68040, CPU32)`).
  This is deliberate: the instruction is unprivileged on the MC68000/MC68008 and privileged from
  the MC68010 on, which is exactly what Table A-1's footnote 4 records, and why its 68000/68008
  cells carry a bare `4` rather than an `X`.
- **`PFLUSHA` and `PFLUSHS` have no description pages of their own** — they are documented inside
  the `PFLUSH` entry (p. 486), whose four headers between them cover the MC68030, MC68040/LC040,
  MC68EC040 and MC68851.
- **The single/double-precision forms** (`FSADD`/`FDADD`, `FSMUL`/`FDMUL`, …) likewise have no
  separate descriptions; each is covered by its parent entry in Section 5.
"""

MASTER_INTRO = """## Master cross-reference

One row per instruction; this is Table A-1 restated with the CPU32 column dropped, grouped
mnemonics split into their individual forms (so `ASL, ASR` becomes two rows), and the two
omissions noted above filled in and marked ⚠.
"""

METHOD = """## Method and caveats

Everything above was extracted mechanically from the PDF's text layer and then reconciled; nothing
was transcribed by hand, and no support claim rests on a single table.

- **Table A-1 is not read from the text layer at all.** Its column widths shift from page to page,
  its footnote markers are superscripts that the extraction drops onto whichever line it likes, and
  a mnemonic too wide for its column is broken across two or three lines with the marks stranded on
  the line between — so `PLOAD`, `PRESTORE` and `PSAVE` have their marks emitted *above* the
  mnemonic, and `ROXL,` / marks / `ROXR` spreads one row over three lines. Instead
  `pdftotext -bbox` gives every word's bounding box; words are clustered into lines by their
  **bottom** edge, and columns assigned by centre against the header row of that same page.
- Clustering on the bottom edge rather than the top is the whole trick. A superscript's top is
  5.3 pt above its line's, which is further than the gap to the line above, so any rule keyed on
  the top strands it; its bottom is only 3.1 pt off. Once the markers land on their own rows, all
  four row layouts come out identically and no special case is needed for any of them.
- A word is a footnote marker rather than a mnemonic or a mark if its box is under 7 pt tall: body
  text in these tables is set at about 8.3 pt and superscripts at about 6 pt. That is what keeps
  the genuine trailing digits of `CMP2`, `CHK2`, `MOVE16`, `FLOG2`, `FLOG10`, `FETOXM1` and
  `FLOGNP1` intact while stripping the fused markers from `MOVES`, `STOP` and `FSAVE`.
- Grouped entries were expanded to their individual mnemonics, so `ASL, ASR` and `CAS, CAS2`
  contribute one row each to the matrix.
- A cell can be marked in three ways. Most carry an `X`. Where a footnote applies the `X` may be
  dropped and the marker left standing alone — `FMOVECR`'s MC68040 cell is a bare `2,3` and
  `MOVE from SR`'s MC68000 and MC68008 cells are a bare `4` — and those still mean supported. A
  cell whose footnotes include 3 is marked `S` here rather than `X`.

Two caveats worth stating:

- **The MC68040 count includes the FPSP.** 29 of its 176 instructions are marked `S`: they are
  provided by the M68040FPSP software package, not by hardware. If you want hardware-only
  capability, exclude them. The MC68EC040 and MC68LC040 lack the FPU entirely — the *not on
  EC/LC040* note in the Notes column marks the affected instructions.
- **Embedded variants are folded in.** Following Appendix A's own preamble, the MC68000 column
  covers the MC68EC000, MC68020 the MC68EC020, and MC68030 the MC68EC030, except where a footnote
  says otherwise (*not on EC030* appears on the MMU instructions, which the MC68EC030 lacks).

The 10 discrepancies above are those where the three sources genuinely disagree. During extraction a
further set of apparent conflicts turned out to be artefacts of the text layer rather than errors
in the manual — descriptions wrapping onto the preceding line in Table A-10, and the `cpTRAPcc`
description page (p. 193) whose header collapses onto a single line, `cpTRAPcc Trap on Coprocessor
Condition cpTRAPcc`, unlike every other instruction page. Those were resolved by reading the pages
concerned and are not reported as documentation defects.
"""


# ------------------------------------------------------------- rendering ----
def counts_table(rows):
    out = ['## Instruction counts', '',
           '| Processor | Instructions | Of which software-only |',
           '|---|--:|--:|']
    for _, label in COLUMNS:
        total = sum(1 for r in rows if r[label])
        soft = sum(1 for r in rows if r[label] == 'S')
        out.append('| %s | %d | %s |' % (label, total, soft if soft else '—'))
    return '\n'.join(out)


def per_processor(rows):
    out = ['## Instructions by processor']
    for _, label in COLUMNS:
        supported = [r['mnemonic'] for r in rows if r[label]]
        out.append('')
        out.append('### %s — %d instructions' % (label, len(supported)))
        soft = [r['mnemonic'] for r in rows if r[label] == 'S']
        if soft:
            hard = [r['mnemonic'] for r in rows if r[label] == 'X']
            out += ['', 'Hardware (%d):' % len(hard), '',
                    '> ' + ', '.join('`%s`' % m for m in hard),
                    '', 'Software, via M68040FPSP (%d):' % len(soft), '',
                    '> ' + ', '.join('`%s`' % m for m in soft)]
        else:
            out += ['', '> ' + ', '.join('`%s`' % m for m in supported)]
    return '\n'.join(out)


def master(rows):
    head = ['Instruction', 'Description'] + [n for _, n in COLUMNS] + ['Notes']
    out = [MASTER_INTRO, '',
           '| ' + ' | '.join(head) + ' |',
           '|---|---|' + ':-:|' * len(COLUMNS) + '---|']
    for r in rows:
        cells = []
        for _, label in COLUMNS:
            mark = r[label]
            if (r['mnemonic'], label) in {(m, dict(COLUMNS)[c])
                                          for m, c in CORRECTIONS}:
                mark = '**%s**⚠' % mark
            cells.append(mark)
        out.append('| `%s` | %s | %s | %s |'
                   % (r['mnemonic'], r['description'], ' | '.join(cells), r['notes']))
    return '\n'.join(out)


def write_csv(rows):
    with open(os.path.join(HERE, 'instructions-by-cpu.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows(rows)
    print('%-38s %d instructions' % ('instructions-by-cpu.csv:', len(rows)))


def write_markdown(rows, check_output):
    text = '\n\n'.join([HEADER, SOURCES % check_output, READING, counts_table(rows),
                        COUNTS_NOTE, per_processor(rows), DISCREPANCIES,
                        master(rows), METHOD,
                        '## Regenerating\n\n```sh\n'
                        'python3 make-instructions-by-cpu.py    # rewrites the CSV and'
                        ' this document\npython3 check-instructions-by-cpu.py   # re-reads'
                        ' the PDFs and checks them\n```\n'])
    text = re.sub(r'\n{3,}', '\n\n', text)
    with open(os.path.join(HERE, 'INSTRUCTIONS-BY-CPU.md'), 'w') as f:
        f.write(text)
    print('%-38s %d instructions' % ('INSTRUCTIONS-BY-CPU.md:', len(rows)))


def main():
    a1 = read_table_a1()
    assert len(a1) == 187, len(a1)
    tables = read_lists()
    rows = build(a1, tables)
    assert len(rows) == 196, len(rows)
    write_csv(rows)
    check = os.path.join(HERE, 'check-instructions-by-cpu.py')
    if os.path.exists(check):
        output = subprocess.run(['python3', check], capture_output=True,
                                text=True).stdout.rstrip()
    else:
        output = '(check-instructions-by-cpu.py has not been written yet)'
    write_markdown(rows, output)


if __name__ == '__main__':
    main()
