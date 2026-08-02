#!/usr/bin/env python3
"""Generate the redrawn MC68030EC/D timing figures 3-8 as SVG.

Each figure transcribes the corresponding scanned page of MC68030EC/D Rev. 1.
Transition times were measured off the 300 dpi page scans against the state
grid printed in each figure, then rounded; callout anchors follow what the
corresponding specification actually measures, per the descriptions in
ac-electrical-specifications.csv.

Horizontal placement is schematic. So is the original: the source figures carry
no time axis, the edge ramps are exaggerated, and nothing in them is to scale.
Read the ordering and the callout anchors from the picture; read the numbers
from the table.

    python3 make-figure-svg.py          # write every figure
    python3 make-figure-svg.py 3 7      # only figures 3 and 7
"""
import os, sys
from timingsvg import Fig

HERE  = os.path.dirname(os.path.abspath(__file__))
ADDR  = "A0-A31, FC0-FC2,|SIZ0-SIZ1"
ASYNC = "ALL|ASYNCHRONOUS|INPUTS"
DSK   = "DSACK0/DSACK1"


# ------------------------------------------------ 3. asynchronous read cycle
def fig3():
    f = Fig("Figure 3. Asynchronous Read Cycle Timing Diagram - MC68030", states=7,
            labels=["S0", "S1", "S2", "S3", "S4", "S5", ""])
    f.clock(lanes=1)
    f.bus("A", [(0, "v"), (0.70, "v"), (6.30, "v")], label=ADDR, lanes=1)
    f.level("RMC", [(0.75, 0), (6.30, 1)], label="RMC", lanes=1)
    f.level("ECS", [(0.30, 0), (1.25, 1)], label="ECS", lanes=1)
    f.level("OCS", [(0.40, 0), (1.32, 1)], label="OCS", lanes=2)
    f.level("AS",  [(1.70, 0), (5.78, 1)], label="AS", lanes=2)
    f.level("DS",  [(1.85, 0), (5.78, 1)], label="DS", lanes=1)
    f.level("RW",  [(0.60, 1), (6.90, 0)], start=0, label="R/W", lanes=1)
    f.level("DBEN", [(0.90, 1), (2.30, 0), (5.90, 1)], start=0, label="DBEN", lanes=1)
    f.level("D0", [(2.90, 0), (6.10, 1)], label="DSACK0", lanes=1)
    f.level("D1", [(3.30, 0), (6.15, 1)], label="DSACK1", lanes=1)
    f.bus("D", [(0, "v"), (0.90, "z"), (4.20, "v"), (6.40, "z")], label="D0-D31", lanes=1)
    f.level("BERR", [(4.26, 0), (6.56, 1)], label="BERR", lanes=1)
    f.level("HALT", [(4.28, 0), (6.71, 1)], label="HALT", lanes=1)
    f.level("ASY", [(2.38, 0), (5.68, 1)], label=ASYNC, lanes=1)
    f.level("CIIN", [(3.58, 0), (4.75, 1)], label="CIIN", lanes=1)
    f.level("CBREQ", [(1.62, 0), (5.58, 1)], label="CBREQ", lanes=0)

    f.span("CLK", 0, 0.00, 0.70, "6", "outR")
    f.span("A",   0, 0.70, 1.25, "6B", "outR")
    f.span("RMC", 0, 0.30, 1.25, "10", "outL")
    f.span("RMC", 0, 1.00, 1.32, "12A", "outR")
    f.span("RMC", 0, 6.00, 6.30, "8", "outR")
    f.span("ECS", 0, 0.00, 0.40, "6A", "outL")
    f.span("ECS", 0, 0.40, 1.32, "10A", "outR")
    f.span("OCS", 0, 0.70, 1.70, "11", "outL")
    f.span("OCS", 0, 1.70, 5.78, "14", "in")
    f.span("OCS", 0, 5.78, 6.30, "13", "outR")
    f.span("OCS", 1, 1.70, 1.85, "9A", "outR")
    f.span("AS",  0, 1.00, 1.70, "9", "outL")
    f.span("AS",  0, 5.78, 5.95, "12", "outR")
    f.span("AS",  1, 0.70, 1.85, "11", "outL")
    f.span("AS",  1, 1.85, 5.78, "14", "in")
    f.span("DS",  0, 0.00, 0.60, "18", "outL")
    f.span("DS",  0, 6.00, 6.90, "20", "outR")
    f.span("RW",  0, 0.60, 1.70, "21", "outL")
    f.span("RW",  0, 0.60, 6.90, "46", "in")
    f.span("RW",  0, 5.00, 5.90, "41", "outR")
    f.span("DBEN", 0, 2.00, 2.30, "40", "outL")
    f.span("DBEN", 0, 2.30, 5.90, "45", "in")
    f.span("DBEN", 0, 5.78, 6.90, "17", "outR")
    f.span("D0", 0, 2.90, 3.30, "31A", "in")
    f.span("D0", 0, 5.78, 6.10, "28", "outR")
    f.span("D1", 0, 3.30, 4.20, "31", "outL")
    f.span("D1", 0, 5.78, 6.40, "29", "outR")
    f.span("D",  0, 4.20, 5.00, "27", "outL")
    f.span("D",  0, 5.78, 6.40, "29A", "outR")
    f.span("BERR", 0, 4.26, 5.00, "27A", "outR")
    f.span("HALT", 0, 2.38, 3.00, "47A", "outL")
    f.span("HALT", 0, 2.90, 4.26, "48", "outR")
    f.span("ASY", 0, 3.58, 4.00, "60", "outL")
    f.span("ASY", 0, 5.00, 5.68, "47B", "outR")
    f.span("CIIN", 0, 4.00, 4.75, "61", "outL")
    f.span("CIIN", 0, 5.00, 5.58, "12", "outR")
    return f


