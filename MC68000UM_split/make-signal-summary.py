#!/usr/bin/env python3
"""Write signal-summary.csv and table-3-4-signal-summary.md.

Table 3-4 is the manual's one-page index of the bus: every signal, which way
it points, which level asserts it, and whether it goes high impedance when
the processor is halted or has given the bus away. It is printed on page
3-10 as an image with no usable text layer, which is why it is retyped here
from a 300 dpi rendering rather than extracted.

The second table on the page is not in the source at all. Table 3-4
describes one part - the 64-pin MC68000 - while the manual covers six, and
the differences are scattered through paragraphs 3.1 to 3.7 and the pin
assignments in Section 11. Every cell of it carries the page it came from.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------ Table 3-4 ----
# (signal name, mnemonic, input/output, active state, Hi-Z on HALT,
#  Hi-Z on bus relinquish, footnote, paragraph)
COLS = ['signal_name', 'mnemonic', 'direction', 'active_state',
        'hiz_on_halt', 'hiz_on_bus_relinquish', 'footnote', 'paragraph']
SIGNALS = [
    ('Address Bus',                   'A0-A23',          'Output',       'High',                  'Yes',  'Yes', '',  '3.1'),
    ('Data Bus',                      'D0-D15',          'Input/Output', 'High',                  'Yes',  'Yes', '',  '3.2'),
    ('Address Strobe',                'AS',              'Output',       'Low',                   'No',   'Yes', '',  '3.3'),
    ('Read/Write',                    'R/W',             'Output',       'Read-High Write-Low',   'No',   'Yes', '',  '3.3'),
    ('Data Strobe',                   'DS',              'Output',       'Low',                   'No',   'Yes', '',  '3.3'),
    ('Upper and Lower Data Strobes',  'UDS, LDS',        'Output',       'Low',                   'No',   'Yes', '',  '3.3'),
    ('Data Transfer Acknowledge',     'DTACK',           'Input',        'Low',                   'No',   'No',  '',  '3.3'),
    ('Bus Request',                   'BR',              'Input',        'Low',                   'No',   'No',  '',  '3.4'),
    ('Bus Grant',                     'BG',              'Output',       'Low',                   'No',   'No',  '',  '3.4'),
    ('Bus Grant Acknowledge',         'BGACK',           'Input',        'Low',                   'No',   'No',  '',  '3.4'),
    ('Interrupt Priority Level',      'IPL0, IPL1, IPL2', 'Input',       'Low',                   'No',   'No',  '',  '3.5'),
    ('Bus Error',                     'BERR',            'Input',        'Low',                   'No',   'No',  '',  '3.6'),
    ('Mode',                          'MODE',            'Input',        'High',                  '',     '',    '',  '3.6'),
    ('Reset',                         'RESET',           'Input/Output', 'Low',                   'No',   'No',  '*', '3.6'),
    ('Halt',                          'HALT',            'Input/Output', 'Low',                   'No',   'No',  '*', '3.6'),
    ('Enable',                        'E',               'Output',       'High',                  'No',   'No',  '',  '3.7'),
    ('Valid Memory Address',          'VMA',             'Output',       'Low',                   'No',   'Yes', '',  '3.7'),
    ('Valid Peripheral Address',      'VPA',             'Input',        'Low',                   'No',   'No',  '',  '3.7'),
    ('Function Code Output',          'FC0, FC1, FC2',   'Output',       'High',                  'No',   'Yes', '',  '3.8'),
    ('Clock',                         'CLK',             'Input',        'High',                  'No',   'No',  '',  '3.9'),
    ('Power Input',                   'VCC',             'Input',        '',                      '',     '',    '',  '3.10'),
    ('Ground',                        'GND',             'Input',        '',                      '',     '',    '',  '3.10'),
]

# Which paragraph heading each signal is described under, as printed.
PARAGRAPH = {
    '3.1': 'Address Bus', '3.2': 'Data Bus', '3.3': 'Asynchronous Bus Control',
    '3.4': 'Bus Arbitration Control', '3.5': 'Interrupt Control',
    '3.6': 'System Control', '3.7': 'M6800 Peripheral Control',
    '3.8': 'Processor Function Codes', '3.9': 'Clock', '3.10': 'Power Supply',
}

# --------------------------------------------------- per-processor table ---
# (signal, 68000/HC000/010, HC001, 68008 48-pin, 68008 52-pin, EC000, source)
PARTS = ['MC68000<br>MC68HC000<br>MC68010', 'MC68HC001',
         'MC68008<br>48-pin', 'MC68008<br>52-pin', 'MC68EC000']
AVAIL = [
    ('Address bus', 'A23–A0', 'A23–A0', 'A19–A0', 'A21–A0', 'A23–A0',
     'p. 3-3'),
    ('Data bus', 'D15–D0', 'D15–D0<br>(D7–D0 in 8-bit mode)', 'D7–D0', 'D7–D0',
     'D15–D0<br>(D7–D0 in 8-bit mode)', 'p. 3-4'),
    ('`UDS`, `LDS`', '✓', '✓', '—', '—', '✓', 'p. 3-4'),
    ('`DS`', '—', '—', '✓', '✓', '—', 'p. 3-5;<br>Fig. 11-4, 11-5'),
    ('`BGACK`', '✓', '✓', '—', '✓', '—',
     'pp. 3-5, 3-6;<br>Fig. 11-3, 11-4, 11-5'),
    ('`IPL0`, `IPL1`, `IPL2`', '✓', '✓', '`IPL0/IPL2` and `IPL1` only',
     '✓', '✓', 'p. 3-6;<br>Fig. 11-4, 11-5'),
    ('`MODE`', '—', '✓', '—', '—', '✓', 'p. 3-7;<br>Fig. 11-3, 11-6'),
    ('`E`', '✓', '✓', '✓', '✓', '—', 'Fig. 11-3, 11-4, 11-5'),
    ('`VMA`', '✓', '✓', '—', '—', '—', 'p. 3-8;<br>Fig. 11-3, 11-4, 11-5'),
    ('`VPA`', '✓', '✓', '✓', '✓', '—', 'Fig. 11-3, 11-4, 11-5'),
    ('`AVEC`', '—', '—', '—', '—', '✓', 'Fig. 3-3, 11-3, 11-6'),
]

DOC = """# Table 3-4 — Signal Summary

