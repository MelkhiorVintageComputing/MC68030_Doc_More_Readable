#!/usr/bin/env python3
"""Write pin-assignments.csv and pin-assignments.md.

Section 11.1 of MC68000UM.pdf gives the pin assignment of every package the
manual covers, as nine drawings over six pages (PDF pages 183-188, printed
11-2 to 11-7). They are line art in a scan, with no text layer worth the
name, so each was read by eye from a 200-400 dpi rendering and is recorded
below in pin order.

The drawings number their pins in three ways. The dual-in-line packages
count down one side and back up the other. The quad packs count
anticlockwise from the index mark, which sits at the middle of the top edge
of a 52- or 68-lead pack and at the top-left corner of the 64-lead one; each
drawing prints a handful of pin numbers at its corners and edge midpoints,
and every one of those was checked against the count. The pin grid arrays
are addressed by row letter and column number, as the drawing labels them.

What the drawings do not give is transcribed as nothing: a signal a package
does not carry has an empty cell, which is different from a pin printed "NC".
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------- Figure 11-1, p. 11-2 ----
DIP64 = """D4 D3 D2 D1 D0 AS UDS LDS R/W DTACK BG BGACK BR VCC CLK GND HALT RESET VMA E
VPA BERR IPL2 IPL1 IPL0 FC2 FC1 FC0 A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14
A15 A16 A17 A18 A19 A20 VCC A21 A22 A23 GND D15 D14 D13 D12 D11 D10 D9 D8 D7 D6
D5""".split()

# --------------------------------------------------- Figure 11-2, p. 11-3 ----
# Bottom view. Rows run K (top) to A (bottom), columns 1 to 10; the middle
# of the grid is empty, so rows H to C carry pins only near the edges.
PGA68 = {
    'K': 'NC FC2 FC0 A1 A3 A4 A6 A7 A9 NC',
    'J': 'BERR IPL0 FC1 NC A2 A5 A8 A10 A11 A14',
    'H': {1: 'E', 2: 'IPL2', 3: 'IPL1', 8: 'A13', 9: 'A12', 10: 'A16'},
    'G': {1: 'VMA', 2: 'VPA', 9: 'A15', 10: 'A17'},
    'F': {1: 'HALT', 2: 'RESET', 9: 'A18', 10: 'A19'},
    'E': {1: 'CLK', 2: 'GND', 9: 'VCC', 10: 'A20'},
    'D': {1: 'BR', 2: 'VCC', 9: 'GND', 10: 'A21'},
    'C': {1: 'BGACK', 2: 'BG', 3: 'R/W', 8: 'D13', 9: 'A23', 10: 'A22'},
    'B': 'DTACK LDS UDS D0 D3 D6 D9 D11 D14 D15',
    'A': 'NC AS D1 D2 D4 D5 D7 D8 D10 D12',
}

# ------------------------------------------ Figure 11-3 (1 of 2), p. 11-4 ----
QUAD68 = """D4 D3 D2 D1 D0 AS UDS LDS R/W DTACK BG BGACK BR VCC CLK GND GND NC HALT
RESET VMA E VPA BERR IPL2 IPL1 IPL0 FC2 FC1 FC0 NC A1 A2 A3 A4 A5 A6 A7 A8 A9
A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 VCC A21 A22 A23 GND GND D15 D14 D13
D12 D11 D10 D9 D8 D7 D6 D5""".split()

QUAD68_EC000 = """GND D4 D3 D2 D1 D0 AS UDS LDS R/W DTACK BG BGACK BR VCC CLK GND GND MODE
HALT RESET NC AVEC BERR IPL2 IPL1 IPL0 FC2 FC1 FC0 A0 A1 A2 A3 GND A4 A5 A6 A7
A8 A9 A10 A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 VCC A21 A22 A23 GND D15 D14
D13 D12 D11 D10 D9 D8 D7 D6 D5""".split()

# ---------------------------------- Figure 11-3 (2 of 2) and 11-4, p. 11-5 ----
# The MC68HC001 packages are the MC68000 ones with MODE on a pin the MC68000
# leaves unconnected. They are written out in full rather than derived, so
# that the check at the bottom can confirm that is all that differs.
QUAD68_HC001 = QUAD68[:17] + ['MODE'] + QUAD68[18:]

QUAD52_68008 = """A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A21 A14 VCC A15 GND A16 A17 A18
A19 A20 D7 D6 D5 D4 D3 D2 D1 D0 AS DS R/W DTACK BG BGACK BR CLK GND HALT RESET
E VPA BERR IPL1 IPL2 IPL0 FC2 FC1 FC0 A0 A1""".split()

# --------------------------------------------------- Figure 11-5, p. 11-6 ----
# Pin 42 carries IPL2 and IPL0 tied together; it is printed "IPL2/IPL0".
DIP48_68008 = """A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 VCC A15 GND A16 A17 A18 A19 D7
D6 D5 D4 D3 D2 D1 D0 AS DS R/W DTACK BG BR CLK GND HALT RESET E VPA BERR IPL1
IPL2/IPL0 FC2 FC1 FC0 A0 A1 A2""".split()

# --------------------------------------------------- Figure 11-6, p. 11-7 ----
QFP64_EC000 = """R/W DTACK BG BR VCC CLK GND MODE HALT RESET AVEC BERR IPL2 IPL1 IPL0 FC2
FC1 FC0 A0 A1 A2 A3 GND A4 A5 A6 A7 A8 A9 A10 A11 A12 A13 A14 A15 A16 A17 A18
A19 A20 VCC A21 A22 A23 D15 D14 D13 D12 D11 D10 D9 D8 D7 D6 D5 GND D4 D3 D2
D1 D0 AS UDS LDS""".split()


def grid(rows):
    out = {}
    for row, cells in rows.items():
        if isinstance(cells, str):
            cells = dict(enumerate(cells.split(), 1))
        for col, sig in cells.items():
            out['%s%d' % (row, col)] = sig
    return out


def numbered(signals):
    return {str(i): s for i, s in enumerate(signals, 1)}


# (column, parts, package, figure, printed page, PDF page, pin -> signal)
PACKAGES = [
    ('dip64', 'MC68000, MC68010, MC68HC000', '64-pin dual in line',
     '11-1', '11-2', 183, numbered(DIP64)),
    ('pga68', 'MC68000, MC68010, MC68HC000', '68-lead pin grid array',
     '11-2', '11-3', 184, grid(PGA68)),
    ('pga68_hc001', 'MC68HC001', '68-lead pin grid array',
     '11-2', '11-3', 184, {**grid(PGA68), 'K1': 'MODE'}),
    ('quad68', 'MC68000, MC68HC000, MC68010', '68-lead quad pack',
     '11-3', '11-4', 185, numbered(QUAD68)),
    ('quad68_ec000', 'MC68EC000', '68-lead quad pack',
     '11-3', '11-4', 185, numbered(QUAD68_EC000)),
    ('quad68_hc001', 'MC68HC001', '68-lead quad pack',
     '11-3', '11-5', 186, numbered(QUAD68_HC001)),
    ('quad52', 'MC68008', '52-lead quad pack',
     '11-4', '11-5', 186, numbered(QUAD52_68008)),
    ('dip48', 'MC68008', '48-pin dual in line',
     '11-5', '11-6', 187, numbered(DIP48_68008)),
    ('qfp64_ec000', 'MC68EC000', '64-lead quad flat pack',
     '11-6', '11-7', 188, numbered(QFP64_EC000)),
]

# Row order: the buses, then the control signals in Table 3-4's order, then
# the signals only some parts have, then power and unconnected pins.
ORDER = (['A%d' % i for i in range(24)] + ['D%d' % i for i in range(16)] +
         ['AS', 'R/W', 'UDS', 'LDS', 'DS', 'DTACK', 'BR', 'BG', 'BGACK',
          'IPL0', 'IPL1', 'IPL2', 'BERR', 'MODE', 'RESET', 'HALT', 'E', 'VMA',
          'VPA', 'AVEC', 'FC0', 'FC1', 'FC2', 'CLK', 'VCC', 'GND', 'NC'])

POWER = ('VCC', 'GND', 'NC')


def pin_key(pin):
    return (pin[0], int(pin[1:])) if pin[0].isalpha() else ('', int(pin))


def check():
    """Every package accounts for each of its pins exactly once.

    The DIP and quad packs must use the numbers 1 to N with none missing; the
    grid arrays must fill exactly 68 positions. Beyond that, three
    comparisons that would each catch a misread pin: the MC68HC001 packages
    differ from their MC68000 twins in one pin only; the MC68000 64-pin DIP
    and 68-lead quad pack share their first sixteen pins; and the MC68EC000
    68-lead quad pack is the 64-lead QFP's signals plus four more pins.
    """
    for col, _, _, _, _, _, pins in PACKAGES:
        size = {'dip64': 64, 'dip48': 48, 'quad52': 52,
                'qfp64_ec000': 64}.get(col, 68)
        assert len(pins) == size, (col, len(pins))
        if not col.startswith('pga'):
            assert sorted(pins, key=int) == [str(i) for i in range(1, size + 1)]
        for sig in pins.values():
            for one in sig.split('/') if sig != 'R/W' else [sig]:
                assert one in ORDER, (col, one)

    base = {c: p for c, *_, p in PACKAGES}
    for a, b in (('pga68', 'pga68_hc001'), ('quad68', 'quad68_hc001')):
        diff = [k for k in base[a] if base[a][k] != base[b][k]]
        assert len(diff) == 1 and base[b][diff[0]] == 'MODE', (a, b, diff)
    assert DIP64[:16] == QUAD68[:16]
    qfp = sorted(s for s in QFP64_EC000)
    quad = sorted(s for s in QUAD68_EC000)
    for s in qfp:
        quad.remove(s)
    assert sorted(quad) == ['BGACK', 'GND', 'GND', 'NC'], quad


def table():
    rows = []
    for sig in ORDER:
        row = {'signal': sig}
        for col, _, _, _, _, _, pins in PACKAGES:
            hits = [p for p, s in pins.items()
                    if s == sig or (s != 'R/W' and sig in s.split('/'))]
            row[col] = ', '.join(sorted(hits, key=pin_key))
        if any(row[c] for c, *_ in PACKAGES):
            rows.append(row)
    return rows


def write_csv(rows):
    cols = ['signal'] + [c for c, *_ in PACKAGES]
    with open(os.path.join(HERE, 'pin-assignments.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(HERE, 'pin-assignment-packages.csv'), 'w',
              newline='') as f:
        w = csv.writer(f)
        w.writerow(['column', 'parts', 'package', 'figure', 'printed_page',
                    'pdf_page', 'pins'])
        for col, parts, pkg, fig, printed, pdf, pins in PACKAGES:
            w.writerow([col, parts, pkg, fig, printed, pdf, len(pins)])
    print('pin-assignments.csv: %d signals x %d packages' % (len(rows),
                                                          len(PACKAGES)))


MD_HEAD = """# M68000 family — pin assignments by package

