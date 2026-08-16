#!/usr/bin/env python3
"""Write the figure-*.md pages for the redrawn Section 10 figures.

The specification table in each page is left as an empty managed block; run
make-figure-tables.py afterwards to fill it from the CSVs.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PART = "13-section-10-electrical-and-thermal-characteristics.pdf"

RULER = ("The horizontal axis is the source's own bus-state ruler, recovered "
         "by measurement: on page 10-13 the printed S0-S7 labels sit 89 px "
         "apart at 300 dpi and each is centred on a clock plateau, so the "
         "state boundaries fall halfway between labels. Every edge below is "
         "drawn at the time the source draws it, delays included.")

NORULER = ("The source figure carries no state ruler and compresses its "
           "middle with a drafting break, so it has no horizontal scale to "
           "recover. This redrawing runs the whole sequence at one scale "
           "instead, at event times chosen so that **every specification the "
           "figure marks holds at once** — the arithmetic is in the "
           "`ARBITRATION` block of `make-figure-svg.py`.")

COMMON = """
## About this redrawing

{ruler}

**Callout anchors follow what each specification measures**, per its
description in [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv),
rather than the pixel position of the arrowhead on the scan. Where the two
disagree the CSV wins, because the CSV is where the numbers live.

{overbar}Rendered as a plain SVG referenced as an image, which is the only diagram
format that survives GitHub's markdown pipeline — GitHub supports no waveform
syntax (Mermaid has none) and strips inline `<svg>`. The figure adapts to
light and dark themes.

## Regenerating

{regen}
"""

OVERBAR = """Overbars are lost in the redrawing: `AS`, `DS`, `UDS`, `LDS`, `DTACK`, `BERR`,
`BR`, `BG`, `BGACK`, `HALT`, `RESET`, `VMA` and `VPA` are all active low.
A signal drawn on a mid-rail line is not being driven at all.

"""

REGEN_GEN = """```sh
python3 make-figure-svg.py {num}      # redraw this figure
python3 make-figure-tables.py         # refresh the table above from the CSV
```"""

REGEN_HAND = """`{slug}.svg` is hand-authored rather than generated: it is an
annotation figure, not a bus cycle, and the shared drawing engine
(`timingsvg.py`) has no vocabulary for threshold crossings and drive levels.
Edit the SVG directly. The table{s} above {v} generated:

```sh
python3 make-figure-tables.py
```"""

REGEN_NONE = """`{slug}.svg` is hand-authored rather than generated: it is an
annotation figure, not a bus cycle, and the shared drawing engine
(`timingsvg.py`) has no vocabulary for threshold crossings and drive levels.
Edit the SVG directly. Nothing on this page is generated from the CSVs — the
figure marks no numbered specification."""

SPEC32 = """
Specification 32 is the input transition time — the ramp on `HALT`/`RESET`
itself. The engine draws every edge with the same short ramp, so there is no
drawn ramp to measure, so the two 32 callouts are given a visible width
centred on the transition instead.
"""

RW_NUMS = ("6|6A|7|8|9|11|11A|12|13|14|15|17|18|27|28|29|29A|30|31|32|47|48|56")
EC_RW_NUMS = ("6|6A|7|8|9|11|11A|12|13|14|15|17|18|27|28|29|30|31|32|47|48|56")
WR_NUMS = ("6|6A|7|8|9|11|11A|12|13|14|14A|15|17|18|20|20A|21|21A|22|23|25|26|"
           "28|30|32|47|48|53|55|56")
EC_WR_NUMS = WR_NUMS

FIGS = [
    dict(num=2, slug="figure-10-02-drive-levels-and-test-points", page=157,
         printed="10-6", sheet=6, ruler=False, generated=False, table=None,
         title="Figure 10-2. Drive Levels and Test Points for AC Specifications",
         intro="Not a bus cycle but the convention the rest of the section is "
               "written in: where an output delay is measured from, where an "
               "input setup time is measured to, and what voltage the tester "
               "drives and senses at.",
         notes="""
| | Legend | |
|:-:|---|---|
| Ⓐ | Maximum output delay specification | clock 1.5 V to the new output valid |
| Ⓑ | Minimum output hold time | clock 1.5 V to the old output going invalid |
| Ⓒ | Minimum input setup time specification | input valid to clock 1.5 V |
| Ⓓ | Minimum input hold time specification | clock 1.5 V to input invalid |
| Ⓔ | Mode select setup time to RESET negated | |
| Ⓕ | Mode select hold time from RESET negated | |