Reconstructed from **Table 3-4** of the M68000 8-/16-/32-Bit Microprocessors
User's Manual (PDF page 45, printed page 3-10 — see
[`06-section-03-signal-description.pdf`](06-section-03-signal-description.pdf)
page 10 for the original scan).

This is the manual's one-page index of the bus: every signal, which way it
points, which level asserts it, and whether it goes to high impedance when
the processor is halted or has handed the bus to another master. The page is
a scanned image with a text layer too damaged to quote — `UDS` comes back as
`UcJS`, `BERR` as `BEAR`, `RESET` as `RESEi` — so the table below was retyped
from a 300 dpi rendering.

## Table 3-4. Signal Summary

{table}

{footnote}

"Hi-Z" is the source's column heading. **On `HALT`** is the state while the
processor is halted; **On Bus Relinquish** is the state after it has given
the bus up to another master. A signal that is neither three-state nor
driven — `MODE`, `VCC`, `GND` — has a dash in both.

Overbars are lost in a plain-text table: `AS`, `DS`, `UDS`, `LDS`, `DTACK`,
`BR`, `BG`, `BGACK`, `IPL0`–`IPL2`, `BERR`, `RESET`, `HALT`, `VMA` and `VPA`
are all active low, which is also what the Active State column says.

Table 3-4 writes the buses ascending — `A0-A23`, `D0-D15` — where the signal
descriptions in 3.1 and 3.2 write them descending, `A23-A0` and `D15-D0`.
Same pins.

## Where each signal is described

{paras}

## What Table 3-4 does not tell you

