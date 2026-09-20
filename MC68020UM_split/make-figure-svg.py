#!/usr/bin/env python3
"""Generate the redrawn Section 10 bus-cycle figures as SVG.

Figures 10-3, 10-4 and 10-5 of MC68020UM.pdf, redrawn so that they can be
read at any size and so that GitHub will show them: the source pages are
line art that a browser will not zoom, and markdown strips inline SVG, so a
referenced .svg file is the only form that works.

Where the numbers come from
---------------------------
The clock and the two-level signals were measured off a 300 dpi rendering of
each page. The clock gives the time base: its edges fall every 19.8 points
across all three figures, which fixes one bus state at 19.8 points and the
origin at the first falling edge, so x = 247.3 + 19.8t on Figure 10-3. Every
level transition was then read against that grid and rounded to a fiftieth of
a state.

The buses are placed rather than measured. They are drawn as two converging
rails, and the callout leaders and discs cross the same band often enough
that a crossover cannot be told from a leader mechanically; their windows
follow the source's own placement, read by eye against the state grid.

Horizontal placement is schematic in the source too - the ramps are
exaggerated and nothing is to scale. Read the ordering and the callout
anchors from the picture and the numbers from
ac-electrical-specifications.csv.

    python3 make-figure-svg.py            # write every figure
    python3 make-figure-svg.py 3 5        # only figures 10-3 and 10-5
"""
import os
import sys

from timingsvg import Fig

HERE = os.path.dirname(os.path.abspath(__file__))

ADDR = "A31-A0,|FC2-FC0,|SIZ1-SIZ0"
ASYNC = "ALL|ASYNCHRONOUS|INPUTS"

# Measured from the 300 dpi renderings, in bus states. The read and write
# cycles are drawn on the same grid and share every edge that is common to
# both; only the data bus, R/W, DS and DBEN differ.
CLK_FALL = 1.00
ADDR_VALID, ADDR_INVALID, ADDR_Z = 0.70, 6.05, 6.60
ECS_ON, ECS_OFF = 0.30, 1.25
OCS_ON, OCS_OFF = 0.35, 1.30
AS_ON, AS_NEG = 1.80, 5.70
DS_READ_ON = 1.81
DS_WRITE_ON = 2.80
RW_LOW = 0.85
DSACK0_ON, DSACK1_ON = 3.30, 3.44
DSACK_OFF = 6.05
DIN_VALID, DIN_Z = 4.30, 6.40
DOUT_VALID, DOUT_INVALID = 2.30, 6.20
DBEN_READ_ON, DBEN_READ_OFF = 2.56, 6.01
DBEN_WRITE_ON, DBEN_WRITE_OFF = 1.95, 6.01
BERR_ON, BERR_OFF = 4.35, 5.95
HALT_ON, HALT_OFF = 4.40, 6.00
ASYNC_ON, ASYNC_OFF = 2.40, 5.60

STATES = 8
LABELS = ["S0", "S1", "S2", "S3", "S4", "S5", "", ""]


