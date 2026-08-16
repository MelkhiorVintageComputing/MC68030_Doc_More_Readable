#!/usr/bin/env python3
"""Redraw the thirteen timing figures of Section 10 as SVG.

    python3 make-figure-svg.py            # all of them
    python3 make-figure-svg.py 4 5        # just figures 10-4 and 10-5

Two things about the redrawing are worth stating up front, because they are
choices rather than transcription:

* **Callout anchors follow what each specification measures**, per its
  description in ac-electrical-specifications.csv, not the pixel position of
  the arrowhead on the scan.  Where the two disagree the CSV wins, because
  the CSV is where the numbers live.

* **The horizontal axis of the bus-cycle figures is the source's own state
  ruler**, recovered by measuring it: on page 10-13 the printed S0..S7 labels
  sit 89 px apart at 300 dpi and each one is centred on a clock plateau, so
  state boundaries fall halfway between labels and every edge below can be
  quoted in states.  The delays drawn here are the ones the source draws -
  AS asserting about 0.8 of a state after the rising edge of S2, for
  instance, which is close to the specification maximum at 8 MHz.

  The five bus-arbitration figures have no state ruler and are broken in the
  middle with a drafting break, so their source has no scale to recover.
  Those are laid out on a plain state grid at event times chosen to satisfy
  every specification the figure marks at once - see ARBITRATION below.
"""
import os, sys
from timingsvg import Fig

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# The bus-cycle timeline, in bus states, S0 starting at t = 0.  Measured off
# the 300 dpi rendering of figure 10-4 (page 10-13) as described above; the
# write, MC68EC000 read and MC68EC000 write figures reuse it, since the
# source draws all four on the same ruler.
CLK_HI0, CLK_LO1 = 0.0, 1.0      # the S0 rising edge and the S0/S1 falling one
FC_VALID = 0.70                  # spec 6A from CLK_HI0
BUS_INVALID = 0.60               # specs 7 and 8 from CLK_HI0
ADDR_VALID = 1.50                # spec 6 from CLK_LO1
AS_NEG_PREV = -0.45              # the previous cycle's AS negating
AS_ASSERT = 2.80                 # spec 9 from the S2 rising edge
AS_NEGATE = 7.80                 # spec 12 from the S6/S7 falling edge
DS_ASSERT_W = 4.40               # a write asserts DS two states later
RW_HIGH = 0.40                   # spec 18 from CLK_HI0
RW_LOW = 2.90                    # spec 20 from the S2 rising edge
DTACK_ASSERT = 4.55              # spec 47 before the S4/S5 falling edge
DTACK_NEGATE = 10.65             # spec 28 from AS_NEGATE
DIN_VALID, DIN_INVALID = 6.55, 9.20
DOUT_VALID, DOUT_INVALID = 3.30, 8.60
BERR_ASSERT, BERR_NEGATE = 4.35, 9.55
HALT_ASSERT, HALT_NEGATE = 2.65, 4.75
ASYNC_CHANGE = 4.87
RAMP = 0.18                      # half-width drawn for specification 32

BUS_STATES = 12
BUS_LABELS = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "", "", "", ""]

# --------------------------------------------------------------------------
# ARBITRATION.  Event times for the five arbitration figures, in bus states.
# Chosen so that every specification the figures mark holds simultaneously:
#   35  BR asserted  -> BG asserted        1.5 .. 3.5 clks   0.7 -> 4.3 = 1.8
#   37A BGACK asserted -> BR negated       .. 1.5 clks       6.7 -> 7.7 = 0.5
#   36  BR negated   -> BG negated         1.5 .. 3.5 clks   7.7 -> 10.7 = 1.5
#   37  BGACK asserted -> BG negated       1.5 .. 3.5 clks   6.7 -> 10.7 = 2.0
#   46  BGACK width low                    >= 1.5 clks       6.7 -> 12.7 = 3.0
#   57  BGACK negated -> AS, DS, R/W driven >= 1.5 clks     12.7 -> 15.7 = 1.5
#   57A BGACK negated -> FC, VMA driven     >= 1 clk        12.7 -> 14.7 = 1.0
# One bus state is half a clock, so a clk is 2.0 on this scale.
BR_ASSERT, BG_ASSERT = 0.70, 4.30
STROBE_Z = 4.80                  # spec 38 from BG asserted
BGACK_ASSERT, BR_NEGATE = 6.70, 7.70
BG_NEGATE, BGACK_NEGATE = 10.70, 12.70
STROBE_DRIVE, FC_DRIVE = 15.70, 14.70
ARB_STATES = 18


