#!/usr/bin/env python3
"""Redraw the MC68881/MC68882 Section 12 bus-cycle figures as SVG.

Figures 12-2, 12-3 and 12-4 are printed side by side on the foldout sheet
(PDF page 405).  Times below were measured off a 300 dpi rendering of that
sheet.  Figures 12-2 and 12-3 carry no clock and no state ruler - the source
gives them no time base at all - so they are drawn on a bare schematic
timeline.  Figure 12-4 does have a clock, so its events are placed on the
printed S0..S5 grid, recovered from the clock's own period (86.25 px per bus
state on the scan).

Figure 12-1, the clock input diagram, is about the *shape* of an edge rather
than the sequence of a cycle; it is hand-authored in
figure-12-1-clock-input-timing.svg and not produced here.

    python3 make-figure-svg.py            # all figures
    python3 make-figure-svg.py 2 4        # just 12-2 and 12-4

One deliberate departure from the source: where the printed figures label the
AS-referenced dimension 11a and the DS-referenced one 11, this redrawing
follows the specification table, which defines 11 as AS-referenced and 11A as
DS-referenced.  See the figure pages and the README.
"""
import os, sys
from timingsvg import Fig

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Figures 12-2 and 12-3 share a signal set and most of their geometry.  The
# schematic timeline runs 0..12 with no meaning attached to the unit.
BARE = dict(states=12, labels=[""] * 12, grid=False, lead=0.4, trail=0.3)


def fig2():
    """Figure 12-2. Asynchronous Read Cycle Timing Diagram."""
    f = Fig("Figure 12-2. Asynchronous Read Cycle Timing Diagram", **BARE)

    ADDR, RW, AS_A, AS_N = 1.50, 1.65, 2.40, 7.55
    DS_A, DS_N, CS_A, CS_D, CS_N = 2.90, 8.15, 1.90, 3.55, 9.20
    ST_T, ST_F = 2.90, 7.80
    ACK1, ACK0, ACK_N, ACK_Z = 3.95, 4.40, 8.30, 9.40
    D_V, D_I, D_Z = 4.95, 9.40, 9.75
    ADDR_I, RW_L = 8.80, 8.95
    AS_A2, DS_A2 = 9.95, 10.45

    f.bus("A", [(0, "v"), (ADDR, "v"), (ADDR_I, "v")], label="A0-A4", lanes=2)
    f.level("RW", [(RW, 1), (RW_L, 0)], start=0, label="R/W", lanes=2)
    f.level("AS", [(AS_A, 0), (AS_N, 1), (AS_A2, 0)], label="AS", lanes=2)
    f.level("DS", [(DS_A, 0), (DS_N, 1), (DS_A2, 0)], label="DS", lanes=2)
    f.level("CS", [(CS_A, 0), (CS_N, 1)], label="CS", lanes=1)
    f.alt("CS", CS_A, CS_D)
    f.level("ST", [(ST_T, 0), (ST_F, 1)], label="START", lanes=2)
    f.alt("ST", ST_T, CS_D)
    f.level("K1", [(ACK1, 0), (ACK_N, 1)], label="DSACK1", lanes=1, z_from=ACK_Z)
    f.level("K0", [(ACK0, 0), (ACK_N, 1)], label="DSACK0", lanes=2, z_from=ACK_Z)
    f.bus("D", [(0, "z"), (D_V, "v"), (D_I, "z")], label="D0-D31", lanes=0)

    f.span("A", 0, ADDR, AS_A, "6", "outL")
    f.span("A", 0, AS_N, ADDR_I, "7", "outL")
    f.span("A", 1, ADDR, DS_A, "6a", "outR")
    f.span("A", 1, DS_N, ADDR_I, "7a", "outR")

    f.span("RW", 0, RW, AS_A, "10", "outL")
    f.span("RW", 0, AS_N, RW_L, "11", "outR")
    f.span("RW", 1, RW, DS_A, "10a", "outL")
    f.span("RW", 1, DS_N, RW_L, "11a", "outR")

    f.span("AS", 0, CS_A, AS_A, "8", "outL")
    f.span("AS", 0, DS_N, AS_A2, "13a", "in")
    f.span("AS", 1, AS_A, CS_D, "8", "outR")
    f.span("AS", 1, DS_N, DS_A2, "13", "in")

    f.span("DS", 0, CS_A, DS_A, "8a", "outL")
    f.span("DS", 0, AS_N, CS_N, "9", "in")
    f.span("DS", 1, DS_A, CS_D, "8a", "outR")
    f.span("DS", 1, DS_N, CS_N, "9a", "outR")

    f.span("CS", 0, DS_A, D_V, "14", "in")

    f.span("ST", 0, ST_T, ACK0, "19", "in")
    f.span("ST", 0, ST_F, ACK_N, "21", "outR")
    f.span("ST", 1, ST_F, ACK_Z, "22", "outR")

    f.span("K1", 0, ACK1, ACK0, "19a", "outL")

    f.span("K0", 0, ACK1, D_V, "20", "in")
    f.span("K0", 0, DS_N, D_Z, "16", "in")
    f.span("K0", 1, DS_N, D_I, "15", "in")
    return f


