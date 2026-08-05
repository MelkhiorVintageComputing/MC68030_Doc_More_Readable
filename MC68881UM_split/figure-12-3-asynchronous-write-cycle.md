# Figure 12-3 — Asynchronous Write Cycle Timing Diagram

Redrawn from **Figure 12-3** of the MC68881/MC68882 User's Manual (PDF page 405,
printed Foldout-2 — see [`21-timing-diagram-foldouts.pdf`](21-timing-diagram-foldouts.pdf)
for the original scan, which carries all three bus-cycle figures side by side on one sheet).

The write counterpart of Figure 12-2. The visible differences: `R/W` is driven **low**, the main processor drives `D0-D31` rather than sampling it, and `DS` asserts much later than `AS` — late enough that the source gives the write case its own specifications 6B, 8B and 10B, and measures the asserted width of `DS` as specification 12. Specifications 14, 15, 16 and 20, which are all about data the FPCP drives, do not appear.

![Figure 12-3 — Asynchronous Write Cycle Timing Diagram](figure-12-3-asynchronous-write-cycle.svg)

## Specifications marked on this figure

<!-- BEGIN TABLE from=ac-electrical-specifications.csv table=read-write nums=6|6B|7|7A|8|8B|9|9A|10|10B|11|11A|12|13|13A|17|18|19|19A|21|22 -->
| Num. | Characteristic | Unit | 16.67 MHz | 20 MHz | 25 MHz | 33.33 MHz |
|:-:|---|:-:|--:|--:|--:|--:|
| 6 | Address Valid to AS Asserted | ns | ≥ 15 | ≥ 10 | ≥ 5 | ≥ 5 |
| 6B | Address Valid to DS Asserted (Write) | ns | ≥ 50 | ≥ 50 | ≥ 35 | ≥ 26 |
| 7 | AS Negated to Address Invalid | ns | ≥ 10 | ≥ 10 | ≥ 5 | ≥ 5 |
| 7A | DS Negated to Address Invalid | ns | ≥ 10 | ≥ 10 | ≥ 5 | ≥ 5 |
| 8 | CS Negated to AS Asserted | ns | ≥ 0 | ≥ 0 | ≥ 0 | ≥ 0 |
| 8B | CS Asserted to DS Asserted (Write) | ns | ≥ 30 | ≥ 25 | ≥ 20 | ≥ 15 |
| 9 | AS Negated to CS Negated | ns | ≥ 10 | ≥ 10 | ≥ 5 | ≥ 5 |
| 9A | DS Negated to CS Negated | ns | ≥ 10 | ≥ 10 | ≥ 5 | ≥ 5 |
| 10 | R/W High to AS Asserted (Read) | ns | ≥ 15 | ≥ 10 | ≥ 5 | ≥ 5 |
| 10B | R/W Low to DS Asserted (Write) | ns | ≥ 35 | ≥ 30 | ≥ 25 | ≥ 25 |
| 11 | AS Negated to R/W Low (Read) or AS Negated to R/W High (Write) | ns | ≥ 10 | ≥ 10 | ≥ 5 | ≥ 5 |
| 11A | DS Negated to R/W Low (Read) or DS Negated to R/W High (Write) | ns | ≥ 10 | ≥ 10 | ≥ 5 | ≥ 5 |
| 12 | DS Width Asserted (Write) | ns | ≥ 40 | ≥ 38 | ≥ 30 | ≥ 23 |
| 13 | DS Width Negated | ns | ≥ 40 | ≥ 38 | ≥ 30 | ≥ 23 |
| 13A | DS Negated to AS Asserted | ns | ≥ 30 | ≥ 30 | ≥ 25 | ≥ 18 |
| 17 | Data-In Valid to DS Asserted (Write) | ns | ≥ 15 | ≥ 10 | ≥ 5 | ≥ 5 |
| 18 | DS Negated to Data-In Invalid (Write) | ns | ≥ 15 | ≥ 10 | ≥ 5 | ≥ 5 |
| 19 | START True to DSACK0 and DSACK1 Asserted | ns | ≤ 50 | ≤ 35 | ≤ 25 | ≤ 20 |
| 19A | DSACK0 Asserted to DSACK1 Asserted (Skew) | ns | -15&nbsp;–&nbsp;15 | -10&nbsp;–&nbsp;10 | -10&nbsp;–&nbsp;10 | ≤ 5 |
| 21 | START False to DSACK0 and DSACK1 Negated | ns | ≤ 50 | ≤ 30 | ≤ 30 | ≤ 20 |
| 22 | START False to DSACK0 and DSACK1 High Impedance | ns | ≤ 70 | ≤ 40 | ≤ 40 | ≤ 30 |
<!-- END TABLE -->

The figures label these with a lowercase suffix — `6a` on the drawing is **6A** in the
table. A range `a – b` is min–max; `≤ b` is a maximum with no minimum specified; `≥ a`
is a minimum with no maximum; `+ n clk` is a clock-period term added to the nanosecond
figure. Full descriptions, footnotes and the source page of every row are in
[`ac-electrical-specifications.csv`](ac-electrical-specifications.csv).

## About this redrawing

Transcribed from a 300 dpi rendering of the foldout sheet. Callout anchors follow
what each specification actually measures, per its description in
[`ac-electrical-specifications.csv`](ac-electrical-specifications.csv).

**Where the figure and the table disagree about 11 and 11A, this redrawing follows
the table.** All three printed foldout figures put the label `11a` on the dimension
that starts at `AS` negating and `11` on the one that starts at `DS` negating — the
reverse of the specification table, which defines **11** as *AS Negated to R/W* and
**11A** as *DS Negated to R/W*. The two entries carry identical limits at every
speed grade, so nothing numerical turns on it.

**Horizontal placement is schematic — and so is the original's.** The source figure carries **no clock and no state ruler at all** — an asynchronous cycle has no fixed length — so the horizontal axis here is a bare schematic timeline with no unit. Read the
*ordering* and the *anchor points* from the picture; read the *numbers* from the
table. Overbars are lost in the redrawing: `AS`, `DS`, `CS`, `DSACKx` and `START`
are all active low.

The dashed edge on `CS` and `START` is the source's: `CS` may legitimately change
at either the solid or the dashed instant, which is why specifications 8 and 8A are
marked twice, once on each side of the strobe assertion. `START` is not a pin — it
is the logical condition `CS + AS + R/W·DS` (footnote 8), drawn as a signal for
clarity.

`DSACK0` and `DSACK1` are shown converging to a mid-rail line once released to high
impedance; the original draws the pull-up's decay instead.

Rendered as a plain SVG referenced as an image, which is the only diagram format
that survives GitHub's markdown pipeline — GitHub supports no waveform syntax
(Mermaid has none) and strips inline `<svg>`. The figure adapts to light and dark
themes.

## Regenerating

```sh
python3 make-figure-svg.py 3      # redraw this figure
python3 make-figure-tables.py         # refresh the table above from the CSV
```
