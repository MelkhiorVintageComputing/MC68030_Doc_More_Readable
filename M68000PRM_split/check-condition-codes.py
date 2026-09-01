#!/usr/bin/env python3
"""Cross-check the condition-code CSVs against the manual, four ways.

make-condition-codes.py reads the "Condition Codes:" block of each instruction
description out of the layout-preserving text extraction. That is one reading
of one place, so on its own it proves nothing. This checks it four ways, none
of which reuses the generator's code:

  A  Table 3-18, Integer Unit Condition Code Computations, states the same
     facts for 30 grouped rows in a different notation. Agreement between two
     differently-worded statements in different parts of the manual is real
     corroboration.
  B  The same pages extracted again with the layout preserver turned off.
     pdftotext then serialises the table into runs of bit letters and runs of
     values rather than two aligned rows - a different enough problem that a
     mistake in one parse will not repeat in the other.
  C  The glyph against the sentence printed for it. Every em dash must read
     "Not affected.", every 0 "Always cleared.", and so on; no asterisk cell
     may read any of those.
  D  pdftotext -bbox, measuring every explanation line, to prove that the two
     sentences with flattened superscripts are the only two.

Neither A nor B can prove a value right - both could be read wrong the same
way - but between them they would have to fail in the same direction twice,
in two notations, to let an error through.

Usage:  python3 check-condition-codes.py

Exits non-zero only on an unexplained mismatch. The manual's own errors are
listed in KNOWN_SOURCE_DEFECTS and reported rather than failed, so that a
transcription slip is still caught while the source's bookkeeping is not
relitigated on every run.
"""
import collections
import csv
import os
import re
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Section 7's three condition-code tables are CPU32-only and out of scope, but
# the parts are read whole, so they are dropped after reconstruction.
CPU32_TABLES = 3

PARTS = ['07-section-04-integer-instructions.pdf',
         '09-section-06-supervisor-instructions.pdf',
         '10-section-07-cpu32-instructions.pdf']

BITS = 'XNZVC'
ASTERISKS = {'∗', '*'}
CANONICAL = {'—': 'Not affected.', '0': 'Always cleared.',
             '1': 'Always set.', 'U': 'Undefined.'}
CONDITIONAL = ('if', 'unless', 'when', 'according', 'otherwise', 'value of',
               'same as', 'set to')

# Where the manual disagrees with itself. Each is written up in
# CONDITION-CODES.md; reported here, never failed on.
KNOWN_SOURCE_DEFECTS = {
    ('CLR', 'N'): "Table 3-18 groups CLR with thirteen instructions whose result is not "
                  "constant and gives the group N = '*'; CLR's own page prints 0, which "
                  "is right because the result of a clear is always zero",
    ('CLR', 'Z'): "the same grouping; CLR's own page prints 1",
    ('ASR', 'V'): "ASL and ASR share one description and one table, so ASR gets ASL's "
                  "conditional V; Table 3-18 gives them separate rows and is right that "
                  "an arithmetic right shift never changes the most significant bit",
}

# Row labels in Table 3-18 that name no instruction description.
# The only explanation lines in Sections 4, 6 and 7 that the manual sets with a
# superscript, and that the text layer therefore flattens. Both are CPU32-only
# and outside the document's table, but the extraction repairs them regardless.
# one line, printed twice - identically - in TBLS, TBLSN and TBLU, TBLUN
RAISED_EXPECTED = {('V — Set if the integer portion of', '23')}
RAISED_OCCURRENCES = 2

KNOWN_UNMATCHED = {
    'DUVU': "Table 3-18 spells the DIVU row 'DIVS, DUVU'",
}


def nolayout(name):
    return subprocess.run(['pdftotext', os.path.join(HERE, name), '-'],
                          capture_output=True, text=True, check=True).stdout


def rows():
    with open(os.path.join(HERE, 'condition-codes.csv')) as f:
        return list(csv.DictReader(f))


def notes():
    with open(os.path.join(HERE, 'condition-code-notes.csv')) as f:
        return {int(r['note']): r for r in csv.DictReader(f)}


def table_3_18():
    with open(os.path.join(HERE,
                           'table-3-18-condition-code-computations.csv')) as f:
        return list(csv.DictReader(f))


