# M68000 family — pin assignments by package

Section 11.1 of the M68000 user's manual (PDF pages 183–188, printed pages
11-2 to 11-7) draws the pin assignment of every package it covers — nine
drawings for six processors. This puts them side by side: one row per signal,
one column per package, and in each cell the pin that carries the signal.

**An empty cell (—) means the package has no such pin.** That is different
from `NC`, which is a pin the package has and leaves unconnected; the `NC`
row lists those. Where a signal is on several pins — `VCC` and `GND` — every
one is listed.

The same data is in [`pin-assignments.csv`](pin-assignments.csv), with the
package columns described in
[`pin-assignment-packages.csv`](pin-assignment-packages.csv). Both are
written by [`make-pin-assignments.py`](make-pin-assignments.py).

## The packages

| Column | Parts | Package | Figure | Page (printed / PDF) | Pins |
|---|---|---|---|---|--:|
| `dip64` | MC68000, MC68010, MC68HC000 | 64-pin dual in line | 11-1 | 11-2 / 183 | 64 |
| `pga68` | MC68000, MC68010, MC68HC000 | 68-lead pin grid array | 11-2 | 11-3 / 184 | 68 |
| `pga68_hc001` | MC68HC001 | 68-lead pin grid array | 11-2 | 11-3 / 184 | 68 |
| `quad68` | MC68000, MC68HC000, MC68010 | 68-lead quad pack | 11-3 | 11-4 / 185 | 68 |
| `quad68_ec000` | MC68EC000 | 68-lead quad pack | 11-3 | 11-4 / 185 | 68 |
| `quad68_hc001` | MC68HC001 | 68-lead quad pack | 11-3 | 11-5 / 186 | 68 |
| `quad52` | MC68008 | 52-lead quad pack | 11-4 | 11-5 / 186 | 52 |
| `dip48` | MC68008 | 48-pin dual in line | 11-5 | 11-6 / 187 | 48 |
| `qfp64_ec000` | MC68EC000 | 64-lead quad flat pack | 11-6 | 11-7 / 188 | 64 |

## Pins by signal