# ======================================================================= 10-4
def read_cycle(ec000):
    """Figures 10-4 and 10-12: an asynchronous read."""
    who = "MC68EC000 " if ec000 else ""
    f = Fig("%sRead Cycle Timing Diagram" % who, states=BUS_STATES,
            labels=BUS_LABELS, lead=0.8, trail=0.3)
    f.clock(lanes=1)
    f.bus("FC", [(0, "v"), (FC_VALID, "v")], label="FC2-FC0", lanes=2)
    f.bus("A", [(0, "v"), (BUS_INVALID, "z"), (ADDR_VALID, "v")],
          label="A23-A0", lanes=2)
    f.level("AS", [(AS_NEG_PREV, 1), (AS_ASSERT, 0), (AS_NEGATE, 1)],
            start=0, label="AS", lanes=3)
    f.level("DS", [(AS_NEG_PREV, 1), (AS_ASSERT, 0), (AS_NEGATE, 1)],
            start=0, label="LDS / UDS", lanes=3)
    f.level("RW", [(RW_HIGH, 1)], start=0, label="R/W", lanes=1)
    f.level("DTACK", [(DTACK_ASSERT, 0), (DTACK_NEGATE, 1)], start=1,
            label="DTACK", lanes=2)
    f.bus("DIN", [(0, "z"), (DIN_VALID, "v"), (DIN_INVALID, "z")],
          label="DATA IN", lanes=1)
    f.level("BERR", [(BERR_ASSERT, 0), (BERR_NEGATE, 1)], start=1,
            label="BERR / BR", lanes=3)
    f.level("HALT", [(HALT_ASSERT, 0), (HALT_NEGATE, 1)], start=1,
            label="HALT / RESET", lanes=2)
    f.bus("ASY", [(0, "v"), (ASYNC_CHANGE, "v")],
          label="ASYNCHRONOUS|INPUTS", lanes=0)

    f.span("CLK", 0, CLK_HI0, FC_VALID, "6A")
    f.span("FC", 0, CLK_HI0, BUS_INVALID, "8")
    f.span("FC", 1, CLK_LO1, ADDR_VALID, "6")
    f.span("A", 0, CLK_HI0, BUS_INVALID, "7")
    f.span("A", 1, 7.0, AS_NEGATE, "12")
    f.span("AS", 0, AS_NEG_PREV, AS_ASSERT, "15")
    f.span("AS", 0, AS_ASSERT, AS_NEGATE, "14")
    f.span("AS", 1, AS_NEG_PREV, BUS_INVALID, "13")
    f.span("AS", 1, ADDR_VALID, AS_ASSERT, "11")
    f.span("AS", 2, FC_VALID, AS_ASSERT, "11A")
    f.span("DS", 0, AS_NEG_PREV, RW_HIGH, "17")
    f.span("DS", 1, 2.0, AS_ASSERT, "9")
    f.span("DS", 2, CLK_HI0, RW_HIGH, "18")
    f.span("RW", 0, DTACK_ASSERT, 5.0, "47")
    f.span("RW", 0, AS_NEGATE, DTACK_NEGATE, "28")
    f.span("DTACK", 0, DIN_VALID, 7.0, "27", style="outL")
    if not ec000:
        f.span("DTACK", 0, AS_NEGATE, DIN_INVALID, "29A")
    f.span("DTACK", 1, BERR_ASSERT, DTACK_ASSERT, "48", style="outL")
    f.span("DTACK", 1, DTACK_ASSERT, DIN_VALID, "31")
    f.span("DIN", 0, AS_NEGATE, DIN_INVALID, "29")
    f.span("BERR", 0, BERR_ASSERT, 5.0, "47")
    f.span("BERR", 0, AS_NEGATE, BERR_NEGATE, "30")
    f.span("BERR", 1, HALT_ASSERT, 3.0, "47")
    f.span("BERR", 1, HALT_NEGATE, 5.0, "47")
    # 32 is the input transition time - the ramp itself.  The engine draws
    # every edge with the same short ramp, so the callout is given a visible
    # width centred on the transition rather than the drawn ramp's width.
    f.span("BERR", 2, HALT_ASSERT - RAMP, HALT_ASSERT + RAMP, "32", style="outL")
    f.span("BERR", 2, HALT_NEGATE - RAMP, HALT_NEGATE + RAMP, "32", style="outR")
    f.span("HALT", 0, HALT_ASSERT, HALT_NEGATE, "56")
    f.span("HALT", 1, ASYNC_CHANGE, 5.0, "47")
    return f