def fig3():
    """Figure 12-3. Asynchronous Write Cycle Timing Diagram."""
    f = Fig("Figure 12-3. Asynchronous Write Cycle Timing Diagram", **BARE)

    ADDR, RW, AS_A, AS_N = 1.15, 1.50, 2.25, 7.50
    DS_A, DS_N, CS_A, CS_D, CS_N = 5.25, 7.95, 1.65, 3.35, 9.15
    ST_T, ST_F = 2.75, 7.75
    ACK1, ACK0, ACK_N, ACK_Z = 3.80, 4.30, 8.60, 9.55
    D_V, D_I = 4.15, 9.25
    ADDR_I, RW_H = 8.80, 9.00
    AS_A2, DS_A2 = 9.90, 10.30

    f.bus("A", [(0, "v"), (ADDR, "v"), (ADDR_I, "v")], label="A0-A4", lanes=2)
    f.level("RW", [(RW, 0), (RW_H, 1)], start=1, label="R/W", lanes=2)
    f.level("AS", [(AS_A, 0), (AS_N, 1), (AS_A2, 0)], label="AS", lanes=2)
    f.level("DS", [(DS_A, 0), (DS_N, 1), (DS_A2, 0)], label="DS", lanes=2)
    f.level("CS", [(CS_A, 0), (CS_N, 1)], label="CS", lanes=1)
    f.alt("CS", CS_A, CS_D)
    f.level("ST", [(ST_T, 0), (ST_F, 1)], label="START", lanes=2)
    f.alt("ST", ST_T, CS_D)
    f.level("K1", [(ACK1, 0), (ACK_N, 1)], label="DSACK1", lanes=1, z_from=ACK_Z)
    f.level("K0", [(ACK0, 0), (ACK_N, 1)], label="DSACK0", lanes=1, z_from=ACK_Z)
    f.bus("D", [(0, "z"), (D_V, "v"), (D_I, "z")], label="D0-D31", lanes=0)

    f.span("A", 0, ADDR, AS_A, "6", "outL")
    f.span("A", 0, AS_N, ADDR_I, "7", "outL")
    f.span("A", 1, ADDR, DS_A, "6b", "in")
    f.span("A", 1, DS_N, ADDR_I, "7a", "outR")

    f.span("RW", 0, RW, AS_A, "10", "outL")
    f.span("RW", 0, AS_N, RW_H, "11", "outR")
    f.span("RW", 1, RW, DS_A, "10b", "in")
    f.span("RW", 1, DS_N, RW_H, "11a", "outR")

    f.span("AS", 0, CS_A, AS_A, "8", "outL")
    f.span("AS", 0, DS_N, AS_A2, "13a", "in")
    f.span("AS", 1, AS_A, CS_D, "8", "outR")
    f.span("AS", 1, DS_A, DS_N, "12", "in")
    f.span("AS", 1, DS_N, DS_A2, "13", "in")

    f.span("DS", 0, CS_A, DS_A, "8b", "in")
    f.span("DS", 0, AS_N, CS_N, "9", "in")
    f.span("DS", 1, DS_N, CS_N, "9a", "outR")

    f.span("ST", 0, ST_T, ACK0, "19", "in")
    f.span("ST", 0, ST_F, ACK_N, "21", "outR")
    f.span("ST", 1, ST_F, ACK_Z, "22", "outR")

    f.span("K1", 0, ACK1, ACK0, "19a", "outL")

    f.span("K0", 0, D_V, DS_A, "17", "in")
    f.span("K0", 0, DS_N, D_I, "18", "in")
    return f