# ------------------------------------------------------ 10-3. read cycle ----
def fig3():
    f = Fig("Figure 10-3. Read Cycle Timing Diagram - MC68020/MC68EC020",
            states=STATES, labels=LABELS)
    f.clock(lanes=1)
    f.bus("A", [(0, "v"), (ADDR_VALID, "v"), (ADDR_INVALID, "v"),
                (ADDR_Z, "z")], label=ADDR, lanes=1)
    f.level("ECS", [(ECS_ON, 0), (ECS_OFF, 1)], label="ECS", lanes=1)
    f.level("OCS", [(OCS_ON, 0), (OCS_OFF, 1)], label="OCS", lanes=2)
    f.level("AS", [(AS_ON, 0), (AS_NEG, 1)], label="AS", lanes=2)
    f.level("DS", [(DS_READ_ON, 0), (AS_NEG, 1)], label="DS", lanes=1)
    f.level("RW", [(0.0, 1)], start=1, label="R/W", lanes=2)
    f.level("D0", [(DSACK0_ON, 0), (DSACK_OFF, 1)], label="DSACK0", lanes=1)
    f.level("D1", [(DSACK1_ON, 0), (DSACK_OFF, 1)], label="DSACK1", lanes=1)
    f.bus("D", [(0, "z"), (DIN_VALID, "v"), (DIN_Z, "z")],
          label="D31-D0", lanes=2)
    f.level("DBEN", [(DBEN_READ_ON, 0), (DBEN_READ_OFF, 1)],
            label="DBEN", lanes=2)
    f.level("BERR", [(BERR_ON, 0), (BERR_OFF, 1)], label="BERR", lanes=1)
    f.level("HALT", [(HALT_ON, 0), (HALT_OFF, 1)], label="HALT", lanes=1)
    f.level("ASY", [(ASYNC_ON, 0), (ASYNC_OFF, 1)], label=ASYNC, lanes=1)

    f.span("CLK", 0, 0.00, ADDR_VALID, "6", "outL")
    f.span("CLK", 0, ADDR_INVALID, ADDR_Z, "7", "outR")
    f.span("A", 0, ADDR_VALID, ECS_OFF, "12A", "outR")
    f.span("A", 0, 6.00, ADDR_INVALID, "8", "outR")
    f.span("ECS", 0, 0.00, ECS_ON, "6A", "outL")
    f.span("ECS", 0, ECS_ON, ECS_OFF, "10", "in")
    f.span("OCS", 0, OCS_ON, OCS_OFF, "10A", "in")
    f.span("OCS", 1, ADDR_VALID, AS_ON, "11", "outL")
    f.span("AS", 0, AS_ON, AS_NEG, "14", "in")
    f.span("AS", 0, AS_NEG, ADDR_INVALID, "13", "outR")
    f.span("AS", 1, CLK_FALL, AS_ON, "9", "outL")
    f.span("AS", 1, AS_NEG, 6.00, "12", "outR")
    f.span("DS", 0, AS_NEG, ADDR_Z, "16", "outR")
    f.span("RW", 0, 0.00, RW_LOW, "18", "outL")
    f.span("RW", 0, RW_LOW, AS_ON, "21", "outL")
    f.span("RW", 1, RW_LOW, 7.00, "46", "in")
    f.span("RW", 1, AS_NEG, 6.60, "17", "outR")
    f.span("D0", 0, DSACK0_ON, DSACK1_ON, "31A", "in")
    f.span("D0", 0, AS_NEG, DSACK_OFF, "28", "outR")
    f.span("D1", 0, DSACK1_ON, DIN_VALID, "31", "outL")
    f.span("D1", 0, AS_NEG, 6.30, "29", "outR")
    f.span("D", 0, DIN_VALID, 5.00, "27", "outL")
    f.span("D", 0, AS_NEG, DIN_Z, "29A", "outR")
    f.span("D", 1, 5.00, 5.60, "30", "outR")
    f.span("DBEN", 0, 2.00, DBEN_READ_ON, "40", "outL")
    f.span("DBEN", 0, DBEN_READ_ON, DBEN_READ_OFF, "45", "in")
    f.span("DBEN", 1, AS_NEG, DBEN_READ_OFF, "41", "outR")
    f.span("BERR", 0, BERR_ON, 5.00, "27A", "outR")
    f.span("HALT", 0, DSACK1_ON, HALT_ON, "48", "outL")
    f.span("ASY", 0, ASYNC_ON, 3.00, "47A", "outL")
    f.span("ASY", 0, 5.00, ASYNC_OFF, "47B", "outR")
    return f