# ======================================================================= 10-5
def write_cycle(ec000):
    """Figures 10-5 and 10-13: an asynchronous write."""
    who = "MC68EC000 " if ec000 else ""
    f = Fig("%sWrite Cycle Timing Diagram" % who, states=BUS_STATES,
            labels=BUS_LABELS, lead=0.8, trail=0.3)
    f.clock(lanes=1)
    f.bus("FC", [(0, "v"), (FC_VALID, "v")], label="FC2-FC0", lanes=2)
    # the write figure labels the address bus A23-A1: on a write it is UDS
    # and LDS, not A0, that pick the byte
    f.bus("A", [(0, "v"), (BUS_INVALID, "z"), (ADDR_VALID, "v")],
          label="A23-A0" if ec000 else "A23-A1", lanes=2)
    f.level("AS", [(AS_NEG_PREV, 1), (AS_ASSERT, 0), (AS_NEGATE, 1)],
            start=0, label="AS", lanes=4)
    f.level("DS", [(AS_NEG_PREV, 1), (DS_ASSERT_W, 0), (AS_NEGATE, 1)],
            start=0, label="LDS / UDS", lanes=4)
    f.level("RW", [(RW_HIGH, 1), (RW_LOW, 0), (AS_NEGATE, 1)], start=0,
            label="R/W", lanes=1)
    f.level("DTACK", [(DTACK_ASSERT, 0), (DTACK_NEGATE, 1)], start=1,
            label="DTACK", lanes=2)
    f.bus("DOUT", [(0, "z"), (DOUT_VALID, "v"), (DOUT_INVALID, "z")],
          label="DATA OUT", lanes=2)
    f.level("BERR", [(BERR_ASSERT, 0), (BERR_NEGATE, 1)], start=1,
            label="BERR / BR", lanes=3)
    f.level("HALT", [(HALT_ASSERT, 0), (HALT_NEGATE, 1)], start=1,
            label="HALT / RESET", lanes=2)
    f.bus("ASY", [(0, "v"), (ASYNC_CHANGE, "v")],
          label="ASYNCHRONOUS|INPUTS", lanes=0)

    f.span("CLK", 0, CLK_HI0, FC_VALID, "6A")
    f.span("FC", 0, CLK_HI0, BUS_INVALID, "8")
    f.span("FC", 1, CLK_LO1, ADDR_VALID, "6")
    f.span("A", 0, CLK_HI0, BUS_INVALID, "7")
    f.span("A", 1, 7.0, AS_NEGATE, "12")
    f.span("AS", 0, AS_NEG_PREV, AS_ASSERT, "15")
    f.span("AS", 0, AS_ASSERT, AS_NEGATE, "14")
    f.span("AS", 1, AS_NEG_PREV, BUS_INVALID, "13")
    f.span("AS", 1, 2.0, AS_ASSERT, "9")
    f.span("AS", 2, ADDR_VALID, AS_ASSERT, "11")
    f.span("AS", 3, FC_VALID, AS_ASSERT, "11A")
    f.span("DS", 0, AS_NEG_PREV, RW_HIGH, "17")
    f.span("DS", 0, AS_ASSERT, RW_LOW, "20A")
    f.span("DS", 1, DS_ASSERT_W, AS_NEGATE, "14A")
    f.span("DS", 2, CLK_HI0, RW_HIGH, "18")
    f.span("DS", 2, 2.0, RW_LOW, "20")
    f.span("DS", 3, ADDR_VALID, RW_LOW, "21")
    f.span("DS", 3, RW_LOW, DS_ASSERT_W, "22")
    f.span("RW", 0, FC_VALID, RW_LOW, "21A")
    f.span("RW", 0, DTACK_ASSERT, 5.0, "47")
    f.span("RW", 0, AS_NEGATE, DTACK_NEGATE, "28")
    f.span("DTACK", 0, RW_LOW, DOUT_VALID, "55")
    f.span("DTACK", 1, DOUT_VALID, DS_ASSERT_W, "26")
    f.span("DOUT", 0, 3.0, DOUT_VALID, "23")
    f.span("DOUT", 0, 8.0, DOUT_INVALID, "53")
    f.span("DOUT", 1, AS_NEGATE, DOUT_INVALID, "25")
    f.span("BERR", 0, BERR_ASSERT, DTACK_ASSERT, "48")
    f.span("BERR", 0, AS_NEGATE, BERR_NEGATE, "30")
    f.span("BERR", 1, HALT_ASSERT, 3.0, "47")
    f.span("BERR", 1, HALT_NEGATE, 5.0, "47")
    # 32 is the input transition time - the ramp itself.  The engine draws
    # every edge with the same short ramp, so the callout is given a visible
    # width centred on the transition rather than the drawn ramp's width.
    f.span("BERR", 2, HALT_ASSERT - RAMP, HALT_ASSERT + RAMP, "32", style="outL")
    f.span("BERR", 2, HALT_NEGATE - RAMP, HALT_NEGATE + RAMP, "32", style="outR")
    f.span("HALT", 0, HALT_ASSERT, HALT_NEGATE, "56")
    f.span("HALT", 1, ASYNC_CHANGE, 5.0, "47")
    return f