# ----------------------------------------------- 4. asynchronous write cycle
def fig4():
    f = Fig("Figure 4. Asynchronous Write Cycle Timing Diagram - MC68030", states=7,
            labels=["S0", "S1", "S2", "S3", "S4", "S5", "S0"])
    f.clock(lanes=1)
    f.bus("A", [(0, "v"), (0.66, "v"), (6.67, "v")], label=ADDR, lanes=1)
    f.level("RMC", [(0.60, 0), (6.42, 1)], label="RMC", lanes=1)
    f.level("ECS", [(0.50, 0), (1.45, 1), (6.45, 0)], label="ECS", lanes=1)
    f.level("OCS", [(0.60, 0), (1.55, 1), (6.55, 0)], label="OCS", lanes=2)
    f.level("AS",  [(1.70, 0), (6.05, 1)], label="AS", lanes=1)
    f.level("DS",  [(3.15, 0), (6.05, 1)], label="DS", lanes=2)
    f.level("RW",  [(0.60, 0), (6.77, 1)], start=1, label="R/W", lanes=1)
    f.level("DBEN", [(0.00, 1), (1.30, 0), (6.40, 1)], start=0, label="DBEN", lanes=1)
    f.level("D0", [(2.42, 0), (6.36, 1)], label="DSACK0", lanes=1)
    f.level("D1", [(2.94, 0), (6.36, 1)], label="DSACK1", lanes=1)
    f.bus("D", [(0, "z"), (2.28, "v"), (6.90, "z")], label="D0-D31", lanes=1)
    f.level("BERR", [(3.98, 0), (6.05, 1)], label="BERR", lanes=1)
    f.level("HALT", [(3.98, 0), (6.29, 1)], label="HALT", lanes=1)
    f.level("CIOUT", [(0.50, 0), (6.50, 1)], label="CIOUT", lanes=0)

    f.span("CLK", 0, 0.00, 0.66, "6", "outR")
    f.span("CLK", 0, 6.00, 6.67, "8", "outR")
    f.span("A",   0, 1.00, 1.45, "12A", "outR")
    f.span("RMC", 0, 0.50, 1.45, "10", "outL")
    f.span("ECS", 0, 0.00, 0.60, "6A", "outL")
    f.span("ECS", 0, 0.60, 1.55, "10A", "outR")
    f.span("ECS", 0, 1.55, 6.45, "10B", "in")
    f.span("OCS", 0, 0.66, 1.70, "11", "outL")
    f.span("OCS", 0, 1.70, 6.05, "14", "in")
    f.span("OCS", 0, 6.05, 6.67, "13", "outR")
    f.span("OCS", 1, 1.70, 3.15, "9B", "in")
    f.span("OCS", 1, 6.05, 6.45, "15A", "outR")
    f.span("AS",  0, 3.00, 3.15, "9", "outL")
    f.span("AS",  0, 3.15, 6.05, "14A", "in")
    f.span("AS",  0, 6.05, 6.60, "15", "outR")
    f.span("DS",  0, 0.00, 0.60, "20", "outL")
    f.span("DS",  0, 0.60, 3.15, "22", "in")
    f.span("DS",  0, 6.05, 6.20, "12", "outR")
    f.span("DS",  1, 6.05, 6.77, "17", "outR")
    f.span("RW",  0, 1.00, 1.30, "42", "outL")
    f.span("RW",  0, 0.60, 6.77, "46", "in")
    f.span("RW",  0, 6.05, 6.40, "25A", "outR")
    f.span("DBEN", 0, 0.60, 1.30, "44", "outL")
    f.span("DBEN", 0, 1.30, 6.40, "45", "in")
    f.span("DBEN", 0, 6.00, 6.40, "43", "outR")
    f.span("D0", 0, 2.42, 2.94, "31A", "in")
    f.span("D0", 0, 6.05, 6.36, "28", "outR")
    f.span("D1", 0, 2.00, 2.28, "23", "outL")
    f.span("D1", 0, 6.00, 6.30, "53", "outR")
    f.span("D",  0, 1.00, 2.28, "55", "outL")
    f.span("D",  0, 2.28, 3.15, "26", "in")
    f.span("D",  0, 6.05, 6.90, "25", "outR")
    f.span("BERR", 0, 2.94, 3.98, "48", "in")
    f.span("HALT", 0, 3.98, 5.00, "27A", "outL")
    return f