Section 11.1 of the M68000 user's manual (PDF pages 183–188, printed pages
11-2 to 11-7) draws the pin assignment of every package it covers — nine
drawings for six processors. This puts them side by side: one row per signal,
one column per package, and in each cell the pin that carries the signal.

**An empty cell (—) means the package has no such pin.** That is different
from `NC`, which is a pin the package has and leaves unconnected; the `NC`
row lists those. Where a signal is on several pins — `VCC` and `GND` — every
one is listed.

The same data is in [`pin-assignments.csv`](pin-assignments.csv), with the
package columns described in
[`pin-assignment-packages.csv`](pin-assignment-packages.csv). Both are
written by [`make-pin-assignments.py`](make-pin-assignments.py).

## The packages

| Column | Parts | Package | Figure | Page (printed / PDF) | Pins |
|---|---|---|---|---|--:|
"""

MD_NOTES = """
## Reading the drawings

The drawings are line art in a scan, with no usable text layer, so every pin
was read by eye from a 200–400 dpi rendering. They number their pins three
ways:

- **Dual in line** packs count down the left side from pin 1 at the notch and
  back up the right.
- **Quad packs** count anticlockwise from the index mark — at the middle of
  the top edge on the 52- and 68-lead packs, at the top-left corner on the
  64-lead one. Each drawing prints a few pin numbers at its corners and edge
  midpoints (9, 10, 18, 26, 27, 35, 43, 44, 52, 60, 61 on the 68-lead packs),
  and every one of those falls on the pin the count says it should.