| Signal | `dip64` | `pga68` | `pga68_hc001` | `quad68` | `quad68_ec000` | `quad68_hc001` | `quad52` | `dip48` | `qfp64_ec000` |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `A0` | — | — | — | — | 31 | — | 51 | 46 | 19 |
| `A1` | 29 | K4 | K4 | 32 | 32 | 32 | 52 | 47 | 20 |
| `A2` | 30 | J5 | J5 | 33 | 33 | 33 | 1 | 48 | 21 |
| `A3` | 31 | K5 | K5 | 34 | 34 | 34 | 2 | 1 | 22 |
| `A4` | 32 | K6 | K6 | 35 | 36 | 35 | 3 | 2 | 24 |
| `A5` | 33 | J6 | J6 | 36 | 37 | 36 | 4 | 3 | 25 |
| `A6` | 34 | K7 | K7 | 37 | 38 | 37 | 5 | 4 | 26 |
| `A7` | 35 | K8 | K8 | 38 | 39 | 38 | 6 | 5 | 27 |
| `A8` | 36 | J7 | J7 | 39 | 40 | 39 | 7 | 6 | 28 |
| `A9` | 37 | K9 | K9 | 40 | 41 | 40 | 8 | 7 | 29 |
| `A10` | 38 | J8 | J8 | 41 | 42 | 41 | 9 | 8 | 30 |
| `A11` | 39 | J9 | J9 | 42 | 43 | 42 | 10 | 9 | 31 |
| `A12` | 40 | H9 | H9 | 43 | 44 | 43 | 11 | 10 | 32 |
| `A13` | 41 | H8 | H8 | 44 | 45 | 44 | 12 | 11 | 33 |
| `A14` | 42 | J10 | J10 | 45 | 46 | 45 | 14 | 12 | 34 |
| `A15` | 43 | G9 | G9 | 46 | 47 | 46 | 16 | 14 | 35 |
| `A16` | 44 | H10 | H10 | 47 | 48 | 47 | 18 | 16 | 36 |
| `A17` | 45 | G10 | G10 | 48 | 49 | 48 | 19 | 17 | 37 |
| `A18` | 46 | F9 | F9 | 49 | 50 | 49 | 20 | 18 | 38 |
| `A19` | 47 | F10 | F10 | 50 | 51 | 50 | 21 | 19 | 39 |
| `A20` | 48 | E10 | E10 | 51 | 52 | 51 | 22 | — | 40 |
| `A21` | 50 | D10 | D10 | 53 | 54 | 53 | 13 | — | 42 |
| `A22` | 51 | C10 | C10 | 54 | 55 | 54 | — | — | 43 |
| `A23` | 52 | C9 | C9 | 55 | 56 | 55 | — | — | 44 |
| `D0` | 5 | B4 | B4 | 5 | 6 | 5 | 30 | 27 | 61 |
| `D1` | 4 | A3 | A3 | 4 | 5 | 4 | 29 | 26 | 60 |
| `D2` | 3 | A4 | A4 | 3 | 4 | 3 | 28 | 25 | 59 |
| `D3` | 2 | B5 | B5 | 2 | 3 | 2 | 27 | 24 | 58 |
| `D4` | 1 | A5 | A5 | 1 | 2 | 1 | 26 | 23 | 57 |
| `D5` | 64 | A6 | A6 | 68 | 68 | 68 | 25 | 22 | 55 |
| `D6` | 63 | B6 | B6 | 67 | 67 | 67 | 24 | 21 | 54 |
| `D7` | 62 | A7 | A7 | 66 | 66 | 66 | 23 | 20 | 53 |
| `D8` | 61 | A8 | A8 | 65 | 65 | 65 | — | — | 52 |
| `D9` | 60 | B7 | B7 | 64 | 64 | 64 | — | — | 51 |
| `D10` | 59 | A9 | A9 | 63 | 63 | 63 | — | — | 50 |
| `D11` | 58 | B8 | B8 | 62 | 62 | 62 | — | — | 49 |
| `D12` | 57 | A10 | A10 | 61 | 61 | 61 | — | — | 48 |
| `D13` | 56 | C8 | C8 | 60 | 60 | 60 | — | — | 47 |
| `D14` | 55 | B9 | B9 | 59 | 59 | 59 | — | — | 46 |
| `D15` | 54 | B10 | B10 | 58 | 58 | 58 | — | — | 45 |
| `AS` | 6 | A2 | A2 | 6 | 7 | 6 | 31 | 28 | 62 |
| `R/W` | 9 | C3 | C3 | 9 | 10 | 9 | 33 | 30 | 1 |
| `UDS` | 7 | B3 | B3 | 7 | 8 | 7 | — | — | 63 |
| `LDS` | 8 | B2 | B2 | 8 | 9 | 8 | — | — | 64 |
| `DS` | — | — | — | — | — | — | 32 | 29 | — |
| `DTACK` | 10 | B1 | B1 | 10 | 11 | 10 | 34 | 31 | 2 |
| `BR` | 13 | D1 | D1 | 13 | 14 | 13 | 37 | 33 | 4 |
| `BG` | 11 | C2 | C2 | 11 | 12 | 11 | 35 | 32 | 3 |
| `BGACK` | 12 | C1 | C1 | 12 | 13 | 12 | 36 | — | — |
| `IPL0` | 25 | J2 | J2 | 27 | 27 | 27 | 47 | 42 | 15 |
| `IPL1` | 24 | H3 | H3 | 26 | 26 | 26 | 45 | 41 | 14 |
| `IPL2` | 23 | H2 | H2 | 25 | 25 | 25 | 46 | 42 | 13 |
| `BERR` | 22 | J1 | J1 | 24 | 24 | 24 | 44 | 40 | 12 |
| `MODE` | — | — | K1 | — | 19 | 18 | — | — | 8 |
| `RESET` | 18 | F2 | F2 | 20 | 21 | 20 | 41 | 37 | 10 |
| `HALT` | 17 | F1 | F1 | 19 | 20 | 19 | 40 | 36 | 9 |
| `E` | 20 | H1 | H1 | 22 | — | 22 | 42 | 38 | — |
| `VMA` | 19 | G1 | G1 | 21 | — | 21 | — | — | — |
| `VPA` | 21 | G2 | G2 | 23 | — | 23 | 43 | 39 | — |
| `AVEC` | — | — | — | — | 23 | — | — | — | 11 |
| `FC0` | 28 | K3 | K3 | 30 | 30 | 30 | 50 | 45 | 18 |
| `FC1` | 27 | J3 | J3 | 29 | 29 | 29 | 49 | 44 | 17 |
| `FC2` | 26 | K2 | K2 | 28 | 28 | 28 | 48 | 43 | 16 |
| `CLK` | 15 | E1 | E1 | 15 | 16 | 15 | 38 | 34 | 6 |
| `VCC` | 14, 49 | D2, E9 | D2, E9 | 14, 52 | 15, 53 | 14, 52 | 15 | 13 | 5, 41 |
| `GND` | 16, 53 | D9, E2 | D9, E2 | 16, 17, 56, 57 | 1, 17, 18, 35, 57 | 16, 17, 56, 57 | 17, 39 | 15, 35 | 7, 23, 56 |
| `NC` | — | A1, J4, K1, K10 | A1, J4, K10 | 18, 31 | 22 | 31 | — | — | — |

