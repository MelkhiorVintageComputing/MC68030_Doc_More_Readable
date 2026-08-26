# M68000 8-/16-/32-Bit Microprocessors User's Manual — split by section

`MC68000UM.pdf` is the ninth edition of Motorola's M68000 user's manual
(M68000UM/AD Rev 5, © 1993), 216 scanned pages covering the MC68000,
MC68008, MC68010, MC68HC000, MC68HC001 and MC68EC000. It arrives as one
flat file with **no outline at all** — not a single bookmark — so opening
it to a particular section means scrolling.

This directory holds the same 216 pages cut into 19 PDFs, one per section,
each with a reconstructed outline; the Section 10 electrical specifications
as CSV; all thirteen of that section's figures redrawn as SVG with the
relevant limits beside them; and Table 3-4, the signal summary, as text.

The source PDF is **not** in this repository. See the [root
README](../README.md) for how to identify the right file.

## The parts

| File | PDF pages | Printed | Pages | Bookmarks |
|---|--:|---|--:|--:|
| [`00-front-matter.pdf`](00-front-matter.pdf) | 1–7 | cover, tabs, title, fax page, sales offices | 7 | 1 |
| [`01-table-of-contents.pdf`](01-table-of-contents.pdf) | 8–12 | vii–xi | 5 | 1 |
| [`02-list-of-illustrations.pdf`](02-list-of-illustrations.pdf) | 13–15 | xii–xiv | 3 | 1 |
| [`03-list-of-tables.pdf`](03-list-of-tables.pdf) | 16–17 | xv–xvi | 2 | 1 |
| [`04-section-01-overview.pdf`](04-section-01-overview.pdf) | 18–21 | 1-1…1-4 | 4 | 7 |
| [`05-section-02-introduction.pdf`](05-section-02-introduction.pdf) | 22–35 | 2-1…2-14 | 14 | 23 |
| [`06-section-03-signal-description.pdf`](06-section-03-signal-description.pdf) | 36–45 | 3-1…3-10 | 10 | 21 |
| [`07-section-04-8-bit-bus-operation.pdf`](07-section-04-8-bit-bus-operation.pdf) | 46–53 | 4-1…4-8 | 8 | 12 |
| [`08-section-05-16-bit-bus-operation.pdf`](08-section-05-16-bit-bus-operation.pdf) | 54–93 | 5-1…5-40 | 40 | 59 |
| [`09-section-06-exception-processing.pdf`](09-section-06-exception-processing.pdf) | 94–113 | 6-1…6-20 | 20 | 39 |
| [`10-section-07-8-bit-instruction-execution-times.pdf`](10-section-07-8-bit-instruction-execution-times.pdf) | 114–125 | 7-1…7-12 | 12 | 28 |
| [`11-section-08-16-bit-instruction-execution-times.pdf`](11-section-08-16-bit-instruction-execution-times.pdf) | 126–137 | 8-1…8-12 | 12 | 27 |
| [`12-section-09-mc68010-instruction-execution-times.pdf`](12-section-09-mc68010-instruction-execution-times.pdf) | 138–151 | 9-1…9-14 | 14 | 32 |
| [`13-section-10-electrical-and-thermal-characteristics.pdf`](13-section-10-electrical-and-thermal-characteristics.pdf) | 152–181 | 10-1…10-30 | 30 | 32 |
| [`14-section-11-ordering-information-and-mechanical-data.pdf`](14-section-11-ordering-information-and-mechanical-data.pdf) | 182–197 | 11-1…11-16 | 16 | 19 |
| [`15-appendix-a-mc68010-loop-mode-operation.pdf`](15-appendix-a-mc68010-loop-mode-operation.pdf) | 198–201 | A-1…A-4 | 4 | 3 |
| [`16-appendix-b-m6800-peripheral-interface.pdf`](16-appendix-b-m6800-peripheral-interface.pdf) | 202–207 | B-1…B-6 | 6 | 9 |
| [`17-index.pdf`](17-index.pdf) | 208–213 | INDEX-1…INDEX-6 | 6 | 1 |
| [`18-back-matter.pdf`](18-back-matter.pdf) | 214–216 | tabs, colophon | 3 | 1 |

216 pages in, 216 pages out, 317 bookmarks where there were none.

## How the outline was rebuilt

Nothing here trusts the scan on its own.