# ------------------------------------------------- 5. synchronous read cycle
SYNC_LAB = ["S0", "S1", "S2", "S3", "S0", "S1", "S2"]


def fig5():
    f = Fig("Figure 5. Synchronous Read Cycle Timing Diagram - MC68030", states=7,
            labels=SYNC_LAB)
    f.clock(lanes=0)
    f.bus("A", [(0, "v"), (0.63, "v"), (4.53, "v")], label=ADDR, lanes=1)
    f.level("RMC", [(0.56, 0), (4.70, 1)], label="RMC", lanes=1)
    f.level("ECS", [(0.41, 0), (1.57, 1), (4.53, 0), (5.70, 1)], label="ECS", lanes=1)
    f.level("OCS", [(0.50, 0), (1.66, 1), (4.62, 0), (5.80, 1)], label="OCS", lanes=1)
    f.level("AS",  [(1.74, 0), (3.35, 1), (5.86, 0)], label="AS", lanes=1)
    f.level("DS",  [(1.86, 0), (3.45, 1), (5.98, 0)], label="DS", lanes=1)
    f.level("RW",  [(0.55, 1), (4.60, 0)], start=0, label="R/W", lanes=1)
    f.level("DBEN", [(1.80, 0), (3.40, 1)], label="DBEN", lanes=1)
    f.level("CIOUT", [(0.60, 0), (4.60, 1)], label="CIOUT", lanes=1)
    f.level("CBREQ", [(1.70, 0), (3.40, 1)], label="CBREQ", lanes=1)
    f.level("DSK", [(0.30, 1)], start=0, label=DSK, lanes=1)
    f.level("STERM", [(2.20, 0), (3.30, 1)], label="STERM", lanes=1)
    f.level("CIIN", [(1.90, 0), (3.20, 1)], label="CIIN", lanes=1)
    f.level("CBACK", [(1.70, 0), (3.10, 1)], label="CBACK", lanes=1)
    f.bus("D", [(0, "z"), (2.55, "v"), (3.55, "z")], label="D0-D31", lanes=0)

    f.span("A",   0, 4.00, 4.53, "8", "outR")
    f.span("RMC", 0, 0.00, 0.56, "6", "outL")
    f.span("RMC", 0, 1.00, 1.57, "12A", "outR")
    f.span("ECS", 0, 0.00, 0.50, "6A", "outL")
    f.span("OCS", 0, 1.74, 3.35, "14B", "in")
    f.span("AS",  0, 1.00, 1.86, "9", "outR")
    f.span("DS",  0, 0.00, 0.55, "18", "outL")
    f.span("DS",  0, 0.55, 4.60, "46A", "in")
    f.span("RW",  0, 1.00, 1.80, "40", "outL")
    f.span("RW",  0, 3.00, 3.40, "41", "outR")
    f.span("DBEN", 0, 1.80, 3.40, "45A", "outR")
    f.span("CIOUT", 0, 3.00, 3.40, "12", "outR")
    f.span("DSK", 0, 2.00, 2.20, "61", "outL")
    f.span("STERM", 0, 1.90, 2.00, "60", "outL")
    f.span("CIIN", 0, 3.00, 3.55, "30A", "outR")
    f.span("CBACK", 0, 2.55, 3.00, "27", "outL")
    f.span("CBACK", 0, 3.00, 3.30, "30", "outR")
    return f


