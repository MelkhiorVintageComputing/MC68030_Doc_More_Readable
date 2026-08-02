# MC68030 Electrical Specifications — Split Index

Source: `../MC68030EC.pdf` — Motorola `MC68030EC/D`, Rev. 1 (© 1990 Motorola), 19 pages, 561 KB.

This is the standalone **electrical specifications data sheet** for the MC68030. It is the companion the *MC68030 Enhanced 32-Bit Microprocessor User's Manual* refers you to: that manual's Section 13 (see [`../MC68030UM_split/15-section-13-electrical-characteristics.pdf`](../MC68030UM_split/15-section-13-electrical-characteristics.pdf)) gives only the maximum ratings and thermal characteristics, then states that the power considerations, DC electrical characteristics and AC timing specifications "can be found in the MC68030EC/D, MC68030 Electrical Specifications" — i.e. in this document. Being a single-section data sheet, the split below follows its own headings rather than numbered sections.

It has been split into **8 PDFs**. Page ranges are contiguous and non-overlapping and together account for all 19 source pages. Each part carries its own bookmarks (headings and figures), remapped to the new page numbering.

The source page range below refers to **PDF page numbers in the original file**. The printed page numbers run from 1 on PDF page 3, so *printed = PDF − 2*.

| # | File | Title | Source pages | Printed pages | Pages |
|---|------|-------|--------------|---------------|-------|
| 00 | [00-front-matter.pdf](00-front-matter.pdf) | Front Matter — Cover and Notices | 1–2 | — | 2 |
| 01 | [01-maximum-ratings-thermal-characteristics.pdf](01-maximum-ratings-thermal-characteristics.pdf) | Maximum Ratings and Thermal Characteristics | 3 | 1 | 1 |
| 02 | [02-power-considerations.pdf](02-power-considerations.pdf) | Power Considerations | 4 | 2 | 1 |
| 03 | [03-ac-electrical-specifications-definitions.pdf](03-ac-electrical-specifications-definitions.pdf) | AC Electrical Specifications Definitions | 5–6 | 3–4 | 2 |
| 04 | [04-dc-electrical-specifications-clock-input.pdf](04-dc-electrical-specifications-clock-input.pdf) | DC Electrical Specifications and AC Clock Input | 7 | 5 | 1 |
| 05 | [05-ac-electrical-specifications-read-write.pdf](05-ac-electrical-specifications-read-write.pdf) | AC Electrical Specifications — Read and Write Cycles | 8–11 | 6–9 | 4 |
| 06 | [06-timing-diagrams.pdf](06-timing-diagrams.pdf) | Timing Diagrams (Figures 2–8) | 12–18 | 10–16 | 7 |
| 07 | [07-back-matter.pdf](07-back-matter.pdf) | Back Matter — Literature Distribution | 19 | — | 1 |

---

## Contents of each part

### 00 — Front Matter
`00-front-matter.pdf` · 2 pages

Cover page (*Motorola Semiconductor Technical Data*, order number MC68030EC/D, Rev 1, © 1990), followed by the standard Motorola disclaimer: no liability for application or use, no patent licence conveyed, and the "not authorized for use as components in life support devices" clause.

### 01 — Maximum Ratings and Thermal Characteristics
`01-maximum-ratings-thermal-characteristics.pdf` · 1 page

Two tables plus the ESD handling note.

**Maximum Ratings** — absolute limits, not operating conditions: supply voltage V<sub>CC</sub> −0.3 to +7.0 V, input voltage V<sub>in</sub> −0.5 to +7.0 V, storage temperature −55 to +150 °C. Operating temperature is split by grade: minimum ambient T<sub>A</sub> = 0 °C for all parts, maximum **ambient** T<sub>A</sub> = 70 °C for the 40 MHz part but maximum **case** T<sub>C</sub> = 80 °C for the 50 MHz part. A footnote records that a continuous clock must be supplied to the MC68030 whenever it is powered up.

**Thermal Characteristics — PGA Package** — junction-to-ambient θ<sub>JA</sub> = 30 °C/W and junction-to-case θ<sub>JC</sub> = 15 °C/W, both marked as estimated.

The margin note is the usual caution that the device contains ESD protection but should still be handled with normal precautions, with unused inputs tied to an appropriate logic level.

### 02 — Power Considerations
`02-power-considerations.pdf` · 1 page

