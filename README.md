# Motorola M68000 documentation — split and extracted

Five Motorola manuals, each broken into one PDF per section so the parts can be opened
and navigated on their own, with a markdown index describing every part. Four of them
carry further extracted material: a per-processor instruction matrix and a condition-code
reference for the programmer's reference manual, and machine-readable electrical specifications plus
redrawn timing diagrams for the MC68030 data sheet, the MC68881/MC68882 manual and the
M68000 user's manual.

**The source PDFs are not in this repository** and never will be — see
[Source documents](#source-documents) below for how to identify the exact editions
everything here was derived from.

## Contents

| Directory | Manual | Parts | Also contains |
|---|---|--:|---|
| [`MC68030UM_split/`](MC68030UM_split/) | MC68030 Enhanced 32-Bit Microprocessor User's Manual | 19 | — |
| [`M68000PRM_split/`](M68000PRM_split/) | M68000 Family Programmer's Reference Manual | 15 | instruction-support matrix, condition-code reference |
| [`MC68030EC_split/`](MC68030EC_split/) | MC68030 Electrical Specifications | 8 | specification CSVs, redrawn timing figures |
| [`MC68881UM_split/`](MC68881UM_split/) | MC68881/MC68882 Floating-Point Coprocessor User's Manual | 23 | specification CSVs, redrawn timing figures |
| [`MC68000UM_split/`](MC68000UM_split/) | M68000 8-/16-/32-Bit Microprocessors User's Manual | 19 | specification CSVs, redrawn timing figures |

### [`MC68030UM_split/`](MC68030UM_split/README.md) — MC68030 User's Manual

The full 599-page user's manual as **19 PDFs**: front matter, table of contents, preface,
the fourteen numbered sections, Appendix A and the index. Page ranges are contiguous and
non-overlapping and account for every source page. Each part keeps its own bookmark tree,
remapped to the new page numbering, so it stays navigable alone.

The large sections are the useful ones to have separately — Section 7 (Bus Operation, 106
pages), Section 9 (Memory Management Unit, 86 pages), Section 10 (Coprocessor Interface,
76 pages) and Section 11 (Instruction Execution Timing, 62 pages).

### [`M68000PRM_split/`](M68000PRM_split/README.md) — M68000 Family Programmer's Reference Manual

The 646-page programmer's reference as **15 PDFs**: front matter, contents, the eight
numbered sections and Appendices A–C. Sections 4, 5 and 6 are the alphabetical instruction
reference and have no bookmarks at all in the source; 167 per-instruction bookmarks were
reconstructed from the page running headers so those parts can be navigated.

Also here:

- **[`INSTRUCTIONS-BY-CPU.md`](M68000PRM_split/INSTRUCTIONS-BY-CPU.md)** — which of the 196
  instructions each processor and coprocessor supports (68000, 68008, 68010, 68020, 68030,
  68040, 68881/2, 68851; CPU32 excluded), as per-CPU lists and a full cross-reference
  matrix. Built from Appendix A's Table A-1 and cross-checked against both the
  per-processor tables and the `(family)` annotation on every instruction description.
  That check turned up **8 discrepancies in the manual**, listed with the evidence —
  including two support marks Table A-1 simply drops.

- **[`CONDITION-CODES.md`](M68000PRM_split/CONDITION-CODES.md)** — what each of the 122 MC680xx
  instructions does to the condition-code bits X, N, Z, V and C, gathered from the
  `Condition Codes:` block of every instruction description. The manual's own notation is kept —
  `U` undefined, `0` always cleared, `—` not affected — but its `*`, meaning "see the explanation
  below the table", is replaced by a note number, so the 193 asterisk cells reduce to 60 distinct
  explanations, each printed once. Cross-checked against Section 3's Table 3-18, which states the
  same facts in a different notation, and against a second extraction of the same pages; that
  turned up **18 defects in the manual**, including one cell where the two sources genuinely
  disagree, an instruction with no condition-code section at all, and a table row labelled
  `DIVS, DUVU`.

The source PDF is owner-password encrypted; the split parts are not.

### [`MC68030EC_split/`](MC68030EC_split/README.md) — MC68030 Electrical Specifications

The 19-page data sheet as **8 PDFs** following its own headings rather than numbered
sections. This is the document the user's manual's Section 13 refers you to for
everything beyond the maximum ratings.

Also here:

- **[`ac-electrical-specifications.csv`](MC68030EC_split/ac-electrical-specifications.csv)**
  — all 77 rows / 536 values of the clock-input and read/write-cycle AC tables, min and max
  for each of the five speed grades.
- **[`dc-electrical-specifications.csv`](MC68030EC_split/dc-electrical-specifications.csv)**
  — the 15-row DC table, by characteristic and signal group.
- **Seven redrawn timing diagrams** — Figures 2–8 as scalable SVG, each with a markdown page
  carrying the diagram beside the specifications marked on it, plus the generator that
  produces them.

The scan's OCR text layer is unreliable for numerals, so the values were read off the page
images and then cross-checked three ways. One value survives as an anomaly in the source
document itself: specification **#48** is the only non-monotonic limit in the tables, and
is flagged as such.

### [`MC68881UM_split/`](MC68881UM_split/README.md) — MC68881/MC68882 Coprocessor User's Manual

The 409-page floating-point coprocessor manual as **23 PDFs**: front matter, contents,
the two reference lists, the preface, the thirteen numbered sections, Appendices A and B,
the index, the timing-diagram foldout and the back cover. The source has 23 top-level
bookmarks and nothing at all below them, so all 311 sub-bookmarks were rebuilt — the
paragraph headings from the manual's own table of contents, verified one by one against
the page each claims, and the **49 instruction descriptions** in Section 4 (`FABS`
through `FTWOTOX`) from the running headers.

Also here:

- **[`ac-electrical-specifications.csv`](MC68881UM_split/ac-electrical-specifications.csv)**
  and **[`dc-electrical-specifications.csv`](MC68881UM_split/dc-electrical-specifications.csv)**
  — Section 12's timing and DC tables as data, at 16.67, 20, 25 and 33.33 MHz.
- **Four redrawn timing diagrams** — Figures 12-1 to 12-4 as scalable SVG, each with a
  markdown page carrying the diagram beside the specifications marked on it. The three
  bus-cycle figures are printed side by side on a single foldout sheet in the source.

The same reading-and-checking method was used as for the MC68030 data sheet, and it
turned up two errors in this manual: the 33.33 MHz maximum clock pulse width (66 ns)
does not fit inside the 33.33 MHz maximum cycle time (60 ns), and all three foldout
figures label specifications 11 and 11A the opposite way round from the table that
defines them.

### [`MC68000UM_split/`](MC68000UM_split/README.md) — M68000 8-/16-/32-Bit Microprocessors User's Manual

The 216-page ninth edition — the manual that covers the MC68000, MC68008, MC68010,
MC68HC000, MC68HC001 and MC68EC000 together — as **19 PDFs**: front matter, contents,
the two reference lists, the eleven numbered sections, Appendices A and B, the index and
the back cover. The source has **no outline whatsoever**, not one bookmark, so all 317
were rebuilt: the paragraph headings from the manual's own table of contents, verified
one by one against the page each claims, and 167 figure and table captions read off the
body pages rather than off the two front-matter lists — which disagree with the body in
several places.

Also here:

- **[`ac-electrical-specifications.csv`](MC68000UM_split/ac-electrical-specifications.csv)**
  — all seven of Section 10's AC tables, 158 rows and 1092 limits, at 8, 10, 12.5, 16.67
  (both the plain and the 12F part), 16 and 20 MHz.
- **[`dc-electrical-specifications.csv`](MC68000UM_split/dc-electrical-specifications.csv)**
  and **[`power-dissipation.csv`](MC68000UM_split/power-dissipation.csv)** — the maximum
  ratings, the thermal characteristics, the three DC tables and Tables 10-1 and 10-2.
- **[`ac-table-notes.csv`](MC68000UM_split/ac-table-notes.csv)** — the footnotes printed
  under each of the seven AC tables, so a figure page can print the ones its own rows
  reference.
- **Thirteen redrawn timing diagrams** — Figures 10-2 to 10-14 as scalable SVG, each with
  a markdown page carrying the diagram beside the specifications marked on it and that
  table's relevant footnotes.
- **[`table-3-4-signal-summary.md`](MC68000UM_split/table-3-4-signal-summary.md)** — the
  manual's one-page index of the bus, retyped from the page image, plus a table the source
  does not have: which of the six processors actually has each pin, with the page or
  figure every cell came from.

The same reading-and-checking method was used as for the other two, and this manual turns
out to be the most self-contradictory of the set: **specification 47 is given three
different values in three different tables**, specification 23's 16.67 MHz maximum is
printed as 550 ns where another table gives 50, §10.10 has two rows both numbered 48, and
a pull-up resistor is specified as 1.1 Ω rather than 1.1 kΩ. Twenty-nine such findings
are listed with the evidence in that directory's README.

## Source documents

These are third-party copyrighted manuals and are **not tracked here** — `.gitignore`
excludes every PDF in the repository root permanently. To reproduce or verify any of the
derived material, place your own copies in the repository root and check them against:

| File name | Size (bytes) | SHA-256 |
|---|--:|---|
| `MC68030UM.pdf` | 22,470,628 | `07a676828a5e476b96f24a8b963fd06b79b5860dac35166a182205ecbb9c7f95` |
| `M68000PRM.pdf` | 4,725,896 | `06e4864b78da0e815054cead9326b7ec9914661f240fd39a455f2061ff47c4e8` |
| `MC68030EC.pdf` | 574,322 | `d0de2af8cb4e806bc1d2f776baf1adb42174243167dcf9a6ed64d53cd812084e` |
| `MC68881UM.pdf` | 9,440,147 | `bb8cbc5262212a431ecb56fd4e5ba6334ecdc5f5ff996bedd729180c91700f2c` |
| `MC68000UM.pdf` | 11,152,468 | `e41cbe7e14dc7cb853f1185adb1dcd7043d2a2a3f43cdc909e0f6c146007a8e5` |

```sh
sha256sum -c <<'EOF'
07a676828a5e476b96f24a8b963fd06b79b5860dac35166a182205ecbb9c7f95  MC68030UM.pdf
06e4864b78da0e815054cead9326b7ec9914661f240fd39a455f2061ff47c4e8  M68000PRM.pdf
d0de2af8cb4e806bc1d2f776baf1adb42174243167dcf9a6ed64d53cd812084e  MC68030EC.pdf
bb8cbc5262212a431ecb56fd4e5ba6334ecdc5f5ff996bedd729180c91700f2c  MC68881UM.pdf
e41cbe7e14dc7cb853f1185adb1dcd7043d2a2a3f43cdc909e0f6c146007a8e5  MC68000UM.pdf
EOF
```

Editions, for identification:

| File | Document | Edition | Pages |
|---|---|---|--:|
| `MC68030UM.pdf` | MC68030 Enhanced 32-Bit Microprocessor User's Manual | `MC68030UM/AD` Rev. 2, © 1990 Motorola, published by Prentice-Hall | 599 |
| `M68000PRM.pdf` | M68000 Family Programmer's Reference Manual (Includes CPU32 Instructions) | © 1992 Motorola; owner-password encrypted (RC4) | 646 |
| `MC68030EC.pdf` | MC68030 Electrical Specifications | `MC68030EC/D` Rev. 1, © 1990 Motorola | 19 |
| `MC68881UM.pdf` | MC68881/MC68882 Floating-Point Coprocessor User's Manual | Second Edition, © 1989 Motorola, published by Prentice-Hall; reprinted 12/93 | 409 |
| `MC68000UM.pdf` | M68000 8-/16-/32-Bit Microprocessors User's Manual | `M68000UM/AD` Rev. 5, Ninth Edition, © 1993 Motorola; printed 10/93 | 216 |

A checksum mismatch does not necessarily mean the wrong manual — these scans circulate in
several distinct digitisations. It does mean page numbers and bookmark offsets in the split
indexes may not line up with your copy, since every page range recorded here was derived
from the file above.

## How it was made

Splitting used `pdftk` throughout: dump the bookmarks, derive section boundaries, confirm
each boundary against the page text, `pdftk cat` the range, then reinject the sub-bookmarks
remapped to the new page numbering. Where a manual has no usable outline of its own, the
sub-bookmarks are reconstructed — from running headers, or from the manual's own table of
contents — and every reconstructed entry is verified against the page it points at before
it is kept. Every split was verified afterwards for page-count
conservation, readability under `mutool`, and the absence of the blank placeholder bookmarks
`pdftk` inserts when an outline skips a level.

Each subdirectory's `README.md` documents its own contents, method and caveats.
