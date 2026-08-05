# MC68881/MC68882 Floating-Point Coprocessor User's Manual — Split Index

The 409-page MC68881/MC68882 user's manual, broken into **23 PDFs** — one per
section, plus the front matter, the two reference lists, the index and the
timing-diagram foldout. Page ranges are contiguous, non-overlapping and account
for every page of the source.

Also here, extracted from Section 12:

- **[`ac-electrical-specifications.csv`](ac-electrical-specifications.csv)** and
  **[`dc-electrical-specifications.csv`](dc-electrical-specifications.csv)** — the
  timing and DC tables as data, all four speed grades.
- **Four redrawn timing diagrams**, Figures 12-1 to 12-4, as scalable SVG with a
  markdown page each carrying the diagram beside the specifications marked on it.

The source PDF is a 400 dpi paper scan with an OCR text layer that is unreliable
for numerals; how that was worked around is described under
[How the values were obtained](#how-the-values-were-obtained).

## The parts

| Part | Pages (source) | Pages | Bookmarks |
|---|--:|--:|--:|
| [`00-front-matter.pdf`](00-front-matter.pdf) | 1–4 | 4 | 1 |
| [`01-table-of-contents.pdf`](01-table-of-contents.pdf) | 5–12 | 8 | 1 |
| [`02-list-of-illustrations.pdf`](02-list-of-illustrations.pdf) | 13–16 | 4 | 1 |
| [`03-list-of-tables.pdf`](03-list-of-tables.pdf) | 17–18 | 2 | 1 |
| [`04-preface.pdf`](04-preface.pdf) | 19–20 | 2 | 1 |
| [`05-section-01-general-description.pdf`](05-section-01-general-description.pdf) | 21–36 | 16 | 19 |
| [`06-section-02-programming-model.pdf`](06-section-02-programming-model.pdf) | 37–44 | 8 | 11 |
| [`07-section-03-operand-data-formats.pdf`](07-section-03-operand-data-formats.pdf) | 45–58 | 14 | 14 |
| [`08-section-04-instruction-set.pdf`](08-section-04-instruction-set.pdf) | 59–208 | 150 | 97 |
| [`09-section-05-coprocessor-programming.pdf`](09-section-05-coprocessor-programming.pdf) | 209–224 | 16 | 21 |
| [`10-section-06-exception-processing.pdf`](10-section-06-exception-processing.pdf) | 225–264 | 40 | 39 |
| [`11-section-07-coprocessor-interface.pdf`](11-section-07-coprocessor-interface.pdf) | 265–306 | 42 | 44 |
| [`12-section-08-instruction-execution-timing.pdf`](12-section-08-instruction-execution-timing.pdf) | 307–346 | 40 | 28 |
| [`13-section-09-functional-signal-descriptions.pdf`](13-section-09-functional-signal-descriptions.pdf) | 347–354 | 8 | 15 |
| [`14-section-10-bus-operation.pdf`](14-section-10-bus-operation.pdf) | 355–370 | 16 | 13 |
| [`15-section-11-interfacing-methods.pdf`](15-section-11-interfacing-methods.pdf) | 371–376 | 6 | 9 |
| [`16-section-12-electrical-specifications.pdf`](16-section-12-electrical-specifications.pdf) | 377–382 | 6 | 7 |
| [`17-section-13-ordering-information.pdf`](17-section-13-ordering-information.pdf) | 383–386 | 4 | 4 |
| [`18-appendix-a-glossary.pdf`](18-appendix-a-glossary.pdf) | 387–390 | 4 | 1 |
| [`19-appendix-b-abbreviations-and-acronyms.pdf`](19-appendix-b-abbreviations-and-acronyms.pdf) | 391–394 | 4 | 1 |
| [`20-index.pdf`](20-index.pdf) | 395–404 | 10 | 1 |
| [`21-timing-diagram-foldouts.pdf`](21-timing-diagram-foldouts.pdf) | 405–406 | 2 | 4 |
| [`22-back-matter.pdf`](22-back-matter.pdf) | 407–409 | 3 | 1 |

Worth knowing about a few of them:

- **Part 08, Section 4 (Instruction Set)** is 150 pages and the reason to have this
  split at all. Its 97 bookmarks are all reconstructed: 48 from the table of
  contents and **49 individual instruction descriptions**, `FABS` through
  `FTWOTOX`, taken from the running headers on pages 76–182. `FMOVE` and `FMOVEM`
  each get two entries because the manual describes them twice, once per operand
  class.
- **Part 21** is the pull-out sheet at the back of the book. All three bus-cycle
  figures — 12-2, 12-3 and 12-4 — are printed side by side on this one landscape
  page, which is why Section 12 says *"Timing diagrams (Figures 12-2, 12-3, and
  12-4) are located on foldout pages at the end of this document"* rather than
  showing them in place.
