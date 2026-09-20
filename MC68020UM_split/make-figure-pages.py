#!/usr/bin/env python3
"""Write one markdown page per Section 10 figure.

Each page carries the figure and, beside it, every specification the figure
marks - the same rows out of ac-electrical-specifications.csv, at all four
speed grades, with the footnotes those rows reference. The manual prints the
figure on one page and the table three pages earlier, so reading a callout
off the diagram means turning back and forth; this puts the two together.

Which specifications a figure marks is not guessed: the callout numbers are
read off the figure's own page in the source, and checked against the spans
the generator draws.
"""
import collections
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

GRADES = [('16.67 MHz', 'f16_67'), ('20 MHz', 'f20'),
          ('25 MHz', 'f25'), ('33.33 MHz', 'f33_33')]

# (slug, figure number, title, svg, table, printed page of the figure)
FIGURES = [
    ('figure-10-01-drive-levels', '10-1',
     'Drive Levels and Test Points for AC Specifications', None, None, 280),
    ('figure-10-02-clock-input-timing', '10-2', 'Clock Input Timing Diagram',
     'figure-10-02-clock-input-timing.svg', 'clock', 281),
    ('figure-10-03-read-cycle', '10-3', 'Read Cycle Timing Diagram',
     'figure-10-03-read-cycle.svg', 'read-write', 285),
    ('figure-10-04-write-cycle', '10-4', 'Write Cycle Timing Diagram',
     'figure-10-04-write-cycle.svg', 'read-write', 286),
    ('figure-10-05-bus-arbitration', '10-5', 'Bus Arbitration Timing Diagram',
     'figure-10-05-bus-arbitration.svg', 'read-write', 287),
]

# Figure 10-2 sits directly under the clock table, so a scan of its page
# cannot tell a callout from a value in the table above it. Its five
# callouts are listed here instead; they are the whole of that table.
CALLOUTS = {'10-2': ['1', '2,3', '4,5']}

RULER = ("The horizontal axis is bus states, six of which - S0 to S5 - are "
         "labelled as the source labels them. Placement is schematic, as it "
         "is in the manual: the edge ramps are exaggerated and nothing is to "
         "scale. Read the ordering and what each callout measures from the "
         "diagram, and the numbers from the table.")

NORULER = ("The horizontal axis is time, with no scale. The callouts mark "
           "what each specification measures, not how long it is.")

SPEC = ("Every specification the figure marks, at all four speed grades, as "
        "printed in Section 10. An em dash is the manual's own \"not "
        "specified\"; a `*` against a number means the MC68EC020 has no such "
        "signal. The footnotes below the table are the ones these rows "
        "reference - [`ac-table-notes.csv`](ac-table-notes.csv) holds all of "
        "them.")

DRIVE_LEVELS = """This figure defines how every other AC specification in the section is
measured: which voltage an input must be driven to, which threshold an output
delay is taken from, and where a signal-to-signal specification starts and
ends. It carries no specification of its own - the only number on it is the
figure's own label - so there is nothing to tabulate beside it, and it is the
one figure in the section that is reproduced here as text rather than redrawn.

The manual's own legend and notes, verbatim:

%s

The 2.0 V and 0.8 V thresholds named throughout are the ones the clock figure
marks; see [Figure 10-2](figure-10-02-clock-input-timing.md).
"""


def rows(name):
    with open(os.path.join(HERE, name)) as f:
        return list(csv.DictReader(f))


def order(num):
    m = re.match(r'(\d+)([A-Z]?)', num)
    return (int(m.group(1)), m.group(2))


def callouts_of(page, known):
    """The specification numbers printed on one figure's page."""
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('m', os.path.join(HERE, 'make-spec-csv.py'))
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    got = []
    for line in mod.lines_of(page):
        text = mod.text_of(line)
        if text.startswith(('Figure', 'NOTE', 'LEGEND', '*')) or 'USER' in text:
            continue
        got += [t[2] for t in line if t[2] in known]
    return sorted(set(got), key=order)


