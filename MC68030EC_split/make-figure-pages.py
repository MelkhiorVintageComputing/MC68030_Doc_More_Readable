#!/usr/bin/env python3
"""Write the figure-NN-*.md pages for the redrawn bus-cycle figures.

The specification table in each page is left as an empty managed block; run
make-figure-tables.py afterwards to fill it from the CSVs.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

COMMON = """
## About this redrawing

The waveforms were transcribed from the 300 dpi scan of the source page: the state
boundaries printed in the figure were located mechanically, and each signal's
transitions measured against that grid. Callout anchors follow what the
corresponding specification actually measures, per its description in
[`ac-electrical-specifications.csv`](ac-electrical-specifications.csv).

**Horizontal placement is schematic — and so is the original's.** The source figure
carries no time axis, its edge ramps are grossly exaggerated, and nothing in it is
to scale. Read the *ordering* and the *anchor points* from the picture; read the
*numbers* from the table. Overbars are lost in the redrawing: `AS`, `DS`, `ECS`,
`DSACKx` and the rest are active low.

Rendered as a plain SVG referenced as an image, which is the only diagram format
that survives GitHub's markdown pipeline — GitHub supports no waveform syntax
(Mermaid has none) and strips inline `<svg>`. The figure adapts to light and dark
themes.

## Regenerating

```sh
python3 make-figure-svg.py {num}      # redraw this figure
python3 make-figure-tables.py         # refresh the table below from the CSV
```
"""

FIGS = [
    dict(num=3, slug="figure-03-asynchronous-read-cycle",
         title="Figure 3 — Asynchronous Read Cycle Timing Diagram",
         pdf=13, printed=11, part=2,
         intro="A complete asynchronous read, states **S0** through **S5** — three clock "
               "periods, since each bus state is one half cycle. The address, function "
               "codes and size are driven in S0 alongside `ECS`/`OCS`; `AS` and `DS` "
               "assert in S1; `DBEN` follows in S2; the slave returns `DSACK0`/`DSACK1` "
               "and data is latched at the end of S4; everything negates in S5.",
         nums="6|6A|6B|8|9|9A|10|10A|11|12|12A|13|14|17|18|20|21|27|27A|28|29|29A|31|31A|"
              "40|41|45|46|47A|47B|48|60|61"),
    dict(num=4, slug="figure-04-asynchronous-write-cycle",
         title="Figure 4 — Asynchronous Write Cycle Timing Diagram",
         pdf=14, printed=12, part=2,
         intro="The write counterpart of Figure 3. The visible differences: `R/W` is "
               "driven **low** through the cycle, `DS` asserts a full state later than "
               "`AS` (specification 9B measures that gap, and has no read-cycle "
               "equivalent), and the processor drives `D0-D31` from S2 rather than "
               "sampling it. `CIOUT` replaces the read figure's input signals.",
         nums="6|6A|8|9|9B|10|10A|10B|11|12|12A|13|14|14A|15|15A|17|20|22|23|25|25A|26|"
              "27A|28|31A|42|43|44|45|46|48|53|55"),
    dict(num=5, slug="figure-05-synchronous-read-cycle",
         title="Figure 5 — Synchronous Read Cycle Timing Diagram",
         pdf=15, printed=13, part=2,
         intro="A synchronous read: two clock periods (**S0**–**S3**) instead of three, "
               "terminated by `STERM` rather than `DSACK0`/`DSACK1`, which stay negated "
               "throughout. The beginning of the following cycle is shown at the right, "
               "which is why the state labels restart at S0. `CBREQ`/`CBACK` and `CIIN` "
               "carry the burst and cache-inhibit handshake.",
         nums="6|6A|8|9|12|12A|14B|18|27|30|30A|40|41|45A|46A|60|61"),
    dict(num=6, slug="figure-06-synchronous-write-cycle",
         title="Figure 6 — Synchronous Write Cycle Timing Diagram",
         pdf=16, printed=14, part=2,
         intro="The write counterpart of Figure 5, again two clock periods terminated by "
               "`STERM`. `BERR` and `HALT` appear here where the read figure shows the "
               "cache handshake, and specification 28A — the synchronous hold time — is "
               "marked on both of them.",
         nums="6|6A|8|9|12|12A|14B|18|20|23|24|27A|28A|42|43|45A|46A|53|60|61"),
    dict(num=7, slug="figure-07-bus-arbitration",
         title="Figure 7 — Bus Arbitration Timing Diagram",
         pdf=17, printed=15, part=2,
         intro="An alternate bus master taking the bus. `BR` is asserted during the "
               "cycle, the processor answers with `BG`, and once the current cycle "
               "finishes it releases the bus: the address, data, function code, size and "
               "the control strobes all go to **high impedance**, drawn here as a "
               "mid-rail line. `BGACK` then asserts and `BG` is negated.",
         nums="7|16|33|34|35|37|39|39A"),
    dict(num=8, slug="figure-08-other-signal-timings",
         title="Figure 8 — Other Signal Timings",
         pdf=18, printed=16, part=2,
         intro="The signals that do not belong to a bus cycle: the interrupt-pending "
               "output `IPEND`, the `MMUDIS` and `CDIS` disable inputs, and the `STATUS` "
               "and `REFILL` pipeline outputs. The original uses a drafting break to show "
               "that arbitrary time passes between assertion and negation; that break is "
               "reproduced here.",
         nums="6|8|47A|62|63"),
]

PAGE = """# {title}

Redrawn from **Figure {num}** of `MC68030EC/D` Rev. 1 (PDF page {pdf}, printed page {printed} —
see [`06-timing-diagrams.pdf`](06-timing-diagrams.pdf) page {part} for the original scan).

{intro}

![{title}]({slug}.svg)

## Specifications marked on this figure

<!-- BEGIN TABLE from=ac-electrical-specifications.csv table=read-write nums={nums} -->
<!-- END TABLE -->

A range `a–b` is min–max; `≤ b` is a maximum with no minimum specified; `≥ a` is a
minimum with no maximum. Full descriptions, footnotes and the other speed-grade
columns are in [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv).
"""


def main():
    for f in FIGS:
        p = os.path.join(HERE, f["slug"] + ".md")
        open(p, "w").write(PAGE.format(**f) + COMMON.format(**f))
        print("wrote %s.md" % f["slug"])


if __name__ == "__main__":
    main()