The source's notes: output timing (1) applies to every parameter specified
relative to the rising edge of the clock, input timing (2) likewise, and the
reset timing (3) to every parameter specified relative to the negation of
`RESET`.

**Two of the signal names in this figure do not belong to this processor.**
The clock is labelled `BCLK` and the reset input `RSTI`, which are MC68040-era
names; everywhere else in the manual they are `CLK` and `RESET`. The figure
was evidently lifted from another book. The bottom row, the mode-select input,
carries no label at all in the source — it is identified here from legend
items E and F.
"""),
    dict(num=3, slug="figure-10-03-clock-input-timing", page=160, printed="10-9",
         sheet=9, ruler=False, generated=False,
         title="Figure 10-3. Clock Input Timing Diagram",
         intro="The clock input, with the two thresholds every other figure in "
               "the section is referenced to. Specifications 2 and 3 share one "
               "table row, as do 4 and 5.",
         table="clock", grades="m68000", nums="|1|2,_3|4,_5",
         notes="""
| | Measurement | Taken between |
|:-:|---|---|
| ① | Cycle time | the 2.0 V point of one falling edge and the 2.0 V point of the next |
| ② | Clock pulse width, low | the 0.8 V point of a falling edge and the 0.8 V point of the following rising edge |
| ③ | Clock pulse width, high | the 2.0 V point of a rising edge and the 2.0 V point of the following falling edge |
| ④ | Rise time | the 0.8 V and 2.0 V points of a rising edge |
| ⑤ | Fall time | the 2.0 V and 0.8 V points of a falling edge |

④ is the **rise** time and ⑤ the **fall** time, which is the same way round as
the MC68030 data sheet and the reverse of the MC68881/MC68882 manual. The
table gives one entry, "4, 5 Clock Rise and Fall Times", so the two share a
limit and nothing numerical turns on it.

The MC68008 has its own clock table with its own, slower limits:

<!-- BEGIN TABLE from=ac-electrical-specifications.csv table=clock-mc68008 grades=mc68008 -->
<!-- END TABLE -->

Sanity check on the numbers. A whole period must hold one high pulse and one
low pulse, so *minimum* pulse width + *maximum* pulse width can never exceed
the *maximum* cycle time. Every grade passes: 55 + 125 = 180 ≤ 250,
45 + 125 = 170 ≤ 250, 35 + 125 = 160 ≤ 250, 27 + 62.5 = 89.5 ≤ 125,
21 + 62.5 = 83.5 ≤ 125. Unlike the MC68881/MC68882 manual, this one has no
impossible corner in its clock table.
"""),
    dict(num=4, slug="figure-10-04-read-cycle", page=164, printed="10-13",
         sheet=13, ruler=True,
         title="Figure 10-4. Read Cycle Timing Diagram",
         intro="A complete asynchronous read. The function code and address go "
               "out during S0 and S1, `AS` and the data strobes assert in S2, "
               "the slave answers with `DTACK`, the data is latched on the "
               "falling edge of S6 and the strobes negate in S7. The three "
               "rows at the bottom show what else the processor is sampling "
               "while that happens.",
         table="read-write", grades="m68000", nums=RW_NUMS,
         notes="""
Specification 48 is drawn between `BERR` asserting and `DTACK` asserting; if
specification 47 is met for both of them, note 3 of the table says 48 may be
ignored.
""" + SPEC32),
    dict(num=5, slug="figure-10-05-write-cycle", page=165, printed="10-14",
         sheet=14, ruler=True,
         title="Figure 10-5. Write Cycle Timing Diagram",
         intro="The write counterpart of Figure 10-4. `R/W` is driven high in "
               "S0 and back low in S2; the data strobes wait until S4, two "
               "states after `AS`, which is what specification 14A measures; "
               "and the processor drives `D0-D15` from S3 instead of sampling "
               "it. The address bus is labelled A23-A1 here because on a write "
               "it is `UDS` and `LDS`, not A0, that pick the byte.",
         table="read-write", grades="m68000", nums=WR_NUMS,
         notes="""
