# Figure 10-8. Bus Arbitration Timing

Redrawn from **Figure 10-8** of the M68000 8-/16-/32-Bit Microprocessors
User's Manual (PDF page 170, printed page 10-19 — see
[`13-section-10-electrical-and-thermal-characteristics.pdf`](13-section-10-electrical-and-thermal-characteristics.pdf) page 19 for the original scan).

The same handshake as Figure 10-7 with the whole bus shown. `BGACK` applies only to the 52-pin MC68008 and to the processors that have the pin; the 48-pin MC68008 arbitrates with two wires. **This figure carries exactly the same caption as Figure 10-7** — see the README.

![Figure 10-8. Bus Arbitration Timing](figure-10-08-bus-arbitration.svg)

## Specifications marked on this figure

<!-- BEGIN TABLE from=ac-electrical-specifications.csv table=bus-arbitration grades=m68000 nums=33|34|35|36|37|37A|38|46|47|57|57A -->
| Num. | Characteristic | Unit | 8 MHz | 10 MHz | 12.5 MHz | 16.67 MHz 12F | 16 MHz | 20 MHz |
|:-:|---|:-:|--:|--:|--:|--:|--:|--:|
| 33 | Clock High to BG Asserted | ns | ≤ 62 | ≤ 50 | ≤ 40 | 0&nbsp;–&nbsp;40 | 0&nbsp;–&nbsp;30 | 0&nbsp;–&nbsp;25 |
| 34 | Clock High to BG Negated | ns | ≤ 62 | ≤ 50 | ≤ 40 | 0&nbsp;–&nbsp;40 | 0&nbsp;–&nbsp;30 | 0&nbsp;–&nbsp;25 |
| 35 | BR Asserted to BG Asserted | Clks | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 |
| 36<sup>1</sup> | BR Negated to BG Negated | Clks | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 |
| 37 | BGACK Asserted to BG Negated | Clks | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 |
| 37A<sup>2</sup> | BGACK Asserted to BR Negated | Clks/ns | 20&nbsp;–&nbsp;1.5 | 20&nbsp;–&nbsp;1.5 | 20&nbsp;–&nbsp;1.5 | 10&nbsp;–&nbsp;1.5 | 10&nbsp;–&nbsp;1.5 | 10&nbsp;–&nbsp;1.5 |
| 38 | BG Asserted to Control, Address, Data Bus High Impedance (AS Negated) | ns | ≤ 80 | ≤ 70 | ≤ 60 | ≤ 50 | ≤ 50 | ≤ 42 |
| 46 | BGACK Width Low | Clks | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 |
| 47 | Asynchronous Input Setup Time | ns | ≥ 10 | ≥ 10 | ≥ 10 | ≥ 5 | ≥ 5 | ≥ 5 |
| 57 | BGACK Negated to AS, DS, R/W Driven | Clks | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 |
| 57A | BGACK Negated to FC, VMA Driven | Clks | ≥ 1 | ≥ 1 | ≥ 1 | ≥ 1 | ≥ 1 | ≥ 1 |
<!-- END TABLE -->

A range `a – b` is min–max; `≤ b` is a maximum with no minimum specified; `≥ a`
is a minimum with no maximum; `—` is not specified at that grade. The
superscript on a specification number is its footnote in the source table.
Full descriptions, footnotes, test conditions and the source page of every row
are in [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv).

The source's note: "Waveform measurements for all inputs and outputs are
specified at: logic high 2.0 V, logic low = 0.8 V. 1. MC68008 52-Pin Version
only."

## About this redrawing

The source figure carries no state ruler and compresses its middle with a drafting break, so it has no horizontal scale to recover. This redrawing runs the whole sequence at one scale instead, at event times chosen so that **every specification the figure marks holds at once** — the arithmetic is in the `ARBITRATION` block of `make-figure-svg.py`.

**Callout anchors follow what each specification measures**, per its
description in [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv),
rather than the pixel position of the arrowhead on the scan. Where the two
disagree the CSV wins, because the CSV is where the numbers live.

Overbars are lost in the redrawing: `AS`, `DS`, `UDS`, `LDS`, `DTACK`, `BERR`,
`BR`, `BG`, `BGACK`, `HALT`, `RESET`, `VMA` and `VPA` are all active low.
A signal drawn on a mid-rail line is not being driven at all.

Rendered as a plain SVG referenced as an image, which is the only diagram
format that survives GitHub's markdown pipeline — GitHub supports no waveform
syntax (Mermaid has none) and strips inline `<svg>`. The figure adapts to
light and dark themes.

## Regenerating

```sh
python3 make-figure-svg.py 8      # redraw this figure
python3 make-figure-tables.py         # refresh the table above from the CSV
```