# ------------------------------------------------ 6. synchronous write cycle
def fig6():
    f = Fig("Figure 6. Synchronous Write Cycle Timing Diagram - MC68030", states=7,
            labels=SYNC_LAB)
    f.clock(lanes=0)
    f.bus("A", [(0, "v"), (0.63, "v"), (4.53, "v")], label=ADDR, lanes=1)
    f.level("RMC", [(0.56, 0), (4.70, 1)], label="RMC", lanes=1)
    f.level("ECS", [(0.41, 0), (1.57, 1), (4.53, 0), (5.70, 1)], label="ECS", lanes=1)
    f.level("OCS", [(0.50, 0), (1.66, 1), (4.62, 0), (5.80, 1)], label="OCS", lanes=1)
    f.level("AS",  [(1.74, 0), (3.90, 1), (5.86, 0)], label="AS", lanes=1)
    f.level("DS",  [(1.86, 0), (3.90, 1), (5.98, 0)], label="DS", lanes=1)
    f.level("RW",  [(0.60, 0), (4.55, 1)], start=1, label="R/W", lanes=1)
    f.level("DBEN", [(1.60, 0), (4.10, 1)], label="DBEN", lanes=1)
    f.bus("D", [(0, "z"), (2.20, "v"), (4.30, "z")], label="D0-D31", lanes=1)
    f.level("DSK", [(0.30, 1)], start=0, label=DSK, lanes=1)
    f.level("STERM", [(2.10, 0), (3.20, 1)], label="STERM", lanes=1)
    f.level("BERR", [(2.70, 0), (4.60, 1)], label="BERR", lanes=1)
    f.level("HALT", [(2.70, 0), (4.75, 1)], label="HALT", lanes=1)
    f.level("CBREQ", [(0.30, 1)], start=0, label="CBREQ", lanes=0)

    f.span("CLK", 0, 0.00, 0.63, "6", "outR") if False else None
    f.span("A",   0, 0.00, 0.63, "6", "outL")
    f.span("A",   0, 4.00, 4.53, "8", "outR")
    f.span("RMC", 0, 1.00, 1.57, "12A", "outR")
    f.span("ECS", 0, 0.00, 0.50, "6A", "outL")
    f.span("OCS", 0, 1.00, 1.86, "9", "outL")
    f.span("OCS", 0, 3.90, 4.05, "12", "outR")
    f.span("AS",  0, 1.74, 3.90, "14B", "in")
    f.span("DS",  0, 0.00, 0.60, "20", "outL")
    f.span("DS",  0, 0.60, 4.55, "46A", "in")
    f.span("DS",  0, 4.00, 4.55, "18", "outR")
    f.span("RW",  0, 1.00, 1.60, "42", "outL")
    f.span("RW",  0, 1.60, 4.10, "45A", "in")
    f.span("RW",  0, 4.00, 4.10, "43", "outR")
    f.span("DBEN", 0, 2.00, 2.20, "23", "outL")
    f.span("DBEN", 0, 4.00, 4.30, "53", "outR")
    f.span("D",   0, 3.90, 4.30, "24", "outR")
    f.span("DSK", 0, 1.90, 2.10, "60", "outL")
    f.span("STERM", 0, 2.00, 2.10, "61", "outL")
    f.span("STERM", 0, 2.70, 4.60, "28A", "in")
    f.span("BERR", 0, 2.70, 4.75, "28A", "in")
    f.span("HALT", 0, 2.10, 2.70, "27A", "outL")
    return f


