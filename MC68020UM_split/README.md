# MC68020/MC68EC020 Microprocessors User's Manual — split by section

`MC68020UM.pdf` is the first edition of Motorola's MC68020/MC68EC020 user's
manual (© 1992, reprinted by Freescale), 306 pages. Unlike the other manuals
in this repository it is not a scan: it has a real text layer and it arrives
with an outline of its own, 227 bookmarks deep enough to reach every
paragraph heading.

So the work here is different in kind. Nothing had to be reconstructed from
running headers. What the manual needed instead was cutting into parts, a way
to reach its 177 figures and tables, and its Section 10 electrical
specifications turned into data — which this text layer makes possible to
*parse* rather than transcribe, provided you do not trust it to decode.

The source PDF is **not** in this repository. See the [root
README](../README.md) for how to identify the right file.

## The parts

| File | PDF pages | Printed | Pages | Bookmarks |
|---|--:|---|--:|--:|
| [`00-front-matter.pdf`](00-front-matter.pdf) | 1–2 | cover, preface (iii) | 2 | 1 |
| [`01-table-of-contents.pdf`](01-table-of-contents.pdf) | 3–9 | vii…xiii | 7 | 1 |
| [`02-list-of-illustrations.pdf`](02-list-of-illustrations.pdf) | 10–13 | xiv…xvii | 4 | 1 |
| [`03-list-of-tables.pdf`](03-list-of-tables.pdf) | 14–15 | xviii…xix | 2 | 1 |
| [`04-acronym-list.pdf`](04-acronym-list.pdf) | 16 | v | 1 | 1 |
| [`05-section-01-introduction.pdf`](05-section-01-introduction.pdf) | 17–29 | 1-1…1-13 | 13 | 16 |
| [`06-section-02-processing-states.pdf`](06-section-02-processing-states.pdf) | 30–35 | 2-1…2-6 | 6 | 11 |
| [`07-section-03-signal-description.pdf`](07-section-03-signal-description.pdf) | 36–43 | 3-1…3-8 | 8 | 17 |
| [`08-section-04-on-chip-cache-memory.pdf`](08-section-04-on-chip-cache-memory.pdf) | 44–47 | 4-1…4-4 | 4 | 9 |
| [`09-section-05-bus-operation.pdf`](09-section-05-bus-operation.pdf) | 48–125 | 5-1…5-78 | 78 | 95 |
| [`10-section-06-exception-processing.pdf`](10-section-06-exception-processing.pdf) | 126–153 | 6-1…6-28 | 28 | 33 |
| [`11-section-07-coprocessor-interface.pdf`](11-section-07-coprocessor-interface.pdf) | 154–214 | 7-1…7-61 | 61 | 99 |
| [`12-section-08-instruction-execution-timing.pdf`](12-section-08-instruction-execution-timing.pdf) | 215–254 | 8-1…8-40 | 40 | 35 |
| [`13-section-09-applications-information.pdf`](13-section-09-applications-information.pdf) | 255–274 | 9-1…9-20 | 20 | 32 |
| [`14-section-10-electrical-characteristics.pdf`](14-section-10-electrical-characteristics.pdf) | 275–288 | 10-1…10-14 | 14 | 15 |
| [`15-section-11-ordering-information-and-mechanical-data.pdf`](15-section-11-ordering-information-and-mechanical-data.pdf) | 289–299 | 13-1…13-11 *(sic — see below)* | 11 | 15 |
| [`16-appendix-a-mc68ec020-three-wire-bus-arbitration.pdf`](16-appendix-a-mc68ec020-three-wire-bus-arbitration.pdf) | 300 | A-1 | 1 | 2 |
| [`17-index.pdf`](17-index.pdf) | 301–306 | INDEX-1…INDEX-6 | 6 | 21 |

306 pages in, 306 pages out, 405 bookmarks where the source has 227. Page
conservation is not merely counted: the concatenated text of the eighteen
parts is byte-for-byte identical to the text of the whole manual.

## What was added to the outline

The manual's own 227 bookmarks are carried through and remapped, and each one
is verified against the page it claims by finding its paragraph number at the
head of a line there. All 227 verify.

The 178 new bookmarks are the figure and table captions, which the manual's
outline stops short of. **The titles come from the front-matter lists and the
pages from the body**, because each source is better at one of the two jobs.

The lists are better at titles. They carry the whole title on one line, where
the body wraps a long one onto a second line that cannot be told apart from a
table's own heading row; and they are set in a font the extraction decodes,
where the body renders θ as `q` and an em dash as `Ñ`. Compare Table 10-1: the
list gives *θJA vs. Airflow—MC68020 CQFP Package*, the body gives
*qJA vs. AirflowÑMC68020 CQFP Package*.

The body is better at pages, because it is where the figure actually is; the
lists give a printed folio, which is a second lookup.