Table 3-4 describes **one part**. The manual covers six, and they do not
have the same pins. The differences are stated in paragraphs 3.1 to 3.7 and
drawn in the pin assignments in Section 11; this table collects them, with
the page or figure each cell came from.

{avail}

✓ present · — no such pin

Two things follow from that table which the summary itself does not say.

**The MC68EC000's `AVEC` pin is missing from Section 3 altogether.** It is
the autovector input that takes the place of `VPA` on that part, and it is
named on Figure 3-3, in Section 5, in the notes under the MC68EC000 AC
tables and in three pin assignments — but there is no `AVEC` row in Table
3-4 and no paragraph describing it in 3.7, which is where `VPA` and `VMA`
are. Section 5 introduces it in passing: *"This is generated internally by
the microprocessor when VPA (or AVEC) is asserted on an interrupt
acknowledge cycle"* (page 5-10).

**Paragraph 3.4 contradicts itself about `BGACK`.**
Its opening says *"In the 48-pin version of the MC68008 and
MC68EC000, no pin is available for the bus grant acknowledge signal"*; the
`BGACK` paragraph a page later says only *"The 48-pin version of the
MC68008 has no pin available for the bus grant acknowledge signal"*. The
pin assignments settle it — the MC68EC000 has no `BGACK` — and so does
Section 10, whose MC68EC000 arbitration table has no specification 37 or 46
and whose Figure 10-14 has no `BGACK` row.

## Cross-checks

The signal groups in the DC tables of Section 10 are an independent listing
of the same pins, and they agree:

- §10.7's output-drive groups name `E`, `AS`, `A0-A23`, `BG`, `D0-D15`,
  `FC0-FC2`, `LDS`, `R/W`, `UDS` and `VMA`.
- §10.13, the MC68EC000 table, names `AS`, `A23-A0`, `BG`, `D15-D0`,
  `FC2-FC0`, `LDS`, `R/W` and `UDS` — **no `E` and no `VMA`** — and lists
  `AVEC` among the inputs where §10.7 lists `VPA`.

## Regenerating

The table above is generated from
[`signal-summary.csv`](signal-summary.csv):

```sh
python3 make-signal-summary.py
```
"""


def md_table(header, aligns, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(aligns) + "|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def main():
    path = os.path.join(HERE, 'signal-summary.csv')
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        w.writerows(SIGNALS)
    print('%-40s %3d rows' % ('signal-summary.csv', len(SIGNALS)))

    rows = []
    for name, mn, io, act, halt, relq, fn, para in SIGNALS:
        rows.append([name, ', '.join('`%s`' % m for m in mn.split(', ')),
                     io, act or '—',
                     (halt or '—') + fn, (relq or '—') + fn, '§' + para])
    table = md_table(
        ['Signal Name', 'Mnemonic', 'Input/Output', 'Active State',
         'Hi-Z<br>On `HALT`', 'Hi-Z<br>On Bus Relinquish', 'Described in'],
        ['---', ':-:', ':-:', ':-:', ':-:', ':-:', ':-:'], rows)

    paras = md_table(
        ['Paragraph', 'Heading', 'Signals'], ['---', '---', '---'],
        [['§%s' % p, PARAGRAPH[p],
          ', '.join('`%s`' % s[1] for s in SIGNALS if s[7] == p)]
         for p in sorted(PARAGRAPH, key=lambda k: [int(x) for x in k.split('.')])])

    avail = md_table(
        ['Signal'] + PARTS + ['Source'],
        ['---'] + [':-:'] * len(PARTS) + [':-:'],
        [list(a) for a in AVAIL])

    doc = DOC.format(table=table, paras=paras, avail=avail,
                     footnote='\\* Open drain.')
    open(os.path.join(HERE, 'table-3-4-signal-summary.md'), 'w').write(doc)
    print('%-40s %3d signals, %3d differences'
          % ('table-3-4-signal-summary.md', len(SIGNALS), len(AVAIL)))


if __name__ == '__main__':
    main()
