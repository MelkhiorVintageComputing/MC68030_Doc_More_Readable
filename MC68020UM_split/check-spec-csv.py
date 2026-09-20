#!/usr/bin/env python3
"""Cross-check the Section 10 CSVs against a second reading of the manual.

make-spec-csv.py parses the tables out of mutool's character stream, so that
it can see the font and the size of every glyph. This re-reads the same pages
with poppler's layout-preserving extraction instead - a different library
taking a different route to a different intermediate form - and compares.

Poppler is the weaker reading of the two: it decodes nothing, so an em dash
arrives as a capital N-tilde and the Symbol font's mu arrives as a plain m.
That is exactly what makes it a useful check. It sees the same glyphs in the
same order, and the numbers it returns are the numbers on the page, so every
row's limits must turn up in it as a subsequence even though none of the
words will match.

Five directions:

  A  every AC row's limits, as a subsequence of the numbers poppler finds on
     the line that carries that row;
  B  the same for the DC, maximum rating and thermal tables;
  C  grade ordering - a faster part should not carry a looser limit;
  D  footnote markers used against footnote markers defined;
  E  the microamp and milliamp cells, which are the one place the two
     readings must legitimately disagree.

Usage:  python3 check-spec-csv.py

Exits non-zero only on an unexplained mismatch.
"""
import collections
import csv
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'MC68020UM.pdf')

GRADES = ['f16_67', 'f20', 'f25', 'f33_33']

# What poppler makes of the characters the generator decodes. The Type 1
# fonts are MacRoman and the extraction reports the raw byte, so these are
# the code points read as Latin-1.
AS_POPPLER_READS_IT = str.maketrans({
    '—': 'Ñ', '–': 'Ð', '’': 'Õ',
    '“': 'Ò', '”': 'Ó', '•': '¥',
    'θ': 'q', 'µ': 'm', '≤': '£', '≈': '»',
})

# Cells where the two readings must differ, because poppler cannot tell the
# Symbol font's mu from an ordinary m. Every one of them is a current, and
# every one is a test condition of the DC tables.
MICROAMP = 'µA'

# Rows whose numbers do not appear on the page in the order the CSV lists
# them, with the reason. The subsequence test is order-sensitive on purpose,
# so each of these is named rather than the test being loosened.
KNOWN_ORDER = {
    ('Input Low Voltage', 'VIL'):
        'the minimum is "GND -0.5" set across two lines, so the maximum of '
        '0.8 is printed between the two halves of it',
}


def numbers(text):
    """Every number in a piece of text, with the minus signs regularised.

    The manual sets a minus as an en dash, which the generator decodes and
    poppler hands back as the raw MacRoman byte, so both spellings have to
    be brought to one before anything can be compared.
    """
    return re.findall(r'-?\d+\.?\d*', text.replace('–', '-')
                      .replace('Ð', '-'))


def as_number(value):
    """The value as a plain number, or None if it is not one."""
    got = numbers(value)
    return got[0] if len(got) == 1 else None


def subsequence(want, have):
    it = iter(have)
    return all(any(h == w for h in it) for w in want)


def pages():
    out = subprocess.run(['pdftotext', '-layout', SRC, '-'],
                         capture_output=True, text=True, check=True).stdout
    return out.split('\f')


def rows(name):
    with open(os.path.join(HERE, name)) as f:
        return list(csv.DictReader(f))


def find(page_text, want):
    """Is this row's list of numbers a subsequence of some line of the page?"""
    lines = page_text.split('\n')
    for i in range(len(lines)):
        for span in (1, 2, 3):
            if subsequence(want, numbers(' '.join(lines[i:i + span]))):
                return True
    return False


def check_ac(book):
    data = rows('ac-electrical-specifications.csv')
    ok, bad = 0, []
    for r in data:
        want = [as_number(v) for g in GRADES
                for v in (r['%s_min' % g], r['%s_max' % g]) if v]
        want = [v for v in want if v is not None]
        if not want:
            ok += 1
            continue
        if find(book[int(r['pdf_page']) - 1], want):
            ok += 1
        else:
            bad.append((r['table'], r['num'], r['characteristic']))
    print('AC: %d of %d rows corroborated by poppler, %d unexplained'
          % (ok, len(data), len(bad)))
    for t, n, c in bad:
        print('   UNEXPLAINED  %-12s %-5s %s' % (t, n, c[:52]))
    return bad