# ----------------------------------------------------- 10-4. write cycle ----
def fig4():
    f = Fig("Figure 10-4. Write Cycle Timing Diagram - MC68020/MC68EC020",
            states=STATES, labels=LABELS)
    f.clock(lanes=1)
    f.bus("A", [(0, "v"), (ADDR_VALID, "v"), (ADDR_INVALID, "v"),
                (ADDR_Z, "z")], label=ADDR, lanes=1)
    f.level("ECS", [(ECS_ON, 0), (ECS_OFF, 1)], label="ECS", lanes=1)
    f.level("OCS", [(OCS_ON, 0), (OCS_OFF, 1)], label="OCS", lanes=2)
    f.level("AS", [(AS_ON, 0), (AS_NEG, 1)], label="AS", lanes=2)
    f.level("DS", [(DS_WRITE_ON, 0), (AS_NEG, 1)], label="DS", lanes=2)
    f.level("RW", [(RW_LOW, 0), (6.40, 1)], start=1, label="R/W", lanes=2)
    f.level("D0", [(DSACK0_ON, 0), (DSACK_OFF, 1)], label="DSACK0", lanes=1)
    f.level("D1", [(DSACK1_ON, 0), (DSACK_OFF, 1)], label="DSACK1", lanes=1)
    f.bus("D", [(0, "z"), (DOUT_VALID, "v"), (DOUT_INVALID, "z")],
          label="D31-D0", lanes=2)
    f.level("DBEN", [(DBEN_WRITE_ON, 0), (DBEN_WRITE_OFF, 1)],
            label="DBEN", lanes=2)
    f.level("BERR", [(BERR_ON, 0), (BERR_OFF, 1)], label="BERR", lanes=1)
    f.level("HALT", [(HALT_ON, 0), (HALT_OFF, 1)], label="HALT", lanes=1)

    f.span("CLK", 0, 0.00, ADDR_VALID, "6", "outL")
    f.span("CLK", 0, ADDR_INVALID, ADDR_Z, "7", "outR")
    f.span("A", 0, ADDR_VALID, ECS_OFF, "12A", "outR")
    f.span("A", 0, 6.00, ADDR_INVALID, "8", "outR")
    f.span("ECS", 0, 0.00, ECS_ON, "6A", "outL")
    f.span("ECS", 0, ECS_ON, ECS_OFF, "10", "in")
    f.span("OCS", 0, OCS_ON, OCS_OFF, "10A", "in")
    f.span("OCS", 1, ADDR_VALID, AS_ON, "11", "outL")
    f.span("AS", 0, AS_ON, AS_NEG, "14", "in")
    f.span("AS", 1, CLK_FALL, AS_ON, "9", "outL")
    f.span("AS", 1, AS_NEG, 6.00, "12", "outR")
    f.span("DS", 0, AS_ON, DS_WRITE_ON, "9B", "outL")
    f.span("DS", 0, DS_WRITE_ON, AS_NEG, "14A", "in")
    f.span("DS", 1, AS_NEG, 6.40, "15", "outR")
    f.span("RW", 0, 0.00, RW_LOW, "20", "outL")
    f.span("RW", 0, RW_LOW, DS_WRITE_ON, "22", "outL")
    f.span("RW", 1, RW_LOW, 6.40, "46", "in")
    f.span("RW", 1, AS_NEG, 6.60, "17", "outR")
    f.span("D0", 0, DSACK0_ON, DSACK1_ON, "31A", "in")
    f.span("D0", 0, AS_NEG, DSACK_OFF, "28", "outR")
    f.span("D", 0, RW_LOW, DOUT_VALID, "55", "outL")
    f.span("D", 0, 2.00, DOUT_VALID, "23", "outL")
    f.span("D", 1, AS_NEG, DOUT_INVALID, "25", "outR")
    f.span("D", 1, 6.00, 6.60, "53", "outR")
    f.span("DBEN", 0, RW_LOW, DBEN_WRITE_ON, "44", "outL")
    f.span("DBEN", 0, DBEN_WRITE_ON, DBEN_WRITE_OFF, "45", "in")
    f.span("DBEN", 1, 1.60, DBEN_WRITE_ON, "42", "outL")
    f.span("DBEN", 1, AS_NEG, DBEN_WRITE_OFF, "43", "outR")
    f.span("BERR", 0, BERR_ON, 5.00, "27A", "outR")
    f.span("HALT", 0, DSACK1_ON, HALT_ON, "48", "outL")
    return f