**The printed-folio to PDF-page map is measured, not assumed.** Every body
page carries a running footer of the form `MOTOROLA  <title>  10-8`, so the
folio of all 196 numbered pages was read straight off the page. They run
1-1…1-4, 2-1…2-14, … with no gaps and no repeats, which is what makes
"printed page 10-8 → PDF page 159" a fact rather than an arithmetic guess.
One page loses its footer to the scan (1-1) and two more have their section
letter misread (`B-3` and `B-5` come back as `8-3` and `8-5`); all three are
pinned by their neighbours.

**Paragraph headings come from the manual's own table of contents** (pages
8–12), and each one is then checked against the page it claims: the heading
number has to appear at the head of a line on that page. 131 entries, 131
placed. Two of them are not where the table of contents says — see below —
and one is exempted by name because the print itself is defective.

**Figure and table captions come from the body pages, not from the two
front-matter lists.** The lists disagree with the body in several places, and
the body is what a reader actually turns to. A caption is told apart from
prose that happens to begin "Figure 5-19." by three filters, each of which is
needed: an indent (prose starts at the left margin), an upper-case first word
(prose continues "… shows the timing for …"), and agreement between the
caption's section number and the section the page is in (a stub head reading
"Table 4-4" inside Table 5-6 is not a caption). Two-line captions are joined
when the second line is centred under the first. 167 captions found this way,
covering 100 figures and 63 tables; two more were supplied by hand because
their pages are full-page drawings with an empty text layer.

Rerun it with:

```sh
python3 split-mc68000um.py       # needs pdftk and pdftotext on PATH
```

## The Section 10 electrical specifications

| File | Rows | What is in it |
|---|--:|---|
| [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv) | 158 | §10.8 – §10.15, all seven AC tables |
| [`dc-electrical-specifications.csv`](dc-electrical-specifications.csv) | 76 | §10.1 maximum ratings, §10.2 thermal, §10.6, §10.7, §10.13 |
| [`power-dissipation.csv`](power-dissipation.csv) | 16 | Tables 10-1 and 10-2 |
| [`ac-table-notes.csv`](ac-table-notes.csv) | 38 | the footnotes printed under each AC table |

1092 AC limits across 158 specification rows.

### Columns of `ac-electrical-specifications.csv`

| Column | Meaning |
|---|---|
| `table` | which of the seven tables: `clock`, `clock-mc68008`, `read-write`, `m6800-peripheral`, `bus-arbitration`, `mc68ec000-read-write`, `mc68ec000-bus-arbitration` |
| `pdf_page`, `printed_page` | where the row is, in both numbering schemes |
| `num` | the specification number as printed (`6A`, `20A`, `48*` — see the anomalies) |
| `footnotes` | the footnote markers on that row, comma-separated |
| `characteristic` | the characteristic text, expanded where the print elides it |
| `condition` | the test conditions from the table heading |
| `unit` | `ns`, `Clks`, `MHz` — as printed, including where that is wrong |
| `f8_min` … `f20_max` | the six speed grades. `f16_67` is the **16.67 MHz 12F** column in the MC68000/MC68008/MC68010 tables and the plain 16.67 MHz column in the MC68EC000 ones; `f16` exists only in the former. An empty cell means the source gives no limit. |
| `note` | anything that needs saying about that row |

`ac-table-notes.csv` holds the footnotes: `table`, `marker`, `applies_to`
(the speed grades a column footnote hangs off, empty for a row footnote) and
`text`. The figure pages print the column footnotes always and a row
footnote only when one of the rows they show references it — a figure page
lists a handful of rows out of a table of sixty, and printing all twelve of
that table's notes would bury the two that matter. A marker the source uses
but never defines is printed as such rather than left as a dangling
superscript.

A few cells in the source are simply left blank where the rest of their row
uses an em dash. Both mean "not specified"; the CSV records both as empty and
the `note` column says which cells are blank rather than dashed.

### How the values were obtained

By eye, from 300 dpi renderings of the pages — not from the PDF's text
layer. The text layer of this scan is good enough to *check* a
transcription and nowhere near good enough to *make* one: it drops columns,
loses em dashes, merges cells and reads `-14` as `·14`.

[`check-spec-csv.py`](check-spec-csv.py) does the checking. It re-extracts
the same pages with `pdftotext -layout` and, for every CSV row, looks for
that row's numbers *as a subsequence* of the numbers on the page line (or
short run of lines) that carries it. Positional comparison would be
hopeless — column *n* in one extraction is not column *n* in the other — but
order survives. It also reports every place where a faster speed grade
carries a looser limit than a slower one.