- **Pin grid arrays** are addressed by row letter (K at the top to A at the
  bottom, bottom view) and column number, exactly as the drawing labels them.

`make-pin-assignments.py` refuses to write anything unless each package
accounts for every one of its pins exactly once, and unless three
comparisons hold that would each expose a misread pin: the two MC68HC001
packages differ from their MC68000 twins in one pin only, the one that
carries `MODE`; the MC68000 64-pin DIP and 68-lead quad pack assign their
first sixteen pins identically; and the MC68EC000 68-lead quad pack is its
64-lead QFP plus exactly `BGACK`, two more `GND` and one `NC`.

## Things the drawings show that the text does not say

- **The MC68008 48-pin DIP ties `IPL2` and `IPL0` to one pin**, 42, printed
  `IPL2/IPL0`. That pin appears in both rows above.
- **The MC68HC001 is the MC68000 pinout plus `MODE`.** It takes pin K1 on the
  grid array and pin 18 on the quad pack, both of which the MC68000 leaves
  `NC`.
- **The MC68EC000's two packages disagree about `BGACK`.** The 68-lead quad
  pack carries it on pin 13; the 64-lead quad flat pack has no such pin. Its
  absence from the smaller package is consistent with the opening of
  paragraph 3.4, which says the MC68EC000 has no `BGACK`; its presence on the
  larger one is not.