# ======================================================================= 10-6
def m6800_cycle():
    """Figure 10-6: an M6800 peripheral cycle, best case.

    E is the M6800 enable clock: six clock periods low, four high, which is
    twelve bus states low and eight high on this ruler.  The thirteen wait
    states the source draws between S4 and S5 are what stretches the cycle
    out until VPA can be recognised in phase with E.
    """
    labels = ["S0", "S1", "S2", "S3", "S4"] + ["w"] * 13 + ["S5", "S6", "S7", "S0"]
    f = Fig("MC68000 to M6800 Peripheral Timing Diagram (Best Case)",
            states=len(labels), labels=labels, lead=0.8, trail=0.5)
    E_LOW, E_HIGH, E_LOW2 = 1.30, 13.30, 21.30
    VPA_A, VPA_N = 4.70, 21.50
    VMA_A, VMA_N = 7.30, 21.30
    AS_N, ADDR_N = 19.80, 21.80
    f.clock(lanes=1)
    f.bus("A", [(0, "v"), (BUS_INVALID, "z"), (ADDR_VALID, "v"), (ADDR_N, "z")],
          label="A23-A1", lanes=1)
    f.level("AS", [(AS_NEG_PREV, 1), (AS_ASSERT, 0), (AS_N, 1)], start=0,
            label="AS", lanes=2)
    f.level("RW", [(RW_HIGH, 1), (RW_LOW, 0), (20.0, 1)], start=0,
            label="R/W", lanes=2)
    f.level("E", [(E_LOW, 0), (E_HIGH, 1), (E_LOW2, 0)], start=1, label="E", lanes=2)
    f.level("VPA", [(VPA_A, 0), (VPA_N, 1)], start=1, label="VPA", lanes=2)
    f.level("VMA", [(VMA_A, 0), (VMA_N, 1)], start=1, label="VMA", lanes=2)
    f.bus("DOUT", [(0, "z"), (DOUT_VALID, "v"), (ADDR_N, "z")],
          label="DATA OUT", lanes=1)
    f.bus("DIN", [(0, "z"), (19.50, "v"), (VPA_N, "z")], label="DATA IN", lanes=1)

    f.span("CLK", 0, AS_N, 20.40, "45")
    f.span("A", 0, 13.0, E_HIGH, "41")
    f.span("A", 0, 19.0, AS_N, "12")
    f.span("AS", 0, CLK_LO1, E_LOW, "41")
    f.span("AS", 1, AS_N, E_LOW2, "49")
    f.span("RW", 0, CLK_HI0, RW_HIGH, "18")
    f.span("RW", 0, 2.0, RW_LOW, "20")
    f.span("RW", 1, 20.0, 20.40, "18")
    f.span("E", 0, E_LOW, E_HIGH, "51")
    f.span("E", 0, E_HIGH, E_LOW2, "50")
    f.span("E", 1, E_LOW - 0.30, E_LOW, "42")
    f.span("E", 1, E_HIGH - 0.30, E_HIGH, "42")
    f.span("E", 1, AS_N, VPA_N, "44")
    f.span("VPA", 0, VPA_A, 5.0, "47")
    f.span("VPA", 1, 7.0, VMA_A, "40")
    f.span("VPA", 1, VMA_A, E_HIGH, "43")
    f.span("VMA", 0, 21.0, VMA_N, "41")
    f.span("VMA", 1, E_LOW2, ADDR_N, "45")
    f.span("DOUT", 0, 3.0, DOUT_VALID, "23")
    f.span("DOUT", 0, E_LOW2, ADDR_N, "54")
    f.span("DIN", 0, 19.50, 20.0, "27")
    f.span("DIN", 0, AS_N, VPA_N, "29")
    return f