The thermal-design method, given as four equations: junction temperature T<sub>J</sub> = T<sub>A</sub> + (P<sub>D</sub> · θ<sub>JA</sub>); the definition P<sub>D</sub> = P<sub>INT</sub> + P<sub>I/O</sub> with the note that P<sub>I/O</sub> is usually negligible against P<sub>INT</sub>; and the constant-*K* relation that lets P<sub>D</sub> and T<sub>J</sub> be solved iteratively for any ambient temperature once *K* has been determined from a single measurement of P<sub>D</sub> at a known T<sub>A</sub>.

It then separates θ<sub>JA</sub> into θ<sub>JC</sub> + θ<sub>CA</sub> and makes the design point that θ<sub>JC</sub> is fixed by the device while θ<sub>CA</sub> is the user's to minimise — heat sinks, forced air, convection — so that good thermal management drives θ<sub>JA</sub> toward θ<sub>JC</sub> and lowers the junction temperature.

Closes with the provenance of the thermal-resistance figures (Motorola Reliability Report 7843, *Thermal Resistance Measurement Method for MC68XX Microcomponent Devices*) and the caveat that they are for design purposes only, since measured values are sensitive to procedure and setup.

### 03 — AC Electrical Specifications Definitions
`03-ac-electrical-specifications-definitions.pdf` · 2 pages

How to read every AC number in the rest of the document. The specifications are of three kinds — output delays, input setup and hold times, and signal skew times — and all are stated relative to an edge of the MC68030 clock input and, where applicable, relative to another signal.

**Figure 1, Drive Levels and Test Points for AC Specifications**, defines the measurement conditions: inputs driven to 0.8 V / 2.4 V, timing referenced at the 2.0 V and 0.8 V test points, with five separate waveform cases (output relative to rising clock edge, output relative to falling edge, input relative to rising edge, input relative to falling edge, and signal-to-signal) and six lettered measurements — A maximum output delay, B minimum output hold, C minimum input setup, D minimum input hold, E signal-valid-to-signal-valid, F signal-valid-to-signal-invalid.

An important qualification closes the section: the testing levels used to verify AC conformance do **not** affect the guaranteed DC operation of the device.

### 04 — DC Electrical Specifications and AC Clock Input
`04-dc-electrical-specifications-clock-input.pdf` · 1 page

**DC Electrical Specifications** (V<sub>CC</sub> = 5.0 V ± 5 %, GND = 0 V; 40 MHz T<sub>A</sub> = 0–70 °C, 50 MHz T<sub>A</sub> = 0 °C to T<sub>C</sub> = 80 °C) — input high/low voltage thresholds (2.0 V / 0.8 V), input leakage and high-impedance off-state leakage by signal group, output high voltage V<sub>OH</sub> = 2.4 V at I<sub>OH</sub> = 400 µA, and output low voltage V<sub>OL</sub> = 0.5 V at four different drive strengths depending on the pin group (3.2 mA for the address/data/function-code pins, 5.3 mA for the strobes, 2.0 mA for `STATUS`/`REFILL`/`CLOUT`/`ECS`/`OCS`, 10.7 mA for `RESET`). Also power dissipation (2.6 W max at T<sub>A</sub> = 0 °C), input capacitance (20 pF), and the maximum load capacitance the specs are guaranteed into — 50 pF for `ECS`/`OCS`, 70 pF for `CLOUT`/`STATUS`/`REFILL`, 130 pF for everything else.

**AC Electrical Specifications — Clock Input** (see Figure 2) — five speed grades in parallel columns: 20, 25, 33.33, 40 and 50 MHz. Gives frequency of operation (all grades run down to 12.5 MHz except the 33.33 and faster parts, which floor at 20–25 MHz), cycle time, clock pulse width measured 1.5 V to 1.5 V, and clock rise and fall times (5 ns at 20 MHz down to 2 ns at 50 MHz). The 50 MHz column is footnoted T<sub>case</sub> = 80 °C maximum.

### 05 — AC Electrical Specifications — Read and Write Cycles
`05-ac-electrical-specifications-read-write.pdf` · 4 pages

The core timing table of the data sheet, numbered specifications **#6 through #63**, spread over four pages headed *(Continued)*, *(Continued)* and *(Concluded)*. Same five speed-grade columns as the clock table, with min/max in nanoseconds for each.