- **Only the MC68EC000 and MC68008 packages bring out `A0`.** The MC68000,
  MC68010, MC68HC000 and MC68HC001 start their address bus at `A1`, using
  `UDS`/`LDS` for byte selection instead.
- **The MC68008 52-lead pack's four extra pins go to `A20`, `A21`, `BGACK`
  and a pin of its own for `IPL0`.** The 48-pin DIP does without all four:
  its address bus stops at `A19`, it has no `BGACK`, and it ties `IPL0` to
  `IPL2`.
"""


def write_md(rows):
    out = [MD_HEAD.rstrip('\n')]
    for col, parts, pkg, fig, printed, pdf, pins in PACKAGES:
        out.append('| `%s` | %s | %s | %s | %s / %d | %d |'
                   % (col, parts, pkg, fig, printed, pdf, len(pins)))
    out += ['', '## Pins by signal', '',
            '| Signal | ' + ' | '.join('`%s`' % c for c, *_ in PACKAGES) + ' |',
            '|---|' + ':-:|' * len(PACKAGES)]
    for r in rows:
        sig = r['signal']
        cells = [r[c] or '—' for c, *_ in PACKAGES]
        out.append('| `%s` | %s |' % (sig, ' | '.join(cells)))
    out.append(MD_NOTES)
    with open(os.path.join(HERE, 'pin-assignments.md'), 'w') as f:
        f.write('\n'.join(out))
    print('pin-assignments.md: %d rows' % len(rows))


if __name__ == '__main__':
    check()
    rows = table()
    write_csv(rows)
    write_md(rows)