# ======================================================================= 10-7
def arb_grant():
    """Figure 10-7: bus arbitration, with the clock drawn last.

    The source puts CLK at the bottom of this one figure and at the top of
    every other; that is reproduced.  It is also the only arbitration figure
    that shows the grant being taken away and given again, which is what the
    second BG pulse and specification 39 are about.
    """
    f = Fig("Bus Arbitration Timing", states=ARB_STATES, labels=[""] * ARB_STATES,
            lead=0.8, trail=0.6)
    BG2_ASSERT = 14.30
    f.level("STR", [(1.50, 1), (STROBE_Z, None)], start=0,
            label="STROBES|AND R/W", lanes=1)
    f.level("BR", [(BR_ASSERT, 0), (BR_NEGATE, 1)], start=1, label="BR", lanes=1)
    f.level("BGACK", [(BGACK_ASSERT, 0), (BGACK_NEGATE, 1)], start=1,
            label="BGACK", lanes=1)
    f.level("BG", [(BG_ASSERT, 0), (BG_NEGATE, 1), (BG2_ASSERT, 0)], start=1,
            label="BG", lanes=2)
    f.clock(lanes=0)

    f.span("STR", 0, BGACK_ASSERT, BR_NEGATE, "37A")
    f.span("STR", 0, BR_NEGATE, BG_NEGATE, "36")
    f.span("BR", 0, BGACK_ASSERT, BG_NEGATE, "37")
    f.span("BGACK", 0, BGACK_ASSERT, BGACK_NEGATE, "46")
    f.span("BGACK", 0, BR_ASSERT, BG_ASSERT, "35")
    f.span("BG", 0, 4.0, BG_ASSERT, "33")
    f.span("BG", 0, 10.0, BG_NEGATE, "34")
    f.span("BG", 0, BG_NEGATE, BG2_ASSERT, "39")
    f.span("BG", 1, BG_ASSERT, STROBE_Z, "38")
    return f


