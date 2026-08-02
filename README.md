# Motorola M68000 / MC68030 documentation — split and extracted

Three Motorola manuals, each broken into one PDF per section so the parts can be opened
and navigated on their own, with a markdown index describing every part. Two of them
carry further extracted material: a per-processor instruction matrix for the
programmer's reference manual, and machine-readable electrical specifications plus
redrawn timing diagrams for the MC68030 data sheet.

**The source PDFs are not in this repository** and never will be — see
[Source documents](#source-documents) below for how to identify the exact editions
everything here was derived from.

## Contents

| Directory | Manual | Parts | Also contains |
|---|---|--:|---|
| [`MC68030UM_split/`](MC68030UM_split/) | MC68030 Enhanced 32-Bit Microprocessor User's Manual | 19 | — |
| [`M68000PRM_split/`](M68000PRM_split/) | M68000 Family Programmer's Reference Manual | 15 | instruction-support matrix |
| [`MC68030EC_split/`](MC68030EC_split/) | MC68030 Electrical Specifications | 8 | specification CSVs, redrawn timing figures |

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

## Source documents

These are third-party copyrighted manuals and are **not tracked here** — `.gitignore`
excludes every PDF in the repository root permanently. To reproduce or verify any of the
derived material, place your own copies in the repository root and check them against:

| File name | Size (bytes) | SHA-256 |
|---|--:|---|
| `MC68030UM.pdf` | 22,470,628 | `07a676828a5e476b96f24a8b963fd06b79b5860dac35166a182205ecbb9c7f95` |
| `M68000PRM.pdf` | 4,725,896 | `06e4864b78da0e815054cead9326b7ec9914661f240fd39a455f2061ff47c4e8` |
| `MC68030EC.pdf` | 574,322 | `d0de2af8cb4e806bc1d2f776baf1adb42174243167dcf9a6ed64d53cd812084e` |

```sh
sha256sum -c <<'EOF'
07a676828a5e476b96f24a8b963fd06b79b5860dac35166a182205ecbb9c7f95  MC68030UM.pdf
06e4864b78da0e815054cead9326b7ec9914661f240fd39a455f2061ff47c4e8  M68000PRM.pdf
d0de2af8cb4e806bc1d2f776baf1adb42174243167dcf9a6ed64d53cd812084e  MC68030EC.pdf
EOF
```

Editions, for identification:

| File | Document | Edition | Pages |
|---|---|---|--:|
| `MC68030UM.pdf` | MC68030 Enhanced 32-Bit Microprocessor User's Manual | `MC68030UM/AD` Rev. 2, © 1990 Motorola, published by Prentice-Hall | 599 |
| `M68000PRM.pdf` | M68000 Family Programmer's Reference Manual (Includes CPU32 Instructions) | © 1992 Motorola; owner-password encrypted (RC4) | 646 |
| `MC68030EC.pdf` | MC68030 Electrical Specifications | `MC68030EC/D` Rev. 1, © 1990 Motorola | 19 |

A checksum mismatch does not necessarily mean the wrong manual — these scans circulate in
several distinct digitisations. It does mean page numbers and bookmark offsets in the split
indexes may not line up with your copy, since every page range recorded here was derived
from the file above.

## How it was made

Splitting used `pdftk` throughout: dump the bookmarks, derive section boundaries, confirm
each boundary against the page text, `pdftk cat` the range, then reinject the sub-bookmarks
remapped to the new page numbering. Every split was verified afterwards for page-count
conservation, readability under `mutool`, and the absence of the blank placeholder bookmarks
`pdftk` inserts when an outline skips a level.

Each subdirectory's `README.md` documents its own contents, method and caveats.