# --------------------------------------------------------- direction A ----
def check_table_3_18(cc, t318):
    """Compare Table 3-18 cell by cell with the instruction pages.

    3-18's '*' means set by the standard definition and '?' means see the
    Special Definition column; both are the instruction page's '*', which
    means see the explanation. The other three symbols map onto themselves.
    """
    index = collections.defaultdict(list)
    for r in cc:
        for name in r['mnemonic'].split(', '):
            index[name].append(r)

    seen, ok, defects, bad, unmatched = set(), 0, [], [], []
    for t in t318:
        if t['qualifier']:
            continue                      # a shift-count case, handled below
        for name in t['operations'].split(', '):
            if name not in index:
                unmatched.append(name)
                continue
            for r in index[name]:
                seen.add((r['mnemonic'], r['processors']))
                for bit in BITS:
                    theirs, ours = t[bit.lower()], r[bit.lower()]
                    want = '*' if theirs in ('*', '?') else theirs
                    if want == ours:
                        ok += 1
                    elif (name, bit) in KNOWN_SOURCE_DEFECTS:
                        defects.append((name, bit, theirs, ours))
                    else:
                        bad.append((name, bit, theirs, ours))

    names = sorted({n for t in t318 for n in t['operations'].split(', ')})
    print('Table 3-18: %d rows, %d mnemonics, %d matched to a description, %d unmatched'
          % (len(t318), len(names), len(names) - len(unmatched), len(unmatched)))
    print('Table 3-18: %d cells corroborate the instruction pages, %d known defects, '
          '%d unexplained' % (ok, len(defects), len(bad)))
    for name, bit, theirs, ours in defects:
        print('   known defect  %-8s %s   3-18 %r  page %r   %s'
              % (name, bit, theirs, ours, KNOWN_SOURCE_DEFECTS[(name, bit)]))
    for name, bit, theirs, ours in bad:
        print('   UNEXPLAINED   %-8s %s   3-18 %r  page %r' % (name, bit, theirs, ours))
    for name in unmatched:
        why = KNOWN_UNMATCHED.get(name, 'NOT EXPLAINED')
        print('   unmatched     %-8s %s' % (name, why))
        if name not in KNOWN_UNMATCHED:
            bad.append((name, '', '', ''))

    qualified = [t for t in t318 if t['qualifier']]
    print('Table 3-18: %d shift-count rows corroborate the sentences rather than the glyphs'
          % len(qualified))
    print('Table 3-18: covers %d of the %d descriptions carrying a Condition Codes block'
          % (len(seen), sum(1 for r in cc if r['form'] != 'absent')))
    return bad


# --------------------------------------------------------- direction B ----
def reconstruct(text):
    """Recover the five values of every table from the unaligned extraction.

    Without -layout the header and the value row interleave, and they do it
    three different ways depending on the page. What survives in every case
    is that the letters and the values alternate in runs, so the token stream
    is split into maximal runs and paired off: run 1 with run 2, run 3 with
    run 4. The letters of a pair must spell part of X N Z V C, and its two
    runs must be the same length.
    """
    out = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if not line.strip().endswith('Condition Codes:'):
            continue
        tokens = []
        for l in lines[i + 1:i + 40]:
            t = l.strip()
            if not t:
                continue
            if re.match(r'^[XNZVC]\s*—', t) or len(tokens) >= 10:
                break
            if t in BITS or t in ASTERISKS or t in CANONICAL:
                tokens.append('*' if t in ASTERISKS else t)
            else:
                break
        if len(tokens) != 10:
            continue
        runs, cur = [], [tokens[0]]
        for t in tokens[1:]:
            same = (t in BITS) == (cur[0] in BITS)
            if same:
                cur.append(t)
            else:
                runs.append(cur)
                cur = [t]
        runs.append(cur)
        letters, values = [], []
        for a, b in zip(runs[::2], runs[1::2]):
            if len(a) != len(b) or not all(x in BITS for x in a):
                letters = []
                break
            letters += a
            values += b
        if ''.join(letters) == BITS:
            out.append(values)
    return out


def check_second_reading(cc):
    """Re-read the same glyphs by a different code path and compare."""
    found = []
    for name in PARTS:
        found += reconstruct(nolayout(name))
    tables = [r for r in cc if r['form'] == 'table']
    # The reconstruction sees every table in these three parts; the CSV keeps
    # only those in scope, so the CPU32 tables of part 10 are dropped from the
    # comparison. Both sequences are in printed order, so they pair by index.
    found = found[:len(found) - CPU32_TABLES]
    print('second reading: %d tables reconstructed from the unaligned extraction'
          % len(found))
    bad = []
    if len(found) == len(tables):
        for r, values in zip(tables, found):
            ours = [r[b.lower()] for b in BITS]
            if ours != values:
                bad.append((r['mnemonic'], ours, values))
    else:
        bad.append(('count', len(tables), len(found)))
    print('second reading: %d of %d tables agree glyph for glyph, %d disagree'
          % (len(tables) - len(bad), len(tables), len(bad)))
    for b in bad:
        print('   UNEXPLAINED   %s  csv %s  second reading %s' % b)
    return bad