Matching one against the other needs care, because prose cites figures by
number too. A sentence ending *"…as shown in Figure 7-7."* puts that number at
the head of a line with the next sentence running on after it, and looks
exactly like a caption. So a body line is accepted only when it carries the
right number **and** opens the right title, compared in the body's own
spelling. All 177 captions — 140 figures and 37 tables — are located, and
Figure 7-7 lands on its caption rather than on the sentence that cites it.

## The Section 10 electrical specifications

| File | Rows | What is in it |
|---|--:|---|
| [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv) | 65 | §10.3, the clock input and read/write tables |
| [`ac-table-notes.csv`](ac-table-notes.csv) | 14 | the footnotes printed under those two tables |
| [`dc-electrical-specifications.csv`](dc-electrical-specifications.csv) | 33 | §10.1 maximum ratings and both DC tables |
| [`thermal-characteristics.csv`](thermal-characteristics.csv) | 47 | §10.2 thermal resistance and Tables 10-1 to 10-4 |

520 AC limits across 65 specification rows, at 16.67, 20, 25 and 33.33 MHz.

### How the values were obtained

**Parsed, not transcribed.** This is the first manual in this repository whose
tables could be read mechanically, and
[`make-spec-csv.py`](make-spec-csv.py) does exactly that.

What the text layer will not do is *decode*. The Type 1 fonts are MacRoman
encoded and every extractor hands back the raw code point, so an em dash
arrives as `Ñ` and a bullet as `¥`; and every Greek letter and relation comes
out of the Symbol font, where `q` is θ and `m` is µ.

That last one is not cosmetic. It is the difference between

> I<sub>OH</sub> = 400 **µ**A — the output high voltage test condition

and

> I<sub>OL</sub> = 3.2 **m**A — the output low voltage one

which the layout-preserving extraction renders identically as `mA`. Eight
cells in the DC tables are microamps and seven are milliamps, and nothing in
the character stream distinguishes them except the font each was set in. So
the text is rebuilt here out of `mutool`'s character stream, which carries the
font and the size of every glyph, rather than taken from `pdftotext`.

The same stream settles the footnote markers, which are set solid against the
specification number: `31A3` is specification 31A carrying footnote 3, and
`9B11` is 9B carrying footnote 11 — not 9B carrying footnote 1 twice. The only
thing that tells a marker from a digit is that it is set a point smaller and
2.3 points higher, and the only thing that tells a raised marker from a
lowered subscript is which way it moved.

### How they were checked

[`check-spec-csv.py`](check-spec-csv.py) re-reads the same pages through
poppler — a different library, a different intermediate form — and compares.
Poppler is deliberately the weaker of the two readings: it decodes nothing, so
the words will not match, but it sees the same glyphs in the same order, and
every row's limits must turn up in it as a subsequence.

```
AC: 65 of 65 rows corroborated by poppler, 0 unexplained
dc-electrical-specifications.csv:      31 of 33 rows corroborated, 2 printed out of order
thermal-characteristics.csv:           47 of 47 rows corroborated, 0 printed out of order
grade ordering: 2 places where a faster grade has the looser maximum
footnotes: 0 markers used but not defined, 0 notes defined but referenced by no row
units: 8 cells read as microamps and 7 as milliamps; poppler renders every one of them "mA", 0 exceptions
```

The last line is the point of the exercise: poppler losing the distinction in
exactly the places the generator claims to have found it is what shows the
distinction was read off the font rather than invented.

The two rows printed out of order are the input low voltage of each DC table,
whose minimum is `GND −0.5` set across two lines, so the maximum of 0.8 is
printed between the two halves of it.

The two grade-ordering flags are not errors. The maximum clock pulse width
grows from 54 ns at 20 MHz to 61 at 25 and 66 at 33.33, because the maximum
*cycle* time is 80 ns at all three grades while the minimum pulse width
shrinks — 14 + 66 = 80 at 33.33 MHz, 19 + 61 = 80 at 25.

## The redrawn figures

| Figure | Page | |
|---|---|---|
| [Figure 10-1](figure-10-01-drive-levels.md) | Drive Levels and Test Points for AC Specifications | legend and notes as text |
| [Figure 10-2](figure-10-02-clock-input-timing.md) | Clock Input Timing Diagram | [SVG](figure-10-02-clock-input-timing.svg) |
| [Figure 10-3](figure-10-03-read-cycle.md) | Read Cycle Timing Diagram | [SVG](figure-10-03-read-cycle.svg) |
| [Figure 10-4](figure-10-04-write-cycle.md) | Write Cycle Timing Diagram | [SVG](figure-10-04-write-cycle.svg) |
| [Figure 10-5](figure-10-05-bus-arbitration.md) | Bus Arbitration Timing Diagram | [SVG](figure-10-05-bus-arbitration.svg) |

Each page carries the figure and, beside it, every specification the figure
marks — at all four speed grades, with the footnotes those rows reference. The
manual prints the figure and its table three pages apart, so reading a callout
off the diagram means turning back and forth.

Which specifications each figure marks is not guessed: the callout numbers are
read off the figure's own page in the source.