- **Part 22** is not part of the book proper: a reader reply card and the back
  cover.

## Machine-readable specifications

### Redrawn figures

| Figure | Page | Diagram | Source |
|---|---|---|---|
| [12-1 Clock Input Timing](figure-12-1-clock-input-timing.md) | printed 12-3 | [SVG](figure-12-1-clock-input-timing.svg) | hand-authored |
| [12-2 Asynchronous Read Cycle](figure-12-2-asynchronous-read-cycle.md) | Foldout-1 | [SVG](figure-12-2-asynchronous-read-cycle.svg) | `make-figure-svg.py 2` |
| [12-3 Asynchronous Write Cycle](figure-12-3-asynchronous-write-cycle.md) | Foldout-2 | [SVG](figure-12-3-asynchronous-write-cycle.svg) | `make-figure-svg.py 3` |
| [12-4 Synchronous Read Cycle](figure-12-4-synchronous-read-cycle.md) | Foldout-3 | [SVG](figure-12-4-synchronous-read-cycle.svg) | `make-figure-svg.py 4` |

Each page carries the diagram and, beneath it, a table of exactly the
specifications that figure marks — generated from the CSV between `BEGIN TABLE`
and `END TABLE` comments by `make-figure-tables.py`, so the two cannot drift
apart. `make-figure-tables.py` refuses to run if a page asks for a specification
number the CSV does not have, because a silently dropped row would read as "this
figure does not reference that specification".

SVG referenced as an image is the only diagram format that survives GitHub's
markdown pipeline: GitHub renders Mermaid, but Mermaid has no waveform or timing
diagram type at all, it does not render WaveDrom, and it strips inline `<svg>`.
The figures are themed for light and dark backgrounds.

`timingsvg.py` is the small renderer the bus-cycle figures are drawn with. It is
byte-identical to [`../MC68030EC_split/timingsvg.py`](../MC68030EC_split/timingsvg.py);
keep the two copies in step if you change either.

### AC table

[`ac-electrical-specifications.csv`](ac-electrical-specifications.csv) — 37 rows
covering both AC tables, at 16.67, 20, 25 and 33.33 MHz.

| Column | Meaning |
|---|---|
| `table` | `clock` (§12.5, printed 12-3) or `read-write` (§12.6, printed 12-4/12-5) |
| `pdf_page`, `printed_page` | where the row comes from |
| `num` | the specification number as printed, e.g. `6A`; the figures draw it as `6a` |
| `footnotes` | the superscript note numbers on that row |
| `characteristic`, `condition`, `unit` | as printed |
| `f1667_min` … `f33_max` | min and max per speed grade; **empty means the source prints an em dash**, i.e. not specified — which is not the same as zero |
| `min_clks`, `max_clks` | the clock-period term of a two-term limit (specifications 25 and 27 only) |
| `confidence`, `note` | see below |

Specifications 25 and 27 are the only two-term limits: the source prints, for
example, `— / 105+` on the nanosecond line and `1.5 / 2.5` on a `Clks` line
beneath it, meaning **min = 1.5 clocks** and **max = 105 ns + 2.5 clocks**. The
nanosecond terms live in the ordinary grade columns and the clock terms in
`min_clks` / `max_clks`; both are the same at every grade.

### DC table

[`dc-electrical-specifications.csv`](dc-electrical-specifications.csv) — the
10-row §12.4 table, by characteristic and signal group. Two limits are symbolic
rather than numeric and are kept as strings: V<sub>IH</sub> max is `VCC`, and
V<sub>IL</sub> min is `GND-0.5`.

### How the values were obtained

The scan's text layer mangles numerals badly enough that reading it would have
been worse than useless — it drops and invents em dashes, so the columns slide,
and it turns digits into punctuation. So every value was read off a 300 dpi
rendering of the page instead, then checked three ways:

