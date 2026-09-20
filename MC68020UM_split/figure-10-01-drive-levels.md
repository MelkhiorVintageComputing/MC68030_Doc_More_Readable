# Figure 10-1. Drive Levels and Test Points for AC Specifications

MC68020/MC68EC020 User's Manual, printed page 10-6 (PDF page 280 of `../MC68020UM.pdf`).

This figure defines how every other AC specification in the section is
measured: which voltage an input must be driven to, which threshold an output
delay is taken from, and where a signal-to-signal specification starts and
ends. It carries no specification of its own - the only number on it is the
figure's own label - so there is nothing to tabulate beside it, and it is the
one figure in the section that is reproduced here as text rather than redrawn.

The manual's own legend and notes, verbatim:

**NOTES:**

- **1.** This output timing is applicable to all parameters specified relative to the rising edge of the clock.
- **2.** This output timing is applicable to all parameters specified relative to the falling edge of the clock.
- **3.** This input timing is applicable to all parameters specified relative to the rising edge of the clock.
- **4.** This input timing is applicable to all parameters specified relative to the falling edge of the clock.
- **5.** This timing is applicable to all parameters specified relative to the assertion/negation of another signal.

**LEGEND:**

- **A.** Maximum output delay specification.
- **B.** Minimum output hold time.
- **C.** Minimum input setup time specification.
- **D.** Minimum input hold time specification.
- **E.** Signal valid to signal valid specification (maximum or minimum).
- **F.** Signal valid to signal invalid specification (maximum or minimum).

The 2.0 V and 0.8 V thresholds named throughout are the ones the clock figure
marks; see [Figure 10-2](figure-10-02-clock-input-timing.md).