# ------------------------------------------------------- 7. bus arbitration
def fig7():
    f = Fig("Figure 7. Bus Arbitration Timing Diagram - MC68030", states=10,
            labels=["S0", "S1", "S2", "S3", "S4", "S5", "", "", "", ""])
    f.clock(lanes=0)
    f.bus("A", [(0, "v"), (0.40, "v"), (5.20, "z")], label="A0-A31", lanes=0)
    f.bus("D", [(0, "v"), (0.40, "v"), (2.30, "v"), (5.20, "z")], label="D0-D31", lanes=0)
    f.bus("FC", [(0, "v"), (0.40, "v"), (5.20, "z")], label="FC0-FC2", lanes=0)
    f.bus("SZ", [(0, "v"), (0.40, "v"), (5.20, "z")], label="SIZ0-SIZ1", lanes=1)
    f.level("ECS", [(0.35, 0), (1.30, 1)], label="ECS", lanes=0)
    f.level("OCS", [(0.45, 0), (1.40, 1)], label="OCS", lanes=0)
    f.level("AS",  [(1.30, 0), (4.10, 1)], label="AS", lanes=0, z_from=5.30)
    f.level("DS",  [(1.45, 0), (4.25, 1)], label="DS", lanes=0, z_from=5.35)
    f.level("RW",  [(0.90, 1)], start=0, label="R/W", lanes=0, z_from=5.30)
    f.level("DBEN", [(0.90, 1), (2.20, 0), (4.20, 1)], start=0, label="DBEN",
            lanes=1, z_from=5.35)
    f.level("DK0", [(2.60, 0), (4.60, 1)], label="DSACK0", lanes=0)
    f.level("DK1", [(2.60, 0), (4.60, 1)], label="DSACK1", lanes=1)
    f.level("BR",  [(1.30, 0), (6.60, 1)], label="BR", lanes=1)
    f.level("BG",  [(0.20, 1), (5.90, 0), (7.30, 1)], start=0, label="BG", lanes=2)
    f.level("BGACK", [(6.20, 0), (8.10, 1)], label="BGACK", lanes=0)

    f.span("SZ",  0, 4.60, 5.20, "7", "outL")
    f.span("DBEN", 0, 4.60, 5.35, "16", "outL")
    f.span("DK1", 0, 5.40, 5.90, "33", "outR")
    f.span("BR",  0, 1.30, 5.90, "35", "in")
    f.span("BG",  0, 5.90, 7.30, "39A", "in")
    f.span("BG",  0, 7.00, 7.30, "34", "outR")
    f.span("BG",  1, 0.20, 5.90, "39", "in")
    f.span("BG",  1, 6.20, 7.30, "37", "in")
    return f


# ---------------------------------------------------- 8. other signal timings
def fig8():
    f = Fig("Figure 8. Other Signal Timings - MC68030", states=8,
            labels=[""] * 8, lead=0.6, trail=0.4)
    f.clock(lanes=1)
    f.level("IPEND", [(1.60, 0), (5.60, 1)], label="IPEND", lanes=0)
    f.level("MMUDIS", [(1.40, 0)], label="MMUDIS", lanes=1)
    f.level("CDIS", [(1.45, 0)], label="CDIS", lanes=1)
    f.level("STATUS", [(1.30, 0), (5.40, 1)], label="STATUS", lanes=1)
    f.level("REFILL", [(1.40, 0), (5.50, 1)], label="REFILL", lanes=0)

    f.span("CLK", 0, 1.00, 1.60, "6", "outR")
    f.span("CLK", 0, 5.00, 5.60, "8", "outL")
    f.span("MMUDIS", 0, 1.00, 1.45, "47A", "outR")
    f.span("STATUS", 0, 1.00, 1.40, "62", "outR")
    f.span("STATUS", 0, 5.00, 5.50, "63", "outL")
    f.brk(3.5)
    return f


FIGURES = {
    3: ("figure-03-asynchronous-read-cycle.svg", fig3),
    4: ("figure-04-asynchronous-write-cycle.svg", fig4),
    5: ("figure-05-synchronous-read-cycle.svg", fig5),
    6: ("figure-06-synchronous-write-cycle.svg", fig6),
    7: ("figure-07-bus-arbitration.svg", fig7),
    8: ("figure-08-other-signal-timings.svg", fig8),
}


def main(which):
    for n in sorted(which):
        name, build = FIGURES[n]
        build().write(os.path.join(HERE, name))
        print("wrote %s" % name)


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or sorted(FIGURES))
