# Figure 10-7. Bus Arbitration Timing

Redrawn from **Figure 10-7** of the M68000 8-/16-/32-Bit Microprocessors
User's Manual (PDF page 169, printed page 10-18 — see
[`13-section-10-electrical-and-thermal-characteristics.pdf`](13-section-10-electrical-and-thermal-characteristics.pdf) page 18 for the original scan).

The three-wire arbitration handshake, seen from the signals rather than from the bus: `BR` asserts, `BG` follows, the alternate master acknowledges with `BGACK` and the strobes go high impedance. This is the one figure in the section that draws `CLK` at the bottom instead of the top, which is reproduced here. It is also the only one that shows the grant being taken away and given again — that second `BG` pulse is what specification 39 bounds.

![Figure 10-7. Bus Arbitration Timing](figure-10-07-bus-arbitration.svg)

## Specifications marked on this figure

<!-- BEGIN TABLE from=ac-electrical-specifications.csv table=bus-arbitration grades=m68000 nums=33|34|35|36|37|37A|38|39|46 -->
| Num. | Characteristic | Unit | 8 MHz<sup>&ast;</sup> | 10 MHz<sup>&ast;</sup> | 12.5 MHz<sup>&ast;</sup> | 16.67 MHz 12F | 16 MHz | 20 MHz<sup>&ast;&ast;</sup> |
|:-:|---|:-:|--:|--:|--:|--:|--:|--:|
| 33 | Clock High to BG Asserted | ns | ≤ 62 | ≤ 50 | ≤ 40 | 0&nbsp;–&nbsp;40 | 0&nbsp;–&nbsp;30 | 0&nbsp;–&nbsp;25 |
| 34 | Clock High to BG Negated | ns | ≤ 62 | ≤ 50 | ≤ 40 | 0&nbsp;–&nbsp;40 | 0&nbsp;–&nbsp;30 | 0&nbsp;–&nbsp;25 |
| 35 | BR Asserted to BG Asserted | Clks | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 |
| 36<sup>1</sup> | BR Negated to BG Negated | Clks | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 |
| 37 | BGACK Asserted to BG Negated | Clks | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 | 1.5&nbsp;–&nbsp;3.5 |
| 37A<sup>2</sup> | BGACK Asserted to BR Negated | Clks/ns | 20&nbsp;–&nbsp;1.5 | 20&nbsp;–&nbsp;1.5 | 20&nbsp;–&nbsp;1.5 | 10&nbsp;–&nbsp;1.5 | 10&nbsp;–&nbsp;1.5 | 10&nbsp;–&nbsp;1.5 |
| 38 | BG Asserted to Control, Address, Data Bus High Impedance (AS Negated) | ns | ≤ 80 | ≤ 70 | ≤ 60 | ≤ 50 | ≤ 50 | ≤ 42 |
| 39 | BG Width Negated | Clks | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 |
| 46 | BGACK Width Low | Clks | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 | ≥ 1.5 |

- **&ast;** These specifications represent an improvement over previously published specifications for the 8-, 10-, and 12.5-MHz MC68000 and are valid only for product bearing date codes of 8827 and later.
- **&ast;&ast;** Applies only to the MC68HC000 and MC68HC001.
- **1** Setup time for the synchronous inputs BGACK, IPL0-IPL2, and VPA guarantees their recognition at the next falling edge of the clock.
- **2** BR need fall at this time only in order to insure being recognized at the end of the bus cycle.
<!-- END TABLE -->

A range `a – b` is min–max; `≤ b` is a maximum with no minimum specified; `≥ a`
is a minimum with no maximum; `—` is not specified at that grade. Superscripts
are the source table's own footnotes; the ones below the table are that
table's, and only the ones these rows actually reference are printed. Test
conditions and the source page of every row are in
[`ac-electrical-specifications.csv`](ac-electrical-specifications.csv), and
every footnote of all seven tables — including the ones no figure references —
is in [`ac-table-notes.csv`](ac-table-notes.csv).

The source's note: "Setup time to the clock (#47) for the asynchronous inputs
BERR, BGACK, BR, DTACK, IPL2-IPL0, and VPA guarantees their recognition at the
next falling edge of the clock."

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
python3 make-figure-svg.py 7      # redraw this figure
python3 make-figure-tables.py         # refresh the table above from the CSV
```
