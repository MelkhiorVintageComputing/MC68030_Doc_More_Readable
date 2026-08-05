#!/usr/bin/env python3
"""Write the figure-12-N-*.md pages for the redrawn bus-cycle figures.

The specification table in each page is left as an empty managed block; run
make-figure-tables.py afterwards to fill it from the CSVs.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

COMMON = """
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

**Horizontal placement is schematic — and so is the original's.** {axis} Read the
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
python3 make-figure-svg.py {num}      # redraw this figure
python3 make-figure-tables.py         # refresh the table above from the CSV
```
"""

NO_CLOCK = ("The source figure carries **no clock and no state ruler at all** — an "
            "asynchronous cycle has no fixed length — so the horizontal axis here is "
            "a bare schematic timeline with no unit.")
CLOCKED = ("The source figure does carry a clock and the printed S0-S5 ruler, "
           "reproduced here; but its edge ramps are exaggerated and the spacing "
           "within a state is arbitrary.")

FIGS = [
    dict(num=2, slug="figure-12-2-asynchronous-read-cycle",
         title="Figure 12-2 — Asynchronous Read Cycle Timing Diagram",
         foldout=1, axis=NO_CLOCK,
         intro="A complete asynchronous read of a coprocessor interface register. The "
               "address, `R/W` and `CS` are driven first, then `AS` and `DS` assert; "
               "`START` — the logical start-of-access condition — goes true; the FPCP "
               "answers with `DSACK1` and `DSACK0` and drives `D0-D31`; the strobes "
               "negate and the data bus is released.",
         nums="6|6A|7|7A|8|8A|9|9A|10|10A|11|11A|13|13A|14|15|16|19|19A|20|21|22"),
    dict(num=3, slug="figure-12-3-asynchronous-write-cycle",
         title="Figure 12-3 — Asynchronous Write Cycle Timing Diagram",
         foldout=2, axis=NO_CLOCK,
         intro="The write counterpart of Figure 12-2. The visible differences: `R/W` is "
               "driven **low**, the main processor drives `D0-D31` rather than sampling "
               "it, and `DS` asserts much later than `AS` — late enough that the source "
               "gives the write case its own specifications 6B, 8B and 10B, and measures "
               "the asserted width of `DS` as specification 12. Specifications 14, 15, "
               "16 and 20, which are all about data the FPCP drives, do not appear.",
         nums="6|6B|7|7A|8|8B|9|9A|10|10B|11|11A|12|13|13A|17|18|19|19A|21|22"),
    dict(num=4, slug="figure-12-4-synchronous-read-cycle",
         title="Figure 12-4 — Synchronous Read Cycle Timing Diagram",
         foldout=3, axis=CLOCKED,
         intro="A synchronous read — which happens only when the save or response CIR is "
               "read (footnote 3). Here the FPCP times its response from `CLK` rather "
               "than from the strobes, so the figure adds the clock-referenced "
               "specifications 23, 24 and 26 and the two-term specifications 25 and 27. "
               "Four wait states are shown between S2 and S3; the beginning of the "
               "following cycle appears at the right.",
         nums="6|6A|7|7A|8|8A|9|9A|10|10A|11|11A|13|13A|15|16|19A|20|21|22|23|24|25|26|27"),
]

PAGE = """# {title}

Redrawn from **Figure 12-{num}** of the MC68881/MC68882 User's Manual (PDF page 405,
printed Foldout-{foldout} — see [`21-timing-diagram-foldouts.pdf`](21-timing-diagram-foldouts.pdf)
for the original scan, which carries all three bus-cycle figures side by side on one sheet).

{intro}

![{title}]({slug}.svg)

## Specifications marked on this figure

<!-- BEGIN TABLE from=ac-electrical-specifications.csv table=read-write nums={nums} -->
<!-- END TABLE -->

The figures label these with a lowercase suffix — `6a` on the drawing is **6A** in the
table. A range `a – b` is min–max; `≤ b` is a maximum with no minimum specified; `≥ a`
is a minimum with no maximum; `+ n clk` is a clock-period term added to the nanosecond
figure. Full descriptions, footnotes and the source page of every row are in
[`ac-electrical-specifications.csv`](ac-electrical-specifications.csv).
"""


def main():
    for f in FIGS:
        p = os.path.join(HERE, f["slug"] + ".md")
        open(p, "w").write(PAGE.format(**f) + COMMON.format(**f))
        print("wrote %s.md" % f["slug"])


if __name__ == "__main__":
    main()