1. **Against the text layer**, comparing the *order* of the numbers rather than
   their positions: each row's numbers must appear as a subsequence of whatever
   the text layer recovered nearby. 33 of the 37 rows corroborate this way.
2. **By eye at 3× zoom** for the four rows where the text layer has nothing to
   compare against — 19, 19A, 20 and 22, all in a block on printed page 12-4
   where the two fastest columns were lost entirely.
3. **For monotonicity** across speed grades: a faster part should not need more
   time than a slower one.

`check-spec-csv.py` runs checks 1 and 3 and prints what it finds:

```sh
python3 check-spec-csv.py [path/to/MC68881UM.pdf]
```

Only one limit rises with frequency — specification **19A**, the `DSACK0`/`DSACK1`
skew window, whose minimum goes −15 → −10 ns. That is the window *narrowing*
around zero, which is the tighter specification, so it is expected rather than
suspect.

### Two things wrong in the source

Both are recorded in the CSV's `note` column and on the figure pages.

**The 33.33 MHz clock pulse width cannot fit its own cycle time.** A period must
hold one high pulse and one low pulse, so minimum pulse width + maximum pulse
width can never exceed the maximum cycle time. Three grades pass; 33.33 MHz gives
14 + 66 = 80 ns against a 60 ns maximum cycle. The page image and the text layer
agree on 66, so it is the manual's arithmetic, not a transcription error.

**The figures label specifications 11 and 11A the wrong way round.** The table
defines **11** as *AS Negated to R/W …* and **11A** as *DS Negated to R/W …*, but
all three foldout figures put `11a` on the `AS`-referenced dimension and `11` on
the `DS`-referenced one. The redrawings here follow the table. Nothing numerical
turns on it — the two entries carry identical limits at every grade.

Two smaller blemishes, faithfully preserved: specification 14 is printed with a
stray closing parenthesis (*"CS, DS Asserted to Data-Out Valid) (Read)"*), and
both continued AC pages head their first column *"16.67 HMz"*.

### A signal-name trap

The FPCP's chip select is **CS**, its address strobe **AS** and its data strobe
**DS** — all active low and all printed with an overbar, which does not survive
text extraction. Two substitutions will bite anyone grepping the text layer: in
Section 7, `CIR` comes out as `ClR` (lowercase L) 8 times in 184, and in the AC
tables `DSACK0` is frequently read as `DSACKO` with a letter O. Search
case-insensitively for both spellings.

## Notes on the split

The source has **23 top-level bookmarks and nothing below them**, so every
sub-bookmark in these parts is reconstructed:

- **Paragraph headings** come from the manual's own table of contents (pages
  5–12). Each entry's printed page — `12-3` — is mapped to a PDF page using the
  starting page of its section; that mapping is *measured*, not assumed, because
  the printed folio was read back off all 374 numbered pages and matched the
  derived page in every case.
- Every entry is then **verified against the page it claims**: the paragraph
  number has to appear at the head of a line there. 259 of 259 place correctly.
  Three needed a hand-written exemption, recorded in the split script with the
  reason: the scan renders `4.5.5.2` as `415.5.2` and `6.2.5` as `612.5`, and it
  drops the heading of `4.7.1.3` altogether (its page is confirmed by 4.7.1.2 and
  4.7.1.4, which share it).
- **Instruction bookmarks** in part 08 come from the running headers.

Titles are cleaned as they are read: the scan spaces out letters
(`T h e r m a l`), loses the wider gap that marked a word boundary inside such a
run, reads a capital I as a lowercase l, and renders em dashes as `- -` or `= -`.
The repairs are rules, not a lookup table, with two exceptions listed explicitly
in the script.

### Reproducing the split

Requires `pdftk` and `pdftotext`, and `MC68881UM.pdf` in the repository root —
see the [root README](../README.md) for its checksum.

```sh
python3 split-mc68881um.py          # writes all 23 PDFs into this directory
python3 make-spec-csv.py            # writes both CSVs
python3 check-spec-csv.py           # cross-checks the AC CSV against the PDF
python3 make-figure-svg.py          # redraws figures 12-2 to 12-4
python3 make-figure-pages.py        # rewrites their markdown pages
python3 make-figure-tables.py       # fills every page's table from the CSV
```

`figure-12-1-clock-input-timing.svg` and its markdown page are hand-authored;
only the table inside the page is generated.