# ============================================================ 10-8 .. 10-11 --
def arb_bus(kind):
    """Figures 10-8, 10-9, 10-10 and 10-11.

    All four share a row set - the arbitration handshake over the bus the
    processor is giving up - and differ only in what the bus is doing when
    the request arrives.  `kind` selects that:

      'plain'    figure 10-8,  captioned exactly like 10-7
      'idle'     figure 10-9,  the bus already idle
      'active'   figure 10-10, a cycle finishing first, so the strobes
                 negate before they are released and the callouts become
                 7 and 16 rather than 38
      'multiple' figure 10-11, two grants in succession
    """
    title = {"plain": "Bus Arbitration Timing",
             "idle": "Bus Arbitration Timing — Idle Bus Case",
             "active": "Bus Arbitration Timing — Active Bus Case",
             "multiple": "Bus Arbitration Timing — Multiple Bus Request"}[kind]
    states = 27 if kind == "multiple" else ARB_STATES
    f = Fig(title, states=states, labels=[""] * states, lead=0.8, trail=0.6)
    f.clock(lanes=1)
    if kind == "multiple":
        # Two alternate masters take the bus one after the other.  BR stays
        # asserted across both grants - that is what tells the processor a
        # second master is still waiting - and is only negated before the
        # last grant ends.
        bg1_n, bg2_a, bg2_n = 9.70, 15.70, 24.70
        a1, n1, a2, n2 = 6.70, 12.70, 17.70, 23.70
        brn = 21.70
        f.level("BR", [(BR_ASSERT, 0), (brn, 1)], start=1, label="BR", lanes=1)
        f.level("BG", [(BG_ASSERT, 0), (bg1_n, 1), (bg2_a, 0), (bg2_n, 1)],
                start=1, label="BG", lanes=1)
        f.level("BGACK", [(a1, 0), (n1, 1), (a2, 0), (n2, 1)], start=1,
                label="BGACK", lanes=1)
        z, drive, fcdrive = STROBE_Z, 24.70, 25.70
    else:
        f.level("BR", [(BR_ASSERT, 0), (BR_NEGATE, 1)], start=1, label="BR", lanes=1)
        f.level("BG", [(BG_ASSERT, 0), (BG_NEGATE, 1)], start=1, label="BG", lanes=2)
        f.level("BGACK", [(BGACK_ASSERT, 0), (BGACK_NEGATE, 1)], start=1,
                label="BGACK", lanes=1)
        z, drive, fcdrive = STROBE_Z, STROBE_DRIVE, FC_DRIVE

    # In the active-bus figure a cycle is still finishing when the grant is
    # taken, so the strobes negate first and only then go high impedance; in
    # the others they are already negated and simply stop being driven.
    if kind == "active":
        strobe, vma, rw = ([(3.30, 1), (4.30, None), (drive, 1)],
                           [(3.30, 1), (4.30, None), (fcdrive, 1)],
                           [(3.30, 1), (4.30, None), (drive, 1)])
    else:
        strobe, vma, rw = ([(z, None), (drive, 1)], [(z, None), (fcdrive, 1)],
                           [(z, None), (drive, 1)])
    f.level("AS", strobe, start=0 if kind == "active" else 1, label="AS", lanes=0)
    f.level("DS", strobe, start=0 if kind == "active" else 1, label="DS", lanes=1)
    f.level("VMA", vma, start=0 if kind == "active" else 1, label="VMA", lanes=0)
    f.level("RW", rw, start=1, label="R/W", lanes=0)
    f.bus("FC", [(0, "v"), (z, "z"), (fcdrive, "v")], label="FC2-FC0", lanes=1)
    f.bus("A", [(0, "v"), (z, "z"), (fcdrive, "v")], label="A19-A0", lanes=0)
    f.bus("D", [(0, "v"), (z, "z"), (fcdrive, "v")], label="D7-D0", lanes=0)

    f.span("CLK", 0, BR_ASSERT, 1.0, "47")
    f.span("CLK", 0, 4.0, BG_ASSERT, "33")
    if kind == "multiple":
        f.span("BR", 0, BR_ASSERT, BG_ASSERT, "35")
        f.span("BR", 0, bg1_n, bg2_a, "39")
        f.span("BR", 0, brn, bg2_n, "36")
        f.span("BG", 0, a1, bg1_n, "37")
        f.span("BG", 0, a2, bg2_n, "37")
        f.span("BGACK", 0, a1, n1, "46")
        f.span("BGACK", 0, a2, n2, "46")
        f.span("DS", 0, BG_ASSERT, z, "38")
        f.span("DS", 0, brn, drive, "58")
        f.span("FC", 0, n2, fcdrive, "57A")
    else:
        f.span("BR", 0, BR_ASSERT, BG_ASSERT, "35")
        f.span("BG", 0, BGACK_ASSERT, BR_NEGATE, "37A")
        f.span("BG", 0, 10.0, BG_NEGATE, "34")
        f.span("BG", 1, BGACK_ASSERT, BG_NEGATE, "37")
        f.span("BG", 1, BR_NEGATE, BG_NEGATE, "36")
        f.span("BGACK", 0, BGACK_ASSERT, BGACK_NEGATE, "46")
        f.span("BGACK", 0, BGACK_NEGATE, 13.0, "47")
        if kind == "active":
            f.span("BGACK", 0, 4.0, 4.30, "16")
            f.span("FC", 0, 4.0, 4.30, "7")
        else:
            f.span("BGACK", 0, BG_ASSERT, z, "38")
        f.span("DS", 0, BGACK_NEGATE, drive, "57")
        f.span("FC", 0, BGACK_NEGATE, fcdrive, "57A")
    return f


