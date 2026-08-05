#!/usr/bin/env python3
"""Cross-check ac-electrical-specifications.csv against the source.

The values in the CSV were read from page images.  This script looks for
reasons to distrust them, from two independent directions:

  1. the PDF's own text layer.  It is bad enough that a positional comparison
     is meaningless - it drops and invents em dashes, so columns slide - but
     the *order* of the numerals it does recover is reliable.  So each row's
     numbers are required to appear, in order, as a subsequence of the
     numbers the text layer found on that row.

  2. monotonicity.  A faster grade of the same part should not need more
     time than a slower one.  Every limit that rises with frequency is
     reported for a human to look at; some are real.

Neither check can prove a value right.  Together they catch the two failure
modes that matter: a digit misread, and a value put in the wrong column.

Usage: python3 check-spec-csv.py [path/to/MC68881UM.pdf]
"""
import csv, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PDF = os.path.join(os.path.dirname(HERE), 'MC68881UM.pdf')
GRADES = [('16.67 MHz', 'f1667'), ('20 MHz', 'f20'),
          ('25 MHz', 'f25'), ('33.33 MHz', 'f33')]

# Rows whose numbers the text layer simply does not contain: on printed page
# 12-4 it drops the 25 MHz and 33.33 MHz columns of this block outright, so
# there is nothing to compare against.  Each was instead re-read at 3x zoom.
TEXT_LAYER_LOST = {
    '19':  'text layer keeps only the 16.67 MHz max',
    '19A': 'text layer loses the 25 MHz pair',
    '20':  'text layer loses the 25 and 33.33 MHz maxima',
    '22':  'text layer garbles the 33.33 MHz max to "3~"',
}

# the scan's usual letter-for-digit substitutions
FIX = str.maketrans({'O': '0', 'o': '0', 'l': '1', 'I': '1', '|': '1',
                     'S': '5', 'B': '8'})


def nums(s):
    return re.findall(r'-?\d+\.?\d*', s.translate(FIX))


def subseq(need, hay):
    it = iter(hay)
    return all(any(h == n for h in it) for n in need)


def text_lines(pdf, first, last):
    out = subprocess.run(['pdftotext', '-layout', '-f', str(first), '-l', str(last),
                          pdf, '-'], capture_output=True, text=True).stdout
    return [l for l in out.split('\n') if l.strip()]


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF
    rows = list(csv.DictReader(open(os.path.join(HERE, 'ac-electrical-specifications.csv'))))

    lines = {}
    for page in sorted({int(r['pdf_page']) for r in rows}):
        lines[page] = text_lines(pdf, page, page)

    print('=== text-layer corroboration')
    ok = miss = known = 0
    for r in rows:
        want = []
        for _, k in GRADES:
            want += nums(r['%s_min' % k]) + nums(r['%s_max' % k])
        if not want:
            continue
        # the row's numbers may be split over the wrapped characteristic, so
        # try every window of up to three consecutive lines on the page
        page = lines[int(r['pdf_page'])]
        hit = False
        for i in range(len(page)):
            for j in (1, 2, 3):
                if subseq(want, nums(' '.join(page[i:i + j]))):
                    hit = True
                    break
            if hit:
                break
        if hit:
            ok += 1
        elif r['num'] in TEXT_LAYER_LOST:
            known += 1
            print('  by eye    %-4s %-40s %s' % (r['num'], r['characteristic'][:40],
                                                 TEXT_LAYER_LOST[r['num']]))
        else:
            miss += 1
            print('  NO MATCH  %-4s %-58s %s' % (r['num'] or '-', r['characteristic'][:58],
                                                 ' '.join(want)))
    print('  %d of %d rows corroborated, %d verified by eye, %d unexplained'
          % (ok, ok + known + miss, known, miss))

    print('\n=== monotonicity across speed grades')
    flagged = 0
    for r in rows:
        if r['table'] != 'read-write':
            continue          # the clock table's own limits are not monotonic
        for what in ('min', 'max'):
            seq = [(g, r['%s_%s' % (k, what)]) for g, k in GRADES]
            seq = [(g, float(v)) for g, v in seq if v]
            for (ga, a), (gb, b) in zip(seq, seq[1:]):
                if b > a:
                    flagged += 1
                    print('  %-4s %-52s %s rises %g -> %g from %s to %s'
                          % (r['num'] or '-', r['characteristic'][:52], what,
                             a, b, ga, gb))
    print('  %d limit(s) rise with frequency' % flagged)
    return 1 if miss else 0


if __name__ == '__main__':
    sys.exit(main())