```
AC: 156 of 158 rows corroborated by the text layer, 2 known losses, 0 unexplained
dc-electrical-specifications.csv:  76 of 76 rows corroborated
power-dissipation.csv:             16 of 16 rows corroborated
grade ordering: 7 places where a faster grade has the looser limit
footnotes: 1 markers used but not defined, 5 notes defined but referenced by no row
```

The two rows the text layer cannot corroborate are named in the script with
the reason, and both were re-read at 3× instead. Of the seven grade-ordering
flags, six are the 16.67 MHz 12F column being a separately binned part rather
than a faster screen of the 16 MHz one, and the seventh is specification 23's
printing error. The footnote line is the source's own bookkeeping and is
covered below: the dangling marker is §10.15's specification 36, and three
of the five unreferenced notes are §10.12's, which marks the wrong ones.

## Where the source contradicts itself

Everything below is in the source. Nothing is corrected in the CSVs — the
printed value is what lands there, with the `note` column saying what is
wrong with it.

### Wrong numbers

* **Specification 23 at 16.67 MHz prints as 550 ns** in §10.10 (Clock Low to
  Data-Out Valid). §10.11 gives **50 ns** for the same specification at the
  same grade, and every other grade in §10.10 is between 25 and 62 ns. The
  550 is a typing error for 50.
* **Specification 46's unit prints as `ns`** in §10.10 (BGACK Width Low,
  1.5). §10.12 gives the same limit in `Clks`. A 1.5 ns minimum width is not
  a thing anyone could design to.
* **§10.6 prints 2.4 in both the minimum and the maximum column** of the
  output high voltage row. §10.7 gives the same line as a minimum only.
* **§10.6's footnote asks for "an external pullup resistor of 1.1 Ω".** On a
  5 V rail that is 4.5 A. It is 1.1 kΩ.

### The same specification, two different values

* **Specification 47, asynchronous input setup time**, is given three
  different ways. §10.10 has 10, 10, 10, 10, 5, 5 ns across the six grades;
  §10.11 has 10, 10, 10, 10, 10, 5; §10.12 has 10, 10, 10, 5, 5, 5. The three
  tables disagree at 16.67 MHz and at 16 MHz.
* **Specification 58A** is *"BR Negated to FC, AS Driven"* in §10.10 and
  *"BR Negated to FC, VMA Driven"* in §10.12.
* **Specification 20A** is *"AS Asserted to R/W Valid (Write)"* in §10.10 and
  *"AS Asserted to R/W Low (Write)"* in §10.14.
* **Specification 28A** is *"AS, DS Negated to Data-In High Impedance"* in
  §10.10 and a different characteristic entirely, *"Clock High to DTACK
  Negated"*, in §10.14.
* **The FN package's θ<sub>JA</sub> is 45 °C/W in §10.2 and 40 °C/W in
  Table 10-2.**

### Numbering and labelling

* **§10.10 has two rows numbered 48**: *BERR Asserted to DTACK Asserted* and
  *DTACK Asserted to BERR Asserted (MC68010 Only)*. The second is `48*` in
  the CSV — that label is this transcription's, not the manual's.
* **§10.15 marks specification 36 with footnote 7**, but that table defines
  only notes 1 and 2. The marker was carried over from §10.14.
* **§10.12's footnote markers point at the wrong notes.** Specifications 36,
  58 and 58A are marked 1 and specification 37A is marked 2; but note 1 of
  that table is about asynchronous input setup and note 2 about when `BR`
  must fall. The notes that fit are 4 and 5 — which are, word for word,
  §10.10's notes 7 and 8, the markers §10.10 puts on those same four
  specifications.
* **The 20 MHz column's footnote names different parts in different
  tables.** §10.8 says *"This frequency applies only to MC68HC000 and
  MC68EC000 parts"*; §10.10, §10.11 and §10.12 all say *"MC68HC000 and
  MC68HC001"*.
* **§10.12's note 1 says "the synchronous inputs `BGACK`, `IPL0-IPL2`, and
  `VPA`".** Every other statement of that note in the manual — Figure 10-7,
  Figure 10-12, §10.14's note 5 — calls them asynchronous, which they are.
* **Specifications 25 and 28 look like they have their footnote markers
  interchanged.** 25 (a 40 ns minimum) carries marker 10, whose note reads
  "245 ns for the MC68008"; 28 (a 240 ns maximum) carries marker 11, whose
  note reads "50 ns for the MC68008". Each note fits the other specification.