def fig4():
    """Figure 12-4. Synchronous Read Cycle Timing Diagram."""
    f = Fig("Figure 12-4. Synchronous Read Cycle Timing Diagram", states=13,
            labels=["S0", "S1", "S2", "Sw", "Sw", "Sw", "Sw", "S3", "S4", "S5",
                    "", "", ""],
            lead=0.5, trail=0.2)

    ADDR, RW, AS_A, AS_N = 0.55, 0.70, 1.40, 9.57
    DS_A, DS_N, CS_A, CS_D, CS_N = 1.80, 9.97, 0.90, 2.35, 11.00
    ST_T, CLK_H, CLK_L = 1.95, 2.05, 5.00
    ACK1, ACK0, ACK_N, ACK_Z = 6.10, 6.60, 10.40, 11.50
    D_V, D_I, D_Z = 7.50, 11.20, 11.55
    ADDR_I, RW_L, ST_F = 10.55, 10.70, 9.85
    AS_A2, DS_A2 = 11.60, 12.00

    f.clock(lanes=0)
    f.bus("A", [(0, "v"), (ADDR, "v"), (ADDR_I, "v")], label="A0-A4", lanes=2)
    f.level("RW", [(RW, 1), (RW_L, 0)], start=0, label="R/W", lanes=2)
    f.level("AS", [(AS_A, 0), (AS_N, 1), (AS_A2, 0)], label="AS", lanes=2)
    f.level("DS", [(DS_A, 0), (DS_N, 1), (DS_A2, 0)], label="DS", lanes=2)
    f.level("CS", [(CS_A, 0), (CS_N, 1)], label="CS", lanes=1)
    f.alt("CS", CS_A, CS_D)
    f.level("ST", [(ST_T, 0), (ST_F, 1)], label="START", lanes=2)
    f.alt("ST", ST_T, CS_D)
    f.level("K1", [(ACK1, 0), (ACK_N, 1)], label="DSACK1", lanes=2, z_from=ACK_Z)
    f.level("K0", [(ACK0, 0), (ACK_N, 1)], label="DSACK0", lanes=2, z_from=ACK_Z)
    f.bus("D", [(0, "z"), (D_V, "v"), (D_I, "z")], label="D0-D31", lanes=0)

    f.span("A", 0, ADDR, AS_A, "6", "outL")
    f.span("A", 0, AS_N, ADDR_I, "7", "outL")
    f.span("A", 1, ADDR, DS_A, "6a", "outR")
    f.span("A", 1, DS_N, ADDR_I, "7a", "outR")

    f.span("RW", 0, RW, AS_A, "10", "outL")
    f.span("RW", 0, AS_N, RW_L, "11", "outR")
    f.span("RW", 1, RW, DS_A, "10a", "outL")
    f.span("RW", 1, DS_N, RW_L, "11a", "outR")

    f.span("AS", 0, CS_A, AS_A, "8", "outL")
    f.span("AS", 0, DS_N, AS_A2, "13a", "in")
    f.span("AS", 1, AS_A, CS_D, "8", "outR")
    f.span("AS", 1, DS_N, DS_A2, "13", "in")

    f.span("DS", 0, CS_A, DS_A, "8a", "outL")
    f.span("DS", 0, AS_N, CS_N, "9", "in")
    f.span("DS", 1, DS_A, CS_D, "8a", "outR")
    f.span("DS", 1, DS_N, CS_N, "9a", "outR")

    f.span("CS", 0, ST_T, CLK_H, "23", "outL")

    f.span("ST", 0, ACK1, ACK0, "19a", "outL")
    f.span("ST", 0, ACK1, D_V, "20", "in")
    f.span("ST", 1, ST_F, ACK_N, "21", "outR")
    f.span("ST", 1, ST_F, ACK_Z, "22", "outR")

    f.span("K1", 0, CLK_L, ACK0, "26", "in")
    f.span("K1", 1, ST_T, ACK0, "27", "in")

    f.span("K0", 0, CLK_L, D_V, "24", "in")
    f.span("K0", 0, DS_N, D_Z, "16", "in")
    f.span("K0", 1, ST_T, D_V, "25", "in")
    f.span("K0", 1, DS_N, D_I, "15", "in")
    return f


FIGURES = {
    2: (fig2, "figure-12-2-asynchronous-read-cycle"),
    3: (fig3, "figure-12-3-asynchronous-write-cycle"),
    4: (fig4, "figure-12-4-synchronous-read-cycle"),
}


def main(which):
    for n in which:
        build, slug = FIGURES[n]
        p = build().write(os.path.join(HERE, slug + ".svg"))
        print("wrote %s (%d bytes)" % (os.path.basename(p), os.path.getsize(p)))


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]] or sorted(FIGURES)
    bad = [a for a in args if a not in FIGURES]
    if bad:
        sys.exit("no such figure: %s (have %s)"
                 % (", ".join(map(str, bad)), ", ".join(map(str, sorted(FIGURES)))))
    main(args)