# ------------------------------------------------- 10-5. bus arbitration ----
ARB_STATES = 12
ARB_LABELS = ["S0", "S1", "S2", "S3", "S4", "S5", "", "", "", "", "", ""]

BR_ON, BR_OFF = 1.20, 6.40
BG_ON, BG_OFF = 3.30, 8.40
BGACK_ON, BGACK_OFF = 5.60, 10.40
ARB_AS_ON, ARB_AS_OFF = 1.80, 4.70
ARB_Z, ARB_DRIVE = 5.20, 11.00


def fig5():
    f = Fig("Figure 10-5. Bus Arbitration Timing Diagram - MC68020/MC68EC020",
            states=ARB_STATES, labels=ARB_LABELS)
    f.clock(lanes=1)
    f.bus("A", [(0, "v"), (0.70, "v"), (4.90, "v"), (ARB_Z, "z"),
                (ARB_DRIVE, "v")], label=ADDR, lanes=1)
    f.bus("D", [(0, "z"), (2.30, "v"), (4.80, "z")], label="D31-D0", lanes=1)
    f.level("OCS", [(0.35, 0), (1.30, 1)], label="ECS, OCS", lanes=1)
    f.level("AS", [(ARB_AS_ON, 0), (ARB_AS_OFF, 1), (ARB_Z, None),
                   (ARB_DRIVE, 1)], label="AS, DS", lanes=2)
    f.level("RW", [(0.85, 0), (4.90, 1), (ARB_Z, None), (ARB_DRIVE, 1)],
            start=1, label="R/W", lanes=1)
    f.level("DBEN", [(1.95, 0), (4.90, 1), (ARB_Z, None), (ARB_DRIVE, 1)],
            label="DBEN", lanes=1)
    f.level("DSK", [(3.30, 0), (4.90, 1)], label="DSACK0, DSACK1", lanes=1)
    f.level("BR", [(BR_ON, 0), (BR_OFF, 1)], label="BR", lanes=2)
    f.level("BG", [(BG_ON, 0), (BG_OFF, 1)], label="BG", lanes=2)
    f.level("BGACK", [(BGACK_ON, 0), (BGACK_OFF, 1)], label="BGACK", lanes=2)

    f.span("CLK", 0, 4.90, ARB_Z, "7", "outR")
    f.span("AS", 0, ARB_AS_OFF, ARB_Z, "16", "outR")
    f.span("BR", 0, BR_ON, BG_ON, "35", "in")
    f.span("BR", 0, BGACK_ON, BR_OFF, "37A", "outR")
    f.span("BR", 1, 3.00, BG_ON, "33", "outL")
    f.span("BG", 0, BG_ON, BGACK_ON, "39A", "in")
    f.span("BG", 0, BGACK_ON, BG_OFF, "37", "outR")
    f.span("BG", 1, 8.00, BG_OFF, "34", "outL")
    f.span("BG", 1, BG_OFF, ARB_DRIVE, "39", "in")
    f.span("BGACK", 0, BGACK_OFF, ARB_DRIVE, "58", "outL")
    f.span("BGACK", 1, BG_OFF, ARB_DRIVE, "59", "in")
    return f


FIGURES = {
    3: ('figure-10-03-read-cycle.svg', fig3),
    4: ('figure-10-04-write-cycle.svg', fig4),
    5: ('figure-10-05-bus-arbitration.svg', fig5),
}


def main(which):
    for key in sorted(which or FIGURES):
        name, build = FIGURES[key]
        path = os.path.join(HERE, name)
        build().write(path)
        print('%-40s %d bytes' % (name + ':', os.path.getsize(path)))


if __name__ == '__main__':
    main([int(a) for a in sys.argv[1:]])