Note 2 of the source figure is worth keeping in mind: "Because of loading
variations, R/W may be valid after AS even though both are initiated by the
rising edge of S2 (specification #20A)."
""" + SPEC32),
    dict(num=6, slug="figure-10-06-m6800-peripheral", page=167, printed="10-16",
         sheet=16, ruler=False,
         title="Figure 10-6. MC68000 to M6800 Peripheral Timing Diagram (Best Case)",
         intro="An M6800 peripheral cycle. `E` is the M6800 enable clock — six "
               "clock periods low, four high, free-running and unrelated to "
               "the bus cycle — so the processor inserts wait states after S4 "
               "until `VPA` can be recognised in phase with it. The source "
               "draws thirteen; the cycle length depends entirely on where "
               "`VPA` lands relative to `E`.",
         table="m6800-peripheral", grades="m68000",
         nums="12|18|20|23|27|29|40|41|42|43|44|45|47|49|50|51|54",
         notes="""
The source's note: "This timing diagram is included for those who wish to
design their own circuit to generate VMA. It shows the best case possible
attainable."

The horizontal scale here is the redrawing's own — the wait states make the
cycle length a function of the `E` phase, not of the specifications, so there
is nothing to measure. Read the ordering and the anchor points from the
picture and the numbers from the table.
"""),
    dict(num=7, slug="figure-10-07-bus-arbitration", page=169, printed="10-18",
         sheet=18, ruler=None,
         title="Figure 10-7. Bus Arbitration Timing",
         intro="The three-wire arbitration handshake, seen from the signals "
               "rather than from the bus: `BR` asserts, `BG` follows, the "
               "alternate master acknowledges with `BGACK` and the strobes go "
               "high impedance. This is the one figure in the section that "
               "draws `CLK` at the bottom instead of the top, which is "
               "reproduced here. It is also the only one that shows the grant "
               "being taken away and given again — that second `BG` pulse is "
               "what specification 39 bounds.",
         table="bus-arbitration", grades="m68000",
         nums="33|34|35|36|37|37A|38|39|46",
         notes="""
The source's note: "Setup time to the clock (#47) for the asynchronous inputs
BERR, BGACK, BR, DTACK, IPL2-IPL0, and VPA guarantees their recognition at the
next falling edge of the clock."
"""),
    dict(num=8, slug="figure-10-08-bus-arbitration", page=170, printed="10-19",
         sheet=19, ruler=None,
         title="Figure 10-8. Bus Arbitration Timing",
         intro="The same handshake as Figure 10-7 with the whole bus shown. "
               "`BGACK` applies only to the 52-pin MC68008 and to the "
               "processors that have the pin; the 48-pin MC68008 arbitrates "
               "with two wires. **This figure carries exactly the same caption "
               "as Figure 10-7** — see the README.",
         table="bus-arbitration", grades="m68000",
         nums="33|34|35|36|37|37A|38|46|47|57|57A",
         notes="""
The source's note: "Waveform measurements for all inputs and outputs are
specified at: logic high 2.0 V, logic low = 0.8 V. 1. MC68008 52-Pin Version
only."
"""),
    dict(num=9, slug="figure-10-09-bus-arbitration-idle", page=171, printed="10-20",
         sheet=20, ruler=None,
         title="Figure 10-9. Bus Arbitration Timing — Idle Bus Case",
         intro="Arbitration arriving while the bus is idle: the strobes are "
               "already negated, so they are simply released. In the source "
               "this drawing is all but identical to Figure 10-8; the "
               "difference is in the caption, not the waveforms.",
         table="bus-arbitration", grades="m68000",
         nums="33|34|35|36|37|37A|38|46|47|57|57A",
         notes=""),
    dict(num=10, slug="figure-10-10-bus-arbitration-active", page=172,
         printed="10-21", sheet=21, ruler=None,
         title="Figure 10-10. Bus Arbitration Timing — Active Bus Case",
         intro="Arbitration arriving mid-cycle. The processor finishes the "
               "cycle first — the strobes negate — and only then releases the "
               "bus, which is why this figure marks specifications 7 and 16 "
               "(clock high to high impedance) where the others mark 38 (BG "
               "asserted to high impedance).",
         table="bus-arbitration", grades="m68000",
         nums="7|16|33|34|35|36|37|37A|46|47|57|57A",
         notes=""),
    dict(num=11, slug="figure-10-11-bus-arbitration-multiple", page=173,
         printed="10-22", sheet=22, ruler=None,
         title="Figure 10-11. Bus Arbitration Timing — Multiple Bus Request",
         intro="Two alternate masters in succession. `BR` stays asserted "
               "across both grants — that is how the processor is told someone "
               "else is still waiting — and is negated only before the last "
               "one ends. `BG` is dropped between grants, and specification 39 "
               "is the minimum width of that gap.",
         table="bus-arbitration", grades="m68000",
         nums="33|35|36|37|38|39|46|47|57A|58",
         notes=""),
    dict(num=12, slug="figure-10-12-mc68ec000-read-cycle", page=177,
         printed="10-26", sheet=26, ruler=True,
         title="Figure 10-12. MC68EC000 Read Cycle Timing Diagram",
         intro="The MC68EC000 read cycle. Structurally identical to Figure "
               "10-4; the limits are the MC68EC000's own, and the part has "
               "`AVEC` where the MC68000 has `VPA`.",
         table="mc68ec000-read-write", grades="mc68ec000", nums=EC_RW_NUMS,
         notes=SPEC32),
    dict(num=13, slug="figure-10-13-mc68ec000-write-cycle", page=178,
         printed="10-27", sheet=27, ruler=True,
         title="Figure 10-13. MC68EC000 Write Cycle Timing Diagram",
         intro="The MC68EC000 write cycle, structurally identical to Figure "
               "10-5. The source labels the address bus A23-A0 here where "
               "Figure 10-5 labels it A23-A1.",
         table="mc68ec000-read-write", grades="mc68ec000", nums=EC_WR_NUMS,
         notes=SPEC32),
    dict(num=14, slug="figure-10-14-mc68ec000-bus-arbitration", page=180,
         printed="10-29", sheet=29, ruler=None,
         title="Figure 10-14. MC68EC000 Bus Arbitration Timing Diagram",
         intro="The MC68EC000 arbitrates with two wires: it has no `BGACK` "
               "pin, so the bus comes back when `BR` is negated rather than "
               "when an acknowledgement is withdrawn. It has no `VMA` either.",
         table="mc68ec000-bus-arbitration", grades="mc68ec000",
         nums="33|34|35|36|38|39|47|58|58A",
         notes=""),
]

PAGE = """# {title}

Redrawn from **Figure 10-{num}** of the M68000 8-/16-/32-Bit Microprocessors
User's Manual (PDF page {page}, printed page {printed} — see
[`{part}`]({part}) page {sheet} for the original scan).