# ====================================================================== 10-14
def arb_ec000():
    """Figure 10-14: the MC68EC000 has no BGACK and no VMA, so the handshake
    is two wires and the bus comes back on BR being negated."""
    f = Fig("MC68EC000 Bus Arbitration Timing Diagram", states=ARB_STATES,
            labels=[""] * ARB_STATES, lead=0.8, trail=0.6)
    BRN, BGN, DRIVE, FCDRIVE = 11.70, 14.70, 16.70, 15.70
    f.clock(lanes=1)
    f.level("BR", [(BR_ASSERT, 0), (BRN, 1)], start=1, label="BR", lanes=1)
    f.level("BG", [(BG_ASSERT, 0), (BGN, 1)], start=1, label="BG", lanes=2)
    f.level("AS", [(STROBE_Z, None), (DRIVE, 1)], start=1, label="AS", lanes=0)
    f.level("DS", [(STROBE_Z, None), (DRIVE, 1)], start=1, label="DS", lanes=0)
    f.level("RW", [(STROBE_Z, None), (DRIVE, 1)], start=1, label="R/W", lanes=2)
    f.bus("FC", [(0, "v"), (STROBE_Z, "z"), (FCDRIVE, "v")], label="FC2-FC0", lanes=0)
    f.bus("A", [(0, "v"), (STROBE_Z, "z"), (FCDRIVE, "v")], label="A19-A0", lanes=0)
    f.bus("D", [(0, "v"), (STROBE_Z, "z"), (FCDRIVE, "v")], label="D7-D0", lanes=0)

    f.span("CLK", 0, BR_ASSERT, 1.0, "47")
    f.span("CLK", 0, 4.0, BG_ASSERT, "33")
    f.span("BR", 0, BR_ASSERT, BG_ASSERT, "35")
    f.span("BR", 0, BRN, BGN, "36")
    f.span("BG", 0, -0.50, BG_ASSERT, "39")
    f.span("BG", 0, 14.0, BGN, "34")
    f.span("BG", 1, BG_ASSERT, STROBE_Z, "38")
    f.span("RW", 0, BGN, DRIVE, "58")
    f.span("RW", 1, BGN, FCDRIVE, "58A")
    return f


# --------------------------------------------------------------------------
FIGS = {
    4:  ("figure-10-04-read-cycle",              lambda: read_cycle(False)),
    5:  ("figure-10-05-write-cycle",             lambda: write_cycle(False)),
    6:  ("figure-10-06-m6800-peripheral",        m6800_cycle),
    7:  ("figure-10-07-bus-arbitration",         arb_grant),
    8:  ("figure-10-08-bus-arbitration",         lambda: arb_bus("plain")),
    9:  ("figure-10-09-bus-arbitration-idle",    lambda: arb_bus("idle")),
    10: ("figure-10-10-bus-arbitration-active",  lambda: arb_bus("active")),
    11: ("figure-10-11-bus-arbitration-multiple", lambda: arb_bus("multiple")),
    12: ("figure-10-12-mc68ec000-read-cycle",    lambda: read_cycle(True)),
    13: ("figure-10-13-mc68ec000-write-cycle",   lambda: write_cycle(True)),
    14: ("figure-10-14-mc68ec000-bus-arbitration", arb_ec000),
}


def main(which):
    for n in which:
        slug, build = FIGS[n]
        p = build().write(os.path.join(HERE, slug + ".svg"))
        print("wrote %s" % os.path.basename(p))


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]] or sorted(FIGS)
    bad = [a for a in args if a not in FIGS]
    if bad:
        sys.exit("no generator for figure(s) %s; 10-2 and 10-3 are "
                 "hand-authored SVGs" % ", ".join("10-%d" % b for b in bad))
    main(args)