def legend_of(page):
    """The LEGEND and NOTES blocks printed under Figure 10-1."""
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('m', os.path.join(HERE, 'make-spec-csv.py'))
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    out, keep = [], False
    for line in mod.lines_of(page):
        text = mod.text_of(line).strip()
        if text.startswith(('NOTES:', 'LEGEND:')):
            keep = True
            out.append('')
            out.append('**%s**' % text)
            out.append('')
            continue
        # the figure's own corner stamp, set inside the artwork
        if text in ('FIGURE 10-1', 'MC68020UM'):
            continue
        if not keep or not text or 'USER' in text or text.startswith('Figure'):
            continue
        m = re.match(r'^([0-9]{1,2}|[A-F])\.\s+(.*)$', text)
        if m:
            out.append('- **%s.** %s' % (m.group(1), m.group(2)))
        elif out and out[-1].startswith('- '):
            out[-1] += ' ' + text
    return '\n'.join(out).strip()


def table_for(spec_rows, notes, nums):
    head = ['Spec', 'Characteristic']
    for label, _ in GRADES:
        head += ['%s min' % label, '%s max' % label]
    head += ['Unit']
    out = ['| ' + ' | '.join(head) + ' |',
           '|---|---|' + '--:|--:|' * len(GRADES) + '---|']
    used = set()
    for r in sorted((r for r in spec_rows if r['num'] in nums),
                    key=lambda r: (order(r['num']), r['condition'])):
        marks = [f for f in r['footnotes'].split(',') if f]
        used |= set(marks)
        num = r['num'] + ('<sup>%s</sup>' % ','.join(marks).replace('*', '&ast;')
                          if marks else '')
        what = r['characteristic'] + (' (%s)' % r['condition']
                                      if r['condition'] else '')
        cells = []
        for _, g in GRADES:
            cells += [r['%s_min' % g] or '', r['%s_max' % g] or '']
        out.append('| %s | %s | %s | %s |'
                   % (num, what, ' | '.join(cells), r['unit']))
    return out, used


def footnotes_for(notes, table, used):
    out = []
    for n in notes:
        if n['table'] != table:
            continue
        if n['applies_to'] or n['marker'] in used:
            out.append('- **%s** %s'
                       % (n['marker'].replace('*', '&ast;'), n['text']))
    return out


def main():
    spec_rows = rows('ac-electrical-specifications.csv')
    notes = rows('ac-table-notes.csv')
    known = {r['num'] for r in spec_rows}

    for slug, number, title, svg, table, page in FIGURES:
        out = ['# Figure %s. %s' % (number, title), '',
               'MC68020/MC68EC020 User\'s Manual, printed page 10-%d '
               '(PDF page %d of `../MC68020UM.pdf`).'
               % (page - 274, page), '']
        if svg is None:
            out.append(DRIVE_LEVELS % legend_of(page))
        else:
            out += ['![Figure %s](%s)' % (number, svg), '',
                    RULER if table == 'read-write' else NORULER, '',
                    '## Specifications marked on this figure', '', SPEC, '']
            nums = CALLOUTS.get(number) or callouts_of(page, known)
            body, used = table_for(spec_rows, notes, nums)
            out += body
            feet = footnotes_for(notes, table, used)
            if feet:
                out += ['', '### Footnotes', ''] + feet
            made = ('drawn by hand, because it has no bus states to lay out '
                    'against' if number == '10-2' else
                    'generated by `make-figure-svg.py`')
            out += ['', 'The figure is %s. Regenerate this page with '
                    '`python3 make-figure-pages.py`.' % made]
        with open(os.path.join(HERE, slug + '.md'), 'w') as f:
            f.write('\n'.join(out).rstrip() + '\n')
        print('%-42s %s' % (slug + '.md:',
                            'legend only' if svg is None
                            else '%d specifications' % (len(body) - 2)))


if __name__ == '__main__':
    main()