* **Table 10-2's caption prints "(θ<sub>JC</sub> ≠ θ<sub>JC</sub>)"**, which
  is a typo for θ<sub>JA</sub> — the table tabulates θ<sub>JA</sub>.
* **Figures 10-7 and 10-8 carry exactly the same caption**, "Bus Arbitration
  Timing", and 10-9 is drawn all but identically to 10-8.
* **Figure 10-2 labels the clock `BCLK` and the reset input `RSTI`**, names
  from a different Motorola manual; everywhere else in this book they are
  `CLK` and `RESET`. Its bottom row, the mode-select input, is unlabelled.
* **§10.1 spells "Commerical"** — twice.
* **§10.10's heading prints the supply tolerance as "±5+"**; §10.13 and
  §10.14 print it as "± 5;PC". Both mean ±5 %. The same ";pc" for "%" turns
  up inside note 6 of §10.10 and §10.14, *"When AS and R/W are equally
  loaded (±20;pc)"*. It is the only place a footnote's text is repaired
  rather than transcribed, because "(±20;pc)" is both unreadable and
  unambiguous.
* **Two footnotes are misspelled**: "Specificaton" in §10.11's note 2 and
  "lienar" in §10.12's note 3. Both are transcribed as printed.

### Outside Section 10

* **Section 5's tables are numbered 5-1 and 5-6** with nothing in between.
  Page 5-30 sends the reader to "Table 5-5" for case numbers that are in
  Table 5-1, and Table 5-6's own stub column is headed *"Conditions of
  Termination in Table 4-4"* — also Table 5-1. Table 5-6 is missing from the
  list of tables altogether.
* **The list of tables for Section 8 is offset by one** from 8-3 onward: it
  lists separate *Move Byte* and *Move Word* tables where the body has a
  single *Move Byte and Word* table, so the list ends at 8-15 and the body at
  8-14.
* **Two table-of-contents page numbers are wrong.** 1.1 is listed on 1-1 but
  printed on 1-2, and 1.4 is listed on 1-2 but printed on 1-3. The split
  script reports both as *relocated* and bookmarks the page the heading is
  actually on.
* **Heading 3.10 is printed "a:10 POWER SUPPLY (Vcc and GND)".** That is why
  it is the one entry the automatic check cannot verify.
