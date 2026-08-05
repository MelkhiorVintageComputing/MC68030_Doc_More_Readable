#!/usr/bin/env python3
"""Write the electrical-specification CSVs for Section 12 of MC68881UM.

The values below were read off 300 dpi renderings of PDF pages 378-381; the
embedded text layer of this scan is not trustworthy for numerals and was used
only as a second opinion (see check-spec-csv.py).  Every cell here has been
looked at.

An empty min/max cell means the source prints an em dash - the limit is not
specified, which is not the same as zero.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))

AC_COLS = ['table', 'pdf_page', 'printed_page', 'num', 'footnotes',
           'characteristic', 'condition', 'unit',
           'f1667_min', 'f1667_max', 'f20_min', 'f20_max',
           'f25_min', 'f25_max', 'f33_min', 'f33_max',
           'min_clks', 'max_clks', 'confidence', 'note']

COND = 'VCC = 5.0 Vdc +/- 5%; GND = 0 Vdc, TA = 0 to 70 C'

# ---------------------------------------------------------------------------
# 12.5 AC ELECTRICAL CHARACTERISTICS - CLOCK INPUT  (printed page 12-3)
# num, footnotes, characteristic, unit, values..., note
CLOCK = [
    ('',    '', 'Frequency of Operation', 'MHz',
     ('8', '16.67'), ('12.5', '20'), ('12.5', '25'), ('16.7', '33.33'), ''),
    ('1',   '', 'Cycle Time', 'ns',
     ('60', '125'), ('50', '80'), ('40', '80'), ('30', '60'), ''),
    ('2, 3', '', 'Clock Pulse Width (Measured from 1.5 V to 1.5 V for 33 MHz)', 'ns',
     ('24', '95'), ('20', '54'), ('15', '59'), ('14', '66'),
     'Figure 12-1 marks 3 on the high pulse and 2 on the low pulse; the table '
     'gives one row for both. At 33.33 MHz the maximum (66 ns) exceeds the '
     'maximum cycle time of 60 ns, which cannot hold: min pulse + max pulse = '
     '14 + 66 = 80 ns. Read from the page and corroborated by the text layer.'),
    ('4, 5', '', 'Rise and Fall Times', 'ns',
     ('', '5'), ('', '5'), ('', '4'), ('', '3'),
     'Figure 12-1 marks 5 on the rising edge and 4 on the falling edge.'),
]

# ---------------------------------------------------------------------------
# 12.6 AC ELECTRICAL CHARACTERISTICS - READ AND WRITE CYCLES
# (printed pages 12-4 and 12-5)
READ_WRITE = [
    (380, 4, '6', '5', 'Address Valid to AS Asserted', 'ns',
     ('15', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '6A', '5', 'Address Valid to DS Asserted (Read)', 'ns',
     ('15', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '6B', '5', 'Address Valid to DS Asserted (Write)', 'ns',
     ('50', ''), ('50', ''), ('35', ''), ('26', ''), '', '', ''),
    (380, 4, '7', '6', 'AS Negated to Address Invalid', 'ns',
     ('10', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '7A', '6', 'DS Negated to Address Invalid', 'ns',
     ('10', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '8', '9', 'CS Negated to AS Asserted', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), '', '', ''),
    (380, 4, '8A', '9', 'CS Negated to DS Asserted (Read)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), '', '', ''),
    (380, 4, '8B', '', 'CS Asserted to DS Asserted (Write)', 'ns',
     ('30', ''), ('25', ''), ('20', ''), ('15', ''), '', '', ''),
    (380, 4, '9', '', 'AS Negated to CS Negated', 'ns',
     ('10', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '9A', '', 'DS Negated to CS Negated', 'ns',
     ('10', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '10', '', 'R/W High to AS Asserted (Read)', 'ns',
     ('15', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '10A', '', 'R/W High to DS Asserted (Read)', 'ns',
     ('15', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '10B', '', 'R/W Low to DS Asserted (Write)', 'ns',
     ('35', ''), ('30', ''), ('25', ''), ('25', ''), '', '', ''),
    (380, 4, '11', '', 'AS Negated to R/W Low (Read) or AS Negated to R/W High (Write)', 'ns',
     ('10', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '11A', '', 'DS Negated to R/W Low (Read) or DS Negated to R/W High (Write)', 'ns',
     ('10', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '12', '', 'DS Width Asserted (Write)', 'ns',
     ('40', ''), ('38', ''), ('30', ''), ('23', ''), '', '', ''),
    (380, 4, '13', '', 'DS Width Negated', 'ns',
     ('40', ''), ('38', ''), ('30', ''), ('23', ''), '', '', ''),
    (380, 4, '13A', '4', 'DS Negated to AS Asserted', 'ns',
     ('30', ''), ('30', ''), ('25', ''), ('18', ''), '', '', ''),
    (380, 4, '14', '2', 'CS, DS Asserted to Data-Out Valid (Read)', 'ns',
     ('', '80'), ('', '45'), ('', '45'), ('', '30'), '', '',
     'The source prints a stray closing parenthesis: '
     '"CS, DS Asserted to Data-Out Valid) (Read)".'),
    (380, 4, '15', '', 'DS Negated to Data-Out Invalid (Read)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), '', '', ''),
    (380, 4, '16', '', 'DS Negated to Data-Out High Impedance (Read)', 'ns',
     ('', '50'), ('', '30'), ('', '30'), ('', '20'), '', '', ''),
    (380, 4, '17', '', 'Data-In Valid to DS Asserted (Write)', 'ns',
     ('15', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '18', '', 'DS Negated to Data-In Invalid (Write)', 'ns',
     ('15', ''), ('10', ''), ('5', ''), ('5', ''), '', '', ''),
    (380, 4, '19', '2', 'START True to DSACK0 and DSACK1 Asserted', 'ns',
     ('', '50'), ('', '35'), ('', '25'), ('', '20'), '', '', ''),
    (380, 4, '19A', '7', 'DSACK0 Asserted to DSACK1 Asserted (Skew)', 'ns',
     ('-15', '15'), ('-10', '10'), ('-10', '10'), ('', '5'), '', '',
     'The 33.33 MHz column gives no minimum, where the three slower grades '
     'are symmetric about zero. Read from the page, not inferred.'),
    (380, 4, '20', '', 'DSACK0 or DSACK1 Asserted to Data-Out Valid', 'ns',
     ('', '50'), ('', '43'), ('', '32'), ('', '17'), '', '', ''),
    (380, 4, '21', '8', 'START False to DSACK0 and DSACK1 Negated', 'ns',
     ('', '50'), ('', '30'), ('', '30'), ('', '20'), '', '', ''),
    (380, 4, '22', '8', 'START False to DSACK0 and DSACK1 High Impedance', 'ns',
     ('', '70'), ('', '40'), ('', '40'), ('', '30'), '', '', ''),
    (381, 5, '23', '3, 8', 'START True to Clock High (Synchronous Read)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), '', '', ''),
    (381, 5, '24', '3', 'Clock Low to Data-Out Valid (Synchronous Read)', 'ns',
     ('', '105'), ('', '80'), ('', '60'), ('', '45'), '', '', ''),
    (381, 5, '25', '3, 8', 'START True to Data-Out Valid (Synchronous Read)', 'ns',
     ('', '105'), ('', '80'), ('', '60'), ('', '45'), '1.5', '2.5',
     'Two-term limit: max is the nanosecond figure plus 2.5 clocks, '
     'min is 1.5 clocks with no nanosecond term.'),
    (381, 5, '26', '3', 'Clock Low to DSACK0 and DSACK1 Asserted (Synchronous Read)', 'ns',
     ('', '75'), ('', '55'), ('', '45'), ('', '30'), '', '', ''),
    (381, 5, '27', '3, 8', 'START True to DSACK0 and DSACK1 Asserted (Synchronous Read)', 'ns',
     ('', '75'), ('', '55'), ('', '45'), ('', '30'), '1.5', '2.5',
     'Two-term limit: max is the nanosecond figure plus 2.5 clocks, '
     'min is 1.5 clocks with no nanosecond term.'),
]

# ---------------------------------------------------------------------------
# 12.4 DC ELECTRICAL CHARACTERISTICS  (printed page 12-2)
DC = [
    ('Input High Voltage', '', '', 'VIH', '2.0', 'VCC', 'V',
     'Max is the symbol VCC, not a number.'),
    ('Input Low Voltage', '', '', 'VIL', 'GND-0.5', '0.8', 'V',
     'Min is symbolic: GND minus 0.5 V.'),
    ('Input Leakage Current', '@ 5.25 V',
     'CLK, RESET, R/W, A0-A4, CS, DS, AS, SIZE', 'Iin', '', '10', 'uA', ''),
    ('Hi-Z (Off State) Input Current', '@ 2.4 V / 0.4 V',
     'DSACK0, DSACK1, D0-D31', 'ITSI', '', '20', 'uA', ''),
    ('Output High Voltage', 'IOH = -400 uA',
     'DSACK0, DSACK1, D0-D31', 'VOH', '2.4', '', 'V', ''),
    ('Output Low Voltage', 'IOL = 5.3 mA',
     'DSACK0, DSACK1, D0-D31', 'VOL', '', '0.5', 'V', ''),
    ('Output Low Current', 'VOL = GND', 'SENSE', 'IOL', '', '500', 'uA', ''),
    ('Power Dissipation', '', '', 'PD', '', '0.75', 'W', ''),
    ('Capacitance', 'Vin = 0, TA = 25 C, f = 1 MHz', '', 'Cin', '', '20', 'pF',
     'Periodically sampled rather than 100% tested.'),
    ('Output Load Capacitance', '', '', 'CL', '', '130', 'pF', ''),
]


def write_ac():
    rows = []
    for num, fn, char, unit, a, b, c, d, note in CLOCK:
        rows.append(['clock', 379, '12-3', num, fn, char, COND, unit,
                     a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1],
                     '', '', 'high', note])
    for pdf, printed, num, fn, char, unit, a, b, c, d, mc, xc, note in READ_WRITE:
        rows.append(['read-write', pdf, '12-%d' % printed, num, fn, char, COND, unit,
                     a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1],
                     mc, xc, 'high', note])
    p = os.path.join(HERE, 'ac-electrical-specifications.csv')
    with open(p, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(AC_COLS)
        w.writerows(rows)
    print('%-38s %d rows, %d values'
          % (os.path.basename(p), len(rows),
             sum(1 for r in rows for c in r[8:18] if c)))


def write_dc():
    p = os.path.join(HERE, 'dc-electrical-specifications.csv')
    with open(p, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['pdf_page', 'printed_page', 'characteristic', 'condition',
                    'signals', 'symbol', 'min', 'max', 'unit', 'confidence', 'note'])
        for char, cond, sig, sym, lo, hi, unit, note in DC:
            w.writerow([378, '12-2', char, cond, sig, sym, lo, hi, unit, 'high', note])
    print('%-38s %d rows' % (os.path.basename(p), len(DC)))


if __name__ == '__main__':
    write_ac()
    write_dc()
