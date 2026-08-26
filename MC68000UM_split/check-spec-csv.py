#!/usr/bin/env python3
"""Cross-check the CSVs against the PDF's own text layer.

The transcription in make-spec-csv.py was made by eye from 300 dpi page
renderings.  This checks it against a completely independent extraction of
the same pages - poppler's text layer - and reports anything it cannot
corroborate.

Positional comparison is hopeless: the text layer drops em dashes, merges
adjacent cells and slides columns, so "column 7" in one is not "column 7" in
the other.  What it does preserve is *order*, so each row's numbers are
looked for as a subsequence of the numbers on the page line (or short run of
lines) that carries that row.  A row passes when every number it claims turns
up, in the order it claims them.

Rows the text layer cannot corroborate are listed with the reason.  Each one
is expected: TEXT_LAYER_LOST records the cells poppler drops on the floor.
"""
import csv, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'MC68000UM.pdf')

GRADES = ['f8', 'f10', 'f12_5', 'f16_67', 'f16', 'f20']

# Cells poplers's extraction loses outright, so the row cannot be matched in
# full.  Each was re-read at 3x from the page rendering instead.
TEXT_LAYER_LOST = {
    ('read-write', '41'):
        'the 8 MHz maximum and its footnote marker run together as "5512", so '
        'the 55 is not there to be found',
    ('clock', ''):
        'the text layer shreds the 10.8 table into one column per line, so '
        'the Frequency of Operation row has no line left holding its numbers',
}

FIX = str.maketrans({'O': '0', 'o': '0', 'l': '1', 'I': '1', '|': '1',
                     'S': '5', 'B': '8'})


def nums(s):
    # the scan reads a leading minus as a middle dot: "-14" comes back as
    # "·14".  Only a dot that starts a number can be one.
    s = re.sub(r'(?<![0-9])[·~](?=\d)', '-', s)
    return re.findall(r'-?\d+\.?\d*', s.translate(FIX))


def subseq(need, hay):
    it = iter(hay)
    return all(any(h == n for h in it) for n in need)


def load_pages():
    out = subprocess.run(['pdftotext', '-layout', SRC, '-'],
                         capture_output=True, text=True).stdout.split('\f')
    return [p.split('\n') for p in out]


def check_ac(pages):
    rows = list(csv.DictReader(open(os.path.join(HERE,
                                                 'ac-electrical-specifications.csv'))))
    ok, lost, unexplained = 0, [], []
    for r in rows:
        want = [v for g in GRADES for v in (r['%s_min' % g], r['%s_max' % g]) if v]
        lines = pages[int(r['pdf_page']) - 1]
        hit = False
        for i in range(len(lines)):
            for w in (1, 2, 3):
                if subseq(want, nums(' '.join(lines[i:i + w]))):
                    hit = True
                    break
            if hit:
                break
        key = (r['table'], r['num'])
        if hit:
            ok += 1
        elif key in TEXT_LAYER_LOST:
            lost.append(key)
        else:
            unexplained.append((r['table'], r['num'], r['characteristic']))
    print('AC: %d of %d rows corroborated by the text layer, %d known losses, '
          '%d unexplained' % (ok, len(rows), len(lost), len(unexplained)))
    for u in unexplained:
        print('   UNEXPLAINED  %-26s %-5s %s' % u)
    for t, n in lost:
        print('   known loss   %-26s %-5s %s' % (t, n, TEXT_LAYER_LOST[(t, n)]))
    stale = sorted(set(TEXT_LAYER_LOST) - set(lost))
    for t, n in stale:
        print('   note: %s %s now matches; its TEXT_LAYER_LOST entry is stale'
              % (t, n))
    return unexplained


def check_dc(pages, name, cols):
    rows = list(csv.DictReader(open(os.path.join(HERE, name))))
    ok, miss = 0, []
    for r in rows:
        want = [v for c in cols for v in [r[c]] if v and re.fullmatch(r'-?\d+\.?\d*', v)]
        if not want:
            ok += 1
            continue
        lines = pages[int(r['pdf_page']) - 1]
        hit = any(subseq(want, nums(' '.join(lines[i:i + w])))
                  for i in range(len(lines)) for w in (1, 2, 3))
        if hit:
            ok += 1
        else:
            miss.append(r)
    print('%-34s %d of %d rows corroborated' % (name + ':', ok, len(rows)))
    for r in miss:
        print('   UNEXPLAINED  %s | %s | %s' %
              (r.get('characteristic', r.get('package')),
               r.get('applies_to', r.get('ta_range')), r.get('symbol', '')))
    return miss


def check_monotonic():
    """Faster grades should not need looser timing.

    A handful of specifications genuinely break this, because the 16.67 MHz
    column is the separately binned 12F part rather than a faster screen of
    the 16 MHz part.  They are printed, not derived, so this only reports.

    Specifications whose minimum is negative are skipped: those are signed
    skews, where the tighter limit is the one closer to zero, so the rule
    would fire on every one of them for the wrong reason.
    """
    rows = list(csv.DictReader(open(os.path.join(HERE,
                                                 'ac-electrical-specifications.csv'))))
    flags = 0
    for r in rows:
        if r['unit'] not in ('ns',):
            continue
        for kind in ('min', 'max'):
            seq = [(g, r['%s_%s' % (g, kind)]) for g in GRADES
                   if r['%s_%s' % (g, kind)]]
            seq = [(g, float(v)) for g, v in seq
                   if re.fullmatch(r'-?\d+\.?\d*', v)]
            if any(v < 0 for _, v in seq):
                continue                       # a signed skew, not a duration
            for (g1, v1), (g2, v2) in zip(seq, seq[1:]):
                if v2 > v1:
                    flags += 1
                    print('   grade order  %-26s %-5s %-3s %s -> %s   %g -> %g'
                          % (r['table'], r['num'], kind, g1, g2, v1, v2))
    print('grade ordering: %d places where a faster grade has the looser limit'
          % flags)


def check_notes():
    """Every footnote marker a row uses should be defined under its table.

    Two tables genuinely fail this and both are recorded in README.md, so
    the check reports rather than fails: it is here to catch a transcription
    slip, not to relitigate the source's own bookkeeping.
    """
    rows = list(csv.DictReader(open(os.path.join(HERE,
                                                 'ac-electrical-specifications.csv'))))
    notes = list(csv.DictReader(open(os.path.join(HERE, 'ac-table-notes.csv'))))
    defined, used = {}, {}
    for n in notes:
        defined.setdefault(n['table'], set()).add(n['marker'])
    for r in rows:
        for m in r['footnotes'].split(','):
            if m.strip():
                used.setdefault(r['table'], set()).add(m.strip())
    dangling = orphan = 0
    for t in sorted(set(used) | set(defined)):
        for m in sorted(used.get(t, set()) - defined.get(t, set())):
            dangling += 1
            print('   dangling marker  %-28s %s referenced but never defined'
                  % (t, m))
        for m in sorted(defined.get(t, set()) - used.get(t, set()) - {'*', '**'}):
            orphan += 1
            print('   unreferenced     %-28s note %s' % (t, m))
    print('footnotes: %d markers used but not defined, %d notes defined but '
          'referenced by no row' % (dangling, orphan))


def main():
    pages = load_pages()
    bad = check_ac(pages)
    bad += check_dc(pages, 'dc-electrical-specifications.csv', ['min', 'max'])
    bad += check_dc(pages, 'power-dissipation.csv',
                    ['theta_c_per_w', 'pd_w_at_ta_min', 'tj_c_at_ta_min',
                     'pd_w_at_ta_max', 'tj_c_at_ta_max'])
    check_monotonic()
    check_notes()
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