* **The table of contents and the body disagree about five section titles.**
  The contents call Section 4 "8-Bit Bus Operations" (the body: "8-BIT BUS
  OPERATION"), Section 7 "8-Bit Instruction Timing" ("8-BIT INSTRUCTION
  EXECUTION TIMES"), and so on for 5, 8 and 9. The bookmarks use the body's
  titles for the section roots and the contents' wording for the paragraphs
  under them, because that is where each came from.
* **Figure 2-7's page in the list of illustrations is 2-3**; the caption is
  on 2-8. **Figure 11-10's entry is broken outright**: "Case - Suffix ……
  11-", with neither a case number nor a page.
* **Paragraph 3.4 contradicts itself about `BGACK`.** Its opening says the
  pin is missing from *"the 48-pin version of the MC68008 and MC68EC000"*;
  its own `BGACK` description a page later names only the 48-pin MC68008.
  The pin assignments and Section 10 both side with the opening.
* **The MC68EC000's `AVEC` pin is missing from Section 3.** It replaces
  `VPA` on that part, and it appears on Figure 3-3, in Section 5, in the
  MC68EC000 AC-table notes and in three pin assignments — but there is no
  row for it in Table 3-4 and no paragraph describing it in 3.7.

## Table 3-4, Signal Summary

[`table-3-4-signal-summary.md`](table-3-4-signal-summary.md) reconstructs the
manual's one-page index of the bus — every signal, its direction, its active
level, and whether it goes high impedance on `HALT` or on giving the bus
away. The page is a scanned image whose text layer renders `UDS` as `UcJS`
and `RESET` as `RESEi`, so the table is retyped from a 300 dpi rendering and
kept as [`signal-summary.csv`](signal-summary.csv).

The page adds one table the source does not have: which of the six
processors actually has each pin, collected from paragraphs 3.1 to 3.7 and
the pin assignments in Section 11, with the page or figure every cell came
from. That is where the two Section 3 findings above come from.

## The redrawn figures

Thirteen figures, one markdown page each, with the diagram and the
specifications it marks pulled from the CSV.

| | Figure | |
|---|---|---|
| 10-2 | [Drive Levels and Test Points for AC Specifications](figure-10-02-drive-levels-and-test-points.md) | the measurement conventions A–F |
| 10-3 | [Clock Input Timing Diagram](figure-10-03-clock-input-timing.md) | specifications 1–5 |
| 10-4 | [Read Cycle Timing Diagram](figure-10-04-read-cycle.md) | |
| 10-5 | [Write Cycle Timing Diagram](figure-10-05-write-cycle.md) | |
| 10-6 | [MC68000 to M6800 Peripheral Timing (Best Case)](figure-10-06-m6800-peripheral.md) | |
| 10-7 | [Bus Arbitration Timing](figure-10-07-bus-arbitration.md) | clock drawn at the bottom |
| 10-8 | [Bus Arbitration Timing](figure-10-08-bus-arbitration.md) | same caption as 10-7 |
| 10-9 | [Bus Arbitration Timing — Idle Bus Case](figure-10-09-bus-arbitration-idle.md) | |
| 10-10 | [Bus Arbitration Timing — Active Bus Case](figure-10-10-bus-arbitration-active.md) | |
| 10-11 | [Bus Arbitration Timing — Multiple Bus Request](figure-10-11-bus-arbitration-multiple.md) | |
| 10-12 | [MC68EC000 Read Cycle Timing Diagram](figure-10-12-mc68ec000-read-cycle.md) | |
| 10-13 | [MC68EC000 Write Cycle Timing Diagram](figure-10-13-mc68ec000-write-cycle.md) | |
| 10-14 | [MC68EC000 Bus Arbitration Timing Diagram](figure-10-14-mc68ec000-bus-arbitration.md) | |

Figure 10-1 is a graph of power dissipation against ambient temperature, not
a timing diagram; its data is in `power-dissipation.csv` instead.

**Format.** Each figure is a `.svg` file referenced from markdown as an
ordinary image. That is the only diagram format that survives GitHub's
markdown pipeline: GitHub supports no waveform syntax at all (Mermaid has
none), it does not render WaveDrom, and it strips inline `<svg>`. The
figures adapt to light and dark themes through `prefers-color-scheme`.

**Where the horizontal axis comes from.** For the four bus-cycle figures it
is the source's own state ruler, recovered by measuring it: on page 10-13 the
printed S0–S7 labels sit 89 px apart at 300 dpi and each is centred on a
clock plateau, so the state boundaries fall halfway between labels and every
edge can be quoted in states. The delays drawn are the ones the source
draws — `AS` asserting about 0.8 of a state after the rising edge of S2, for
instance, which is close to the specification maximum at 8 MHz.

The five arbitration figures have no state ruler and are broken in the middle
with a drafting break, so their source has no scale to recover. Those are
laid out on a plain grid at event times chosen so that **every specification
the figure marks is satisfied at once**; the arithmetic is written out in the
`ARBITRATION` block of `make-figure-svg.py`.

**Callout anchors follow what each specification measures**, per its
description in the CSV, rather than the pixel position of the arrowhead on
the scan.

Figures 10-2 and 10-3 are hand-authored SVG. They are annotation figures
rather than bus cycles — threshold crossings, drive levels, ramp times — and
the shared engine has no vocabulary for any of that.

`timingsvg.py` is the same small renderer used by `MC68030EC_split` and
`MC68881UM_split`, and the three copies are byte-identical. It grew one thing
for this manual: a level of `None` in a signal's edge list drops that signal
to a mid-rail line and lets it come back, which is what an arbitration figure
needs when the bus is handed over and then handed back. The addition is
inert for the other two manuals — their figures regenerate byte-identical.

## Reproducing everything

```sh
python3 split-mc68000um.py        # the 19 PDFs and their outlines
python3 make-spec-csv.py          # the three CSVs
python3 check-spec-csv.py         # cross-check them against the text layer
python3 make-figure-svg.py        # the eleven generated SVGs
python3 make-figure-pages.py      # the thirteen markdown pages
python3 make-figure-tables.py     # fill in their specification tables
python3 make-signal-summary.py    # Table 3-4 as CSV and markdown
```

`pdftk` and `pdftotext` (poppler-utils) need to be on `PATH`. The split
script writes a fresh document ID and modification date into every output on
each run, so the PDFs will not be byte-identical between runs even when
nothing has changed; compare page counts, bookmark counts and text digests
instead.