{intro}

![{title}]({slug}.svg)
{spec}{notes}"""

SPEC = """
## Specifications marked on this figure

<!-- BEGIN TABLE from=ac-electrical-specifications.csv table={table} grades={grades} nums={nums} -->
<!-- END TABLE -->

A range `a – b` is min–max; `≤ b` is a maximum with no minimum specified; `≥ a`
is a minimum with no maximum; `—` is not specified at that grade. The
superscript on a specification number is its footnote in the source table.
Full descriptions, footnotes, test conditions and the source page of every row
are in [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv).
"""

SCHEMATIC = ("The waveform is drawn with deliberately exaggerated ramps so "
             "that the edge measurements are visible; ramp width, plateau "
             "width and the ratio between them carry no information, and nor "
             "do they in the original.")


def main():
    for f in FIGS:
        ruler = RULER if f["ruler"] else (NORULER if f["ruler"] is None
                                          else SCHEMATIC)
        spec = SPEC.format(**f) if f["table"] else ""
        rest = {k: v for k, v in f.items() if k != "ruler"}
        head = PAGE.format(part=PART, spec=spec, **rest)
        n = head.count("BEGIN TABLE")
        if f.get("generated", True):
            regen = REGEN_GEN.format(**f)
        elif n:
            regen = REGEN_HAND.format(s="s" if n > 1 else "",
                                      v="are" if n > 1 else "is", **f)
        else:
            regen = REGEN_NONE.format(**f)
        body = head + COMMON.format(
            ruler=ruler, regen=regen,
            overbar=OVERBAR if f.get("generated", True) else "", **rest)
        open(os.path.join(HERE, f["slug"] + ".md"), "w").write(body)
        print("wrote %s.md" % f["slug"])


if __name__ == "__main__":
    main()