## Reading the drawings

The drawings are line art in a scan, with no usable text layer, so every pin
was read by eye from a 200–400 dpi rendering. They number their pins three
ways:

- **Dual in line** packs count down the left side from pin 1 at the notch and
  back up the right.
- **Quad packs** count anticlockwise from the index mark — at the middle of
  the top edge on the 52- and 68-lead packs, at the top-left corner on the
  64-lead one. Each drawing prints a few pin numbers at its corners and edge
  midpoints (9, 10, 18, 26, 27, 35, 43, 44, 52, 60, 61 on the 68-lead packs),
  and every one of those falls on the pin the count says it should.
- **Pin grid arrays** are addressed by row letter (K at the top to A at the
  bottom, bottom view) and column number, exactly as the drawing labels them.

`make-pin-assignments.py` refuses to write anything unless each package
accounts for every one of its pins exactly once, and unless three
comparisons hold that would each expose a misread pin: the two MC68HC001
packages differ from their MC68000 twins in one pin only, the one that
carries `MODE`; the MC68000 64-pin DIP and 68-lead quad pack assign their
first sixteen pins identically; and the MC68EC000 68-lead quad pack is its
64-lead QFP plus exactly `BGACK`, two more `GND` and one `NC`.

## Things the drawings show that the text does not say

- **The MC68008 48-pin DIP ties `IPL2` and `IPL0` to one pin**, 42, printed
  `IPL2/IPL0`. That pin appears in both rows above.
- **The MC68HC001 is the MC68000 pinout plus `MODE`.** It takes pin K1 on the
  grid array and pin 18 on the quad pack, both of which the MC68000 leaves
  `NC`.
- **The MC68EC000's two packages disagree about `BGACK`.** The 68-lead quad
  pack carries it on pin 13; the 64-lead quad flat pack has no such pin. Its
  absence from the smaller package is consistent with the opening of
  paragraph 3.4, which says the MC68EC000 has no `BGACK`; its presence on the
  larger one is not.
- **Only the MC68EC000 and MC68008 packages bring out `A0`.** The MC68000,
  MC68010, MC68HC000 and MC68HC001 start their address bus at `A1`, using
  `UDS`/`LDS` for byte selection instead.
- **The MC68008 52-lead pack's four extra pins go to `A20`, `A21`, `BGACK`
  and a pin of its own for `IPL0`.** The 48-pin DIP does without all four:
  its address bus stops at `A19`, it has no `BGACK`, and it ties `IPL0` to
  `IPL2`.