The three bus-cycle figures are generated by
[`make-figure-svg.py`](make-figure-svg.py) on the drawing engine
[`timingsvg.py`](timingsvg.py), which is byte-identical to the copies in
`MC68030EC_split/`, `MC68881UM_split/` and `MC68000UM_split/`. The clock
figure is drawn by hand, having no bus states to lay out against.

**Figure 10-1 is not redrawn.** It is five stacked measurement conventions
rather than a timing diagram, and it carries no specification of its own — the
only number on it is the figure's own label. Its legend and notes are what
carry the meaning, and they are reproduced verbatim on its page.

The clock and the two-level signals of Figures 10-3 to 10-5 were measured off
300 dpi renderings. The clock gives the time base: its edges fall every 19.8
points, which fixes one bus state at 19.8 points and the origin at the first
falling edge. The buses are placed rather than measured — they are drawn as
two converging rails, and the callout leaders cross the same band often enough
that a crossover cannot be told from a leader mechanically. Horizontal
placement is schematic in the source too.

## Where the source is not what it says it is

Nothing below is corrected in the split or the CSVs. What the manual prints is
what lands there.

### Section 11 carries a different manual's running footer

All eleven pages of Section 11, *Ordering Information and Mechanical Data*
(PDF pages 289–299), are footed

> MOTOROLA  **MC68838 USER'S MANUAL**  **13-1**

and run 13-1 to 13-11. Every other body page in the book is footed
`M68020 USER'S MANUAL` and carries a folio in its own section's series. The
apostrophe differs too — these eleven use a typographic `’` where the rest of
the manual uses the MacRoman code point that everything else in the file is
set with — so the pages were produced separately and dropped in without their
footers being corrected. The MC68838 is an FDDI device, not a member of this
family.

This is the reason the parts table above shows Section 11 as `13-1…13-11`:
that is what the pages say.

### The acronym list is bound out of order

The acronym list is printed page **v**, and it sits at PDF page 16 — after the
lists of illustrations and tables, which run xiv to xix. In folio order it
belongs immediately after the preface (iii) and before the table of contents
(vii). It is given a part of its own here rather than being filed under a
neighbour it does not belong to.

### The note under Figure 10-2 is misprinted and then breaks up

The note reads, as printed:

> NOTE: Timing measurements are referenced to and from a low voltage of **.08 V**
> and a high voltage of 2.0 V, unless **othervise** noted. The voltage swing
> through this **r** ... should start outside and pass through the range such
> that the rise or fall ... between 0.8 V and 2.0 V.

Three separate faults in one paragraph. The low threshold is **.08 V** where it
is 0.8 V everywhere else in the section, including in the figure's own axis
label directly above the note. *Otherwise* is spelled **othervise**. And the
text physically breaks up: "range" loses its last four letters and "will be
linear" is dropped altogether, with stray fragments stranded against the right
margin. The same note under Figure 10-3 (printed page 10-11) is complete and
correct, and reads "0.8 V" and "otherwise".

### `DSACK≈` is used ten times and defined nowhere

The read and write cycle table names the two data transfer acknowledge signals
collectively as `DSACK≈` — using the Symbol font's *approximately equal* glyph.
It appears ten times, on printed pages 10-8 to 10-10, and nowhere else: the
other 454 occurrences of the mnemonic in the manual write `DSACK0` and
`DSACK1` out in full. Nothing in the section, the acronym list or Section 3
defines it.

It is almost certainly meant to be the `x` of Motorola's usual `DSACKx`, set
from the wrong font. It is transcribed as printed.

### Two headings, two spellings

The MC68020 thermal resistance table is headed *Characteristic—Natural
Convection and No Heatsink*, with an em dash set solid; the MC68EC020 one,
four printed pages later and otherwise word for word the same, is headed
*Characteristic – Natural Convection and No Heatsink*, with a spaced en dash.

### The manual's own outline has two typos in it

The bookmarks that ship with the PDF include

- `10.2.2 MC68EC020 Thermal Characteristics and DC ELectrical Characteristics`
  — a capital L in the middle of *Electrical*, where the page itself prints it
  correctly;
- `11.2.3 MC68020 RP Suffix- Packabe Dimensions` — *Packabe* for *Package*.

Both are carried through unchanged, because the split reproduces the outline
it is given rather than editing it.

## Reproducing everything

```sh
python3 split-mc68020um.py      # the 18 part PDFs and their outlines
python3 make-spec-csv.py        # the four CSVs
python3 check-spec-csv.py       # re-reads the PDF and checks them
python3 make-figure-svg.py      # the three bus-cycle SVGs
python3 make-figure-pages.py    # the five figure markdown pages
```

`split-mc68020um.py` needs `pdftk` and `pdftotext`; `make-spec-csv.py` needs
`mutool`; `check-spec-csv.py` needs `pdftotext`. All of them read
`../MC68020UM.pdf`, which is not in this repository — see the root README.