# --------------------------------------------------------- direction C ----
def check_glyph_against_sentence(cc, note_rows):
    """The glyph and the sentence printed for it must agree."""
    unconditional = conditional = 0
    bad = []
    for r in cc:
        for bit in BITS:
            glyph, note = r[bit.lower()], r['%s_note' % bit.lower()]
            if glyph in CANONICAL and not note:
                unconditional += 1
            elif glyph == '*' and note:
                sentence = note_rows[int(note)]['sentence']
                if sentence in CANONICAL.values():
                    bad.append((r['mnemonic'], bit,
                                'an asterisk cell reading a constant sentence'))
                elif not any(w in sentence.lower() for w in CONDITIONAL):
                    bad.append((r['mnemonic'], bit,
                                'an asterisk cell whose sentence states no condition'))
                else:
                    conditional += 1
    print('glyph/sentence: %d unconditional cells, %d asterisk cells reading a condition, '
          '%d wrong' % (unconditional, conditional, len(bad)))

    glyphs = collections.defaultdict(set)
    for r in cc:
        for bit in BITS:
            note = r['%s_note' % bit.lower()]
            if note:
                glyphs[int(note)].add(r[bit.lower()])
    ambiguous = [n for n, g in glyphs.items() if len(g) > 1]
    print('glyph/sentence: %d notes, each used with exactly one glyph, %d ambiguous'
          % (len(note_rows), len(ambiguous)))
    for m, bit, why in bad:
        print('   UNEXPLAINED   %-12s %s  %s' % (m, bit, why))
    return bad + [('note %d' % n, '', 'used with two different glyphs') for n in ambiguous]


# --------------------------------------------------------- direction D ----
WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" '
                  r'yMax="([\d.]+)">(.*?)</word>')


def check_raised_glyphs(note_rows):
    """Find every explanation line set with a sub-size digit.

    The text layer flattens superscripts, so "2 to the 23rd" comes out as
    "223". Rather than assume that happens only where it has been noticed,
    every explanation line in the three parts is measured: words are grouped
    into lines by their top edge, and any word more than a point shorter than
    its line's median is flagged.
    """
    flagged = []
    scanned = 0
    for name in PARTS:
        xml = subprocess.run(['pdftotext', '-bbox', os.path.join(HERE, name), '-'],
                             capture_output=True, text=True, check=True).stdout
        for page in xml.split('<page ')[1:]:
            words = [(float(a), float(b), float(c), float(d), e)
                     for a, b, c, d, e in WORD.findall(page)]
            # Cluster into lines by the bottom edge, not the top: a raised
            # digit's top is 5.3 pt above its line's, which is more than the
            # gap to the line above, but its bottom is only 3.1 pt off. Any
            # rule keyed on the top puts the superscript in a line of its own,
            # which is the one place it must not go.
            words.sort(key=lambda w: w[1])
            groups, cur = [], []
            for w in words:
                if cur and w[1] - cur[0][1] > 5.0:
                    groups.append(cur)
                    cur = []
                cur.append(w)
            if cur:
                groups.append(cur)
            for group in groups:
                group.sort(key=lambda w: w[0])
                text = ' '.join(w[4] for w in group)
                if not re.match(r'^[XNZVC]\s*[—–]', text):
                    continue
                scanned += 1
                median = statistics.median(w[3] - w[1] for w in group)
                for w in group:
                    if median - (w[3] - w[1]) > 1.0:
                        flagged.append((text, w[4]))
    # The two sentences the generator repairs, named here rather than imported,
    # so this really is an independent statement of what should be found.
    got = {(t[:33].strip(), w) for t, w in flagged}
    print('raised glyphs: %d explanation lines measured, %d carry a sub-size digit, '
          '%d distinct' % (scanned, len(flagged), len(got)))
    bad = []
    if got != RAISED_EXPECTED or len(flagged) != RAISED_OCCURRENCES:
        bad.append(('raised glyphs', sorted(got), sorted(RAISED_EXPECTED)))
        print('   UNEXPLAINED   flagged set is not the expected one')
        for t in sorted(got - RAISED_EXPECTED):
            print('     unexpected: %s | %s' % t)
        for t in sorted(RAISED_EXPECTED - got):
            print('     missing:    %s | %s' % t)
    return bad


# ----------------------------------------------------------- integrity ----
def check_integrity(cc, note_rows):
    cells = sum(1 for r in cc for b in BITS if r[b.lower()] or r['%s_note' % b.lower()])
    used = {int(r['%s_note' % b.lower()]) for r in cc for b in BITS
            if r['%s_note' % b.lower()]}
    dangling = sorted(used - set(note_rows))
    unused = sorted(set(note_rows) - used)
    keys = collections.Counter((r['mnemonic'], r['processors']) for r in cc)
    duplicate = [k for k, n in keys.items() if n > 1]
    print('csv integrity: %d rows, %d cells, %d notes, %d dangling, %d unused, %d duplicate keys'
          % (len(cc), cells, len(note_rows), len(dangling), len(unused), len(duplicate)))
    bad = []
    for n in dangling:
        bad.append(('note %d' % n, '', 'referenced but not defined'))
    for n in unused:
        bad.append(('note %d' % n, '', 'defined but referenced by no cell'))
    for k in duplicate:
        bad.append((str(k), '', 'duplicate row key'))
    for b in bad:
        print('   UNEXPLAINED   %s %s' % (b[0], b[2]))
    return bad


def main():
    cc, note_rows, t318 = rows(), notes(), table_3_18()
    bad = check_table_3_18(cc, t318)
    bad += check_second_reading(cc)
    bad += check_glyph_against_sentence(cc, note_rows)
    bad += check_raised_glyphs(note_rows)
    bad += check_integrity(cc, note_rows)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