Covers clock-high to function-code / size / `RMC` / `IPEND` / `CLOUT` / address valid (#6) and to `ECS`/`OCS` asserted (#6A); address and data high-impedance and invalid times (#7, #8); clock-low to `AS`/`DS` asserted and `CBREQ` valid (#9); the `AS`-to-`DS` assertion skew on reads (#9A) and `AS`-asserted-to-`DS`-asserted on writes (#9B); `ECS`/`OCS` asserted and negated widths (#10, #10A, #10B); address setup to the asserting edge of `AS` (#11); negation timings (#12, #12A, #13); and onward through data setup and hold, `DSACKx` and `BERR`/`HALT` timings, bus arbitration (`BR`, `BG`, `BGACK`), cache signals, the synchronous-input requirements (#60, #61) and finally the clock-low to `STATUS` timings (#62, #63).

Page four carries the fourteen numbered footnotes, several of which are design-relevant rather than editorial — notably #4 (which `DSACKx` the spec applies to, and what happens in its absence), #7 (minimum `ECS`/`OCS` high time when an internal cache hit is followed by an external access), #8 and #14 (specifications added specifically to guarantee correct operation with the MC68881/MC68882 floating-point coprocessor), #9 (data hold times on the output side of data buffers), and #13 (synchronous inputs must meet #60/#61 with stable logic levels at every rising clock edge).

### 06 — Timing Diagrams
`06-timing-diagrams.pdf` · 7 pages

The seven full-page waveform diagrams referenced by the tables in parts 04 and 05, one per page:

| Page | Figure |
|---|---|
| 1 | Figure 2 — Clock Input Timing Diagram |
| 2 | Figure 3 — Asynchronous Read Cycle Timing Diagram |
| 3 | Figure 4 — Asynchronous Write Cycle Timing Diagram |
| 4 | Figure 5 — Synchronous Read Cycle Timing Diagram |
| 5 | Figure 6 — Synchronous Write Cycle Timing Diagram |
| 6 | Figure 7 — Bus Arbitration Timing Diagram |
| 7 | Figure 8 — Other Signal Timings |

Each diagram places the numbered specifications from part 05 against the waveforms, so the two parts are meant to be read side by side.

### 07 — Back Matter
`07-back-matter.pdf` · 1 page

Motorola literature distribution addresses for the USA (Phoenix, Arizona), Europe (Milton Keynes, England), Asia Pacific (Kowloon, Hong Kong) and Japan (Minato-ku, Tokyo), with the document number MC68030EC/D repeated.

---

## Machine-readable specifications

Two CSVs, because the AC and DC tables have genuinely different shapes — the AC tables are indexed by numbered specification and speed grade, the DC table by characteristic and signal group.

| File | Covers | Rows |
|---|---|---|
| [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv) | AC clock-input table (part 04) + AC read-and-write-cycle table (part 05) | 77 |
| [`dc-electrical-specifications.csv`](dc-electrical-specifications.csv) | DC electrical specifications table (part 04) | 15 |

### Redrawn figures

All seven figures have been redrawn as scalable SVG. Each has a markdown page carrying the diagram plus the specifications marked on it.

| Page | Figure | Signals | Callouts |
|---|---|--:|--:|
| [`figure-02-clock-input-timing.md`](figure-02-clock-input-timing.md) | Clock Input Timing Diagram | 1 | 5 |
| [`figure-03-asynchronous-read-cycle.md`](figure-03-asynchronous-read-cycle.md) | Asynchronous Read Cycle | 17 | 33 |
| [`figure-04-asynchronous-write-cycle.md`](figure-04-asynchronous-write-cycle.md) | Asynchronous Write Cycle | 15 | 34 |
| [`figure-05-synchronous-read-cycle.md`](figure-05-synchronous-read-cycle.md) | Synchronous Read Cycle | 16 | 17 |
| [`figure-06-synchronous-write-cycle.md`](figure-06-synchronous-write-cycle.md) | Synchronous Write Cycle | 15 | 20 |
| [`figure-07-bus-arbitration.md`](figure-07-bus-arbitration.md) | Bus Arbitration | 16 | 8 |
| [`figure-08-other-signal-timings.md`](figure-08-other-signal-timings.md) | Other Signal Timings | 6 | 5 |

**Why SVG.** It is the only diagram format that survives GitHub's markdown pipeline. GitHub renders Mermaid, but Mermaid has no timing or waveform diagram type at all; it does not render WaveDrom, the usual choice for digital timing in markdown; and it strips inline `<svg>` from markdown. A plain `.svg` file referenced as an ordinary image works everywhere, scales, and adapts to light and dark themes.

**How they are built.**

| Script | Produces |
|---|---|
| [`timingsvg.py`](timingsvg.py) | the renderer — a small timing-diagram engine (clock, two-level signals, valid/high-impedance buses, numbered dimension callouts) |
| [`make-figure-svg.py`](make-figure-svg.py) | figures 3–8, from a declarative description of each |
| [`make-figure-tables.py`](make-figure-tables.py) | the specification table inside every `figure-*.md`, from the CSVs |
| [`make-figure-pages.py`](make-figure-pages.py) | the figure-3–8 markdown pages themselves |

Figure 2's SVG is hand-authored rather than generated — it is the only figure that is about edge shape rather than signal sequencing, so it does not fit the engine's model.

Each page's table sits between `BEGIN TABLE` / `END TABLE` comments and is generated from [`ac-electrical-specifications.csv`](ac-electrical-specifications.csv), so a figure page cannot drift from the extracted data. Naming a specification number that does not exist in the CSV is a hard error rather than a silently dropped row.

**Fidelity.** Waveform transitions were measured off the 300 dpi scans against the state grid printed in each figure; callout anchors follow what each specification actually measures, per its description in the CSV. Horizontal placement is nonetheless schematic — as it is in the source, which has no time axis, exaggerates every edge ramp and is not to scale in any dimension. The figures are authoritative for *ordering* and for *which edges a specification is measured between*; the numbers come from the table.

Both were produced by the same method and subjected to the same checks; see [How the values were obtained](#how-the-values-were-obtained).

### DC table

Columns: `pdf_page, printed_page, characteristic, condition, signals, symbol, min, max, unit, confidence, note`.

Measured under the table's stated conditions: **V<sub>CC</sub> = 5.0 Vdc ± 5 %, GND = 0 Vdc, 40 MHz T<sub>A</sub> = 0–70 °C, 50 MHz T<sub>A</sub> = 0 °C to T<sub>C</sub> = 80 °C.**

- **Two limits are symbolic, not numeric**: V<sub>IH</sub> max is `VCC`, and V<sub>IL</sub> min is `GND-0.5` (printed on two lines in the source as `GND` / `−0.5`).
- **Four rows in the source carry several signal groups under one heading**, and are expanded to one CSV row per group: *Input Leakage Current* (±2.5 µA for the normal inputs, ±20 µA for `HALT`/`RESET`), *Output Low Voltage* (four different I<sub>OL</sub> drive strengths, all with the same 0.5 V limit), and *Load Capacitance* (50 / 70 / 130 pF).
- An empty `min` or `max` means the source prints an em dash — that limit is not specified.
- All 15 rows are `confidence = high`; every numeric value was read at 3× zoom and every one is corroborated by the text layer.

### AC tables

Columns: `table, pdf_page, printed_page, num, footnotes, characteristic, condition, unit,` `f20_min, f20_max, f25_min, f25_max, f33_min, f33_max, f40_min, f40_max, f50_min, f50_max,` `confidence, note` — **536 populated value cells**, one row per numbered specification with min and max for each of the five speed grades.

Columns: `table, pdf_page, printed_page, num, footnotes, characteristic, condition, unit,` `f20_min, f20_max, f25_min, f25_max, f33_min, f33_max, f40_min, f40_max, f50_min, f50_max,` `confidence, note`.

- An **empty value cell means the source prints an em dash** — no limit specified for that grade — not missing data.
- `table` is `clock` (part 04) or `read-write` (part 05); `num` is the specification number as printed (`6`, `6A`, `9B`, …); `footnotes` lists the superscripts attached to it in the Num column.
- Specs **19, 36, 38, 49–52 and 54 do not exist** — the source numbering skips them. Verified against the page images, not inferred.
- `condition` is used only for **#45** and **#45A**, which each carry two value rows under one heading (asynchronous/synchronous read vs. write). Note the source's typography puts each sub-condition's *label* one line below its *values*; the mapping in the CSV is read→first row, write→second row, corroborated by footnote 9.
- Overbars are lost in both files: `AS`, `DS`, `ECS`, `DSACKx` etc. are active-low in the original.

### A signal-name trap

The PDF text layer consistently renders the MC68030's **`CIOUT`** (cache inhibit out) as **`CLOUT`** — the capital I is read as an L. It appears that way in the DC table's V<sub>OH</sub> and C<sub>L</sub> rows and throughout the AC table. There is no `CLOUT` signal on this part; both CSVs use the correct `CIOUT`. Worth knowing if you grep the text layer directly.

### How the values were obtained

The PDF's own OCR layer is not trustworthy for this table, so the numbers were **read off the page images directly** rather than copied from the text layer. Each page was rendered with `pdftoppm -r 300` and read in overlapping full-width bands at roughly 1:1 with the 300 dpi scan.

Every value then had to survive three independent checks:

1. **Visual read** of the rendered page image.
2. **Corroboration against the PDF text layer** — not positionally (the text layer drops and invents dashes, so alignment cascades), but by testing whether the visually-read numbers appear as an ordered subsequence of the numeric tokens OCR emits for that row. 65 of 76 rows matched outright; the 11 that did not were inspected individually. Nine were artefacts of tokenising (`3.`, `45.`, `50` split as `5 0`, `1.5` flattened to `115`). Two were genuine OCR failures where the text layer dropped a leading `1` — **#6A** at 25 MHz (`15` read as `5`) and **#20** at 40 MHz (`14` read as `4`) — both re-checked at 3× zoom and resolved in favour of the image.
3. **Monotonicity across speed grades** — a timing limit should not get looser as the part gets faster. Exactly two rows broke this, and both were examined: **#9A** is a signed skew window whose min column legitimately tightens toward zero, and **#48** is the genuine anomaly described below. (This check applies only to the AC tables; the DC table has no speed-grade axis, so every DC value was instead read at 3× zoom individually — all 15 rows, and all of them corroborated by the text layer.)

### An anomaly in the source: specification #48

Every value in both CSVs is `confidence = high`. One is nevertheless worth knowing about, because it is odd in the *source document* rather than in the transcription:

> **#48 — `DSACKx` Asserted to `BERR`, `HALT` Asserted (max)**
>
> | | 20 MHz | 25 MHz | 33.33 MHz | 40 MHz | 50 MHz |
> |---|--:|--:|--:|--:|--:|
> | max (ns) | **20** | **25** | 18 | 14 | 13 |
>
> The 20 MHz limit (20 ns) is *tighter* than the 25 MHz limit (25 ns), so the sequence rises before falling. This is **the only non-monotonic limit anywhere in the AC tables** — every other specification gets tighter, or stays equal, as the speed grade increases.
>
> The transcription has been confirmed against the printed document: the digits are what the datasheet says. So this is either an error in the original `MC68030EC/D` or a deliberate exception that the datasheet does not explain — the row carries only footnote 4, which concerns *which* `DSACKx` signal the specification applies to, and says nothing about the limits themselves.
>
> The 3× crop used to verify it is kept as [`check-spec-48.png`](check-spec-48.png). Treat the 20 MHz figure with care if you are designing to it.

Apart from that anomaly, every value in both tables passed all applicable checks.

---

## Notes on the split

- The source is **unencrypted** and was produced by PageGenie PDFGenerator from scanned TIFFs; pages are 507 × 665 pt. There is an OCR text layer, but it is noticeably noisier than in the two programmer's manuals — numerals in the timing tables in particular are unreliable when copied as text. **Read the values off the page image, not the text layer.**
- Page 7 is not split further even though it carries two headings (DC specifications and the AC clock-input table), because both begin and end on that page.
- The source's `LIST OF ILLUSTRATIONS` bookmark is a navigational container that points at the front of the document rather than at any content of its own; it was dropped, and the figure bookmarks it grouped were promoted to top level inside the parts that actually contain them.
- Bookmark levels were re-based per part, so each file's outline starts at level 1. This avoids the blank placeholder entries pdftk inserts when an outline begins below level 1.
- Verified after splitting: 2 + 1 + 1 + 2 + 1 + 4 + 7 + 1 = **19 pages**, matching the source exactly; every part opens cleanly under `mutool`; and no part contains an empty bookmark.

### Reproducing the split

```sh
pdftk MC68030EC.pdf cat 12-18 output 06-timing-diagrams.pdf
```

Bookmarks and the document title were then reinjected per part with `pdftk <part> update_info - output <part>.tmp`, feeding a remapped `dump_data` block on standard input.