def check_tables(book):
    bad = []
    for name, cells in (('dc-electrical-specifications.csv', ('min', 'max')),
                        ('thermal-characteristics.csv', ('value',))):
        data = rows(name)
        ok, miss, known = 0, [], []
        for r in data:
            want = [as_number(r[c]) for c in cells]
            want = [v for v in want if v is not None]
            if not want:
                ok += 1
                continue
            key = (r.get('characteristic', ''), r.get('symbol', ''))
            if find(book[int(r['pdf_page']) - 1], want):
                ok += 1
            elif key in KNOWN_ORDER:
                known.append(key)
            else:
                miss.append(r)
        print('%-38s %d of %d rows corroborated, %d printed out of order'
              % (name + ':', ok, len(data), len(known)))
        for key in known:
            print('   out of order %-28s %s' % (key[0], KNOWN_ORDER[key]))
        for r in miss:
            print('   UNEXPLAINED  %s | %s' %
                  (r.get('characteristic', r.get('row')), r.get('symbol', '')))
        bad += miss
    return bad


def check_grade_order():
    """A faster part should not need a looser limit.

    Only maxima are compared, and only where both are plain numbers: a
    minimum that is a setup or hold time legitimately stays flat across the
    grades, and a negative minimum is a signed skew, where the tighter limit
    is the one nearer zero.
    """
    data = rows('ac-electrical-specifications.csv')
    flags = 0
    for r in data:
        if r['unit'] != 'ns':
            continue
        seq = [(g, r['%s_max' % g]) for g in GRADES]
        seq = [(g, float(v)) for g, v in seq
               if re.fullmatch(r'\d+\.?\d*', v)]
        for (g1, v1), (g2, v2) in zip(seq, seq[1:]):
            if v2 > v1:
                flags += 1
                print('   grade order  %-12s %-5s %s -> %s   %g -> %g'
                      % (r['table'], r['num'], g1, g2, v1, v2))
    print('grade ordering: %d places where a faster grade has the looser maximum'
          % flags)


def check_notes():
    data = rows('ac-electrical-specifications.csv')
    notes = rows('ac-table-notes.csv')
    defined, used = collections.defaultdict(set), collections.defaultdict(set)
    for n in notes:
        defined[n['table']].add(n['marker'])
    for r in data:
        for marker in r['footnotes'].split(','):
            if marker:
                used[r['table']].add(marker)
    dangling = orphan = 0
    for table in sorted(set(defined) | set(used)):
        for marker in sorted(used[table] - defined[table]):
            dangling += 1
            print('   dangling marker  %-12s %s referenced but never defined'
                  % (table, marker))
        column = {n['marker'] for n in notes
                  if n['table'] == table and n['applies_to']}
        for marker in sorted(defined[table] - used[table] - column):
            orphan += 1
            print('   unreferenced     %-12s note %s' % (table, marker))
    print('footnotes: %d markers used but not defined, %d notes defined but '
          'referenced by no row' % (dangling, orphan))
    return dangling


def check_microamps(book):
    """The one place the two readings must disagree.

    Poppler cannot tell the Symbol font's mu from an m, so every microamp in
    the CSVs has to come back from it as a milliamp. Finding that it does is
    what shows the distinction was made by the font and not invented.
    """
    data = rows('dc-electrical-specifications.csv')
    micro = [r for r in data if MICROAMP in (r['unit'] + r['condition'])]
    milli = [r for r in data if 'mA' in (r['unit'] + r['condition'])]
    lost = 0
    for r in micro:
        text = book[int(r['pdf_page']) - 1]
        if MICROAMP in text:
            print('   UNEXPLAINED  poppler shows a real µ on page %s'
                  % r['pdf_page'])
            lost += 1
    print('units: %d cells read as microamps and %d as milliamps; poppler '
          'renders every one of them "mA", %d exceptions'
          % (len(micro), len(milli), lost))
    return lost


def main():
    book = pages()
    bad = check_ac(book)
    bad += check_tables(book)
    check_grade_order()
    bad += [1] * check_notes()
    bad += [1] * check_microamps(book)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
