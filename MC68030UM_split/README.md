# MC68030 Enhanced 32-Bit Microprocessor User's Manual — Split Index

Source: `../MC68030UM.pdf` — Motorola `MC68030UM/AD`, Rev. 2 (© 1990 Motorola, published by Prentice-Hall), 599 pages, 21 MB.

The manual has been split into **19 PDFs**, one per front-matter part, numbered section, appendix, and the index. Page ranges are contiguous and non-overlapping, and together account for all 599 source pages. Each section file keeps its own bookmark tree (subsections, tables, and figures), remapped to the new page numbering, so the parts remain navigable on their own.

The source page range below refers to **PDF page numbers in the original file**, not the printed page numbers on the page (the front matter is Roman-numbered, and each section restarts its printed numbering at *n*-1).

| # | File | Title | Source pages | Pages |
|---|------|-------|--------------|-------|
| 00 | [00-front-matter.pdf](00-front-matter.pdf) | Front Matter | 1–4 | 4 |
| 01 | [01-table-of-contents.pdf](01-table-of-contents.pdf) | Table of Contents | 5–27 | 23 |
| 02 | [02-preface.pdf](02-preface.pdf) | Preface | 28–29 | 2 |
| 03 | [03-section-01-introduction.pdf](03-section-01-introduction.pdf) | Section 1 — Introduction | 30–45 | 16 |
| 04 | [04-section-02-data-organization-and-addressing.pdf](04-section-02-data-organization-and-addressing.pdf) | Section 2 — Data Organization and Addressing Capabilities | 46–85 | 40 |
| 05 | [05-section-03-instruction-set-summary.pdf](05-section-03-instruction-set-summary.pdf) | Section 3 — Instruction Set Summary | 86–117 | 32 |
| 06 | [06-section-04-processing-states.pdf](06-section-04-processing-states.pdf) | Section 4 — Processing States | 118–125 | 8 |
| 07 | [07-section-05-signal-description.pdf](07-section-05-signal-description.pdf) | Section 5 — Signal Description | 126–137 | 12 |
| 08 | [08-section-06-on-chip-cache-memories.pdf](08-section-06-on-chip-cache-memories.pdf) | Section 6 — On-Chip Cache Memories | 138–161 | 24 |
| 09 | [09-section-07-bus-operation.pdf](09-section-07-bus-operation.pdf) | Section 7 — Bus Operation | 162–267 | 106 |
| 10 | [10-section-08-exception-processing.pdf](10-section-08-exception-processing.pdf) | Section 8 — Exception Processing | 268–301 | 34 |
| 11 | [11-section-09-memory-management-unit.pdf](11-section-09-memory-management-unit.pdf) | Section 9 — Memory Management Unit | 302–387 | 86 |
| 12 | [12-section-10-coprocessor-interface.pdf](12-section-10-coprocessor-interface.pdf) | Section 10 — Coprocessor Interface Description | 388–463 | 76 |
| 13 | [13-section-11-instruction-execution-timing.pdf](13-section-11-instruction-execution-timing.pdf) | Section 11 — Instruction Execution Timing | 464–525 | 62 |
| 14 | [14-section-12-applications-information.pdf](14-section-12-applications-information.pdf) | Section 12 — Applications Information | 526–571 | 46 |
| 15 | [15-section-13-electrical-characteristics.pdf](15-section-13-electrical-characteristics.pdf) | Section 13 — Electrical Characteristics | 572–573 | 2 |
| 16 | [16-section-14-ordering-info-and-mechanical-data.pdf](16-section-14-ordering-info-and-mechanical-data.pdf) | Section 14 — Ordering Information and Mechanical Data | 574–579 | 6 |
| 17 | [17-appendix-a-m68000-family-summary.pdf](17-appendix-a-m68000-family-summary.pdf) | Appendix A — M68000 Family Summary | 580–583 | 4 |
| 18 | [18-index.pdf](18-index.pdf) | Index | 584–599 | 16 |

---

## Contents of each part

### 00 — Front Matter
`00-front-matter.pdf` · 4 pages

Cover and title pages, Motorola/Prentice-Hall copyright and publication notice, and the trademark and disclaimer boilerplate.

### 01 — Table of Contents
`01-table-of-contents.pdf` · 23 pages

The full paragraph-level table of contents for all fourteen sections and the appendix, followed by the List of Illustrations and the List of Tables. Useful as a standalone lookup for locating a topic before opening the corresponding section file.

### 02 — Preface
`02-preface.pdf` · 2 pages

Describes the scope of the manual and lists its sections. Defines the *assertion*/*negation* signal terminology used throughout (independent of the voltage level representing the state), and gives reading paths by audience: systems designers (Sections 1, 5, 6, 7, 13, 14, Appendix A, plus Section 10 for coprocessor implementers), systems programmers (1, 2, 3, 4, 6, 8, 9, 11, Appendix A), and applications programmers (1, 2, 3, 4, 9, 11, 12, Appendix A). Points to `M68000PM/AD`, the *M68000 Family Programmer's Reference Manual*, for detailed instruction descriptions.

### 03 — Section 1: Introduction
`03-section-01-introduction.pdf` · 16 pages

Overview of the MC68030 as a second-generation full 32-bit processor combining a CPU core, separate instruction and data caches, an enhanced bus controller, and an on-chip MMU. Covers the feature list and the extensions over earlier M68000 Family parts; the user and supervisor programming models and the status register; data types and the addressing-mode summary; an instruction set overview; virtual memory and virtual machine concepts; and short introductions to the MMU, the three-stage pipelined architecture, and the two caches. Contains the block diagram (Figure 1-1) and the addressing-mode and instruction-set summary tables.

**Subsections:** 1.1 Features · 1.2 MC68030 Extensions to the M68000 Family · 1.3 Programming Model · 1.4 Data Types and Addressing Modes · 1.5 Instruction Set Overview · 1.6 Virtual Memory and Virtual Machine Concepts · 1.7 The Memory Management Unit · 1.8 Pipelined Architecture · 1.9 The Cache Memories

### 04 — Section 2: Data Organization and Addressing Capabilities
`04-section-02-data-organization-and-addressing.pdf` · 40 pages

How operands are represented and reached. Covers instruction operands; the organization of data in the integer, address, and control registers and in memory (byte/word/long-word alignment, BCD and packed formats, bit and bit-field operands); and the complete set of addressing modes — register direct, register indirect with all its post/pre-increment and displacement variants, the memory-indirect and scaled-index modes, PC-relative, absolute, and immediate. Includes the effective-address encoding summary tables, a programmer's-eye view of mode usage, notes on addressing compatibility across the M68000 Family, and the standard data structures (stacks and queues).

**Subsections:** 2.1 Instruction Operands · 2.2 Organization of Data in Registers · 2.3 Organization of Data in Memory · 2.4 Addressing Modes · 2.5 Effective Address Encoding Summary · 2.6 Programmer's View of Addressing Modes · 2.7 M68000 Family Addressing Compatibility · 2.8 Other Data Structures

### 05 — Section 3: Instruction Set Summary
`05-section-03-instruction-set-summary.pdf` · 32 pages

Summary-level reference for the instruction set: the general instruction format and operand-extension words, the instruction summary tables grouped by category (data movement, integer and BCD arithmetic, logical and shift/rotate, bit and bit-field, program control, system control, MMU, multiprocessor, and coprocessor instructions), the integer condition codes and how each instruction affects the CCR, and a set of worked instruction examples. This is a summary — full per-instruction descriptions live in `M68000PM/AD`.

**Subsections:** 3.1 Instruction Format · 3.2 Instruction Summary · 3.3 Integer Condition Codes · 3.4 Instruction Set Summary · 3.5 Instruction Examples

### 06 — Section 4: Processing States
`06-section-04-processing-states.pdf` · 8 pages

The processor's normal, exception-processing, and halted states, and the transitions between them. Describes the user/supervisor privilege levels and how the processor changes between them, the master and interrupt stack pointers, and the address space types selected by the function codes (user/supervisor program and data, plus CPU space). Introduces exception processing — the bits of the supervisor portion of the status register, exception vectors and the vector table, and the general response to an exception — with the detailed treatment deferred to Section 8.

**Subsections:** 4.1 Privilege Levels · 4.2 Address Space Types · 4.3 Exception Processing

### 07 — Section 5: Signal Description
`07-section-05-signal-description.pdf` · 12 pages

Pin-by-pin reference for every external signal. Covers the function code outputs FC0–FC2, the A0–A31 address bus and D0–D31 data bus, the SIZ0/SIZ1 transfer size encodings, and then each control group in turn: bus control, cache control (CIIN, CIOUT, CBREQ, CBACK), interrupt control (IPL0–IPL2, IPEND, AVEC), bus arbitration (BR, BG, BGACK), bus exception control (RESET, HALT, BERR), the emulator-support signals (STATUS and REFILL), the clock, and the power and ground connections. Ends with the signal summary table giving direction and active state for all signals.

**Subsections:** 5.1 Signal Index · 5.2 Function Code Signals (FC0–FC2) · 5.3 Address Bus (A0–A31) · 5.4 Data Bus (D0–D31) · 5.5 Transfer Size Signals (SIZ0, SIZ1) · 5.6 Bus Control Signals · 5.7 Cache Control Signals · 5.8 Interrupt Control Signals · 5.9 Bus Arbitration Control Signals · 5.10 Bus Exception Control Signals · 5.11 Emulator Support Signals · 5.12 Clock (CLK) · 5.13 Power Supply Connections · 5.14 Signal Summary

### 08 — Section 6: On-Chip Cache Memories
`08-section-06-on-chip-cache-memories.pdf` · 24 pages

The 256-byte instruction cache and 256-byte data cache, both accessed by logical (virtual) addresses. Explains how the caches raise performance both by freeing the external bus for other masters and by allowing instruction and data accesses to proceed simultaneously on separate internal buses. Covers the organization and operation of each cache (line and entry format, tags, validity, hit/miss handling), the write-through policy and write allocation of the data cache, burst-mode filling via CBREQ/CBACK, single-entry and full-cache invalidation, cache behaviour on reset, and cache control through the CACR and CAAR registers and the external cache-control signals.

**Subsections:** 6.1 On-Chip Cache Organization and Operation · 6.2 Cache Reset · 6.3 Cache Control

### 09 — Section 7: Bus Operation
`09-section-07-bus-operation.pdf` · 106 pages

The largest section: the complete external bus protocol, heavily illustrated with timing diagrams and flowcharts. Covers the bus transfer signals and the dynamic bus sizing / operand transfer mechanism (misaligned and multi-part transfers, byte enables); the individual data transfer cycles — asynchronous and synchronous read, write, and read-modify-write, plus burst operation; CPU space cycles (interrupt acknowledge, breakpoint acknowledge, coprocessor communication); the bus exception control cycles for bus error, retry, halt, and double bus fault; bus synchronization; the three-wire bus arbitration protocol and bus grant/relinquish timing; and reset operation, both externally applied and RESET-instruction driven.

**Subsections:** 7.1 Bus Transfer Signals · 7.2 Data Transfer Mechanism · 7.3 Data Transfer Cycles · 7.4 CPU Space Cycles · 7.5 Bus Exception Control Cycles · 7.6 Bus Synchronization · 7.7 Bus Arbitration · 7.8 Reset Operation

### 10 — Section 8: Exception Processing
`10-section-08-exception-processing.pdf` · 34 pages

Detailed treatment of what the processor does in preparing to run an exception handler (the handler itself is not part of exception processing). Walks the exception processing sequence and then each exception type in turn — reset, bus error, address error, instruction traps, illegal and unimplemented instructions, privilege violations, tracing, interrupts (including autovectored and spurious), format error, breakpoints, and the multiple-exception priority ordering. Covers returning from an exception via RTE, bus fault recovery and the completion of faulted accesses, coprocessor-related considerations, and the layout of every exception stack frame format. MMU-specific and coprocessor-specific exceptions are cross-referenced to Sections 9 and 10.

**Subsections:** 8.1 Exception Processing Sequence · 8.2 Bus Fault Recovery · 8.3 Coprocessor Considerations · 8.4 Exception Stack Frame Formats

### 11 — Section 9: Memory Management Unit
`11-section-09-memory-management-unit.pdf` · 86 pages

The on-chip paged MMU. Describes the translation table structure and the multi-level tree search, the address translation process, the transparent translation registers (TT0/TT1) that bypass translation for selected address ranges, and the 22-entry address translation cache (ATC) with its tag and entry formats. Details the descriptor formats at every table level, the differences between the MC68030 MMU and the external MC68851 PMMU, the MMU register set (CRP, SRP, TC, TT0, TT1, MMUSR), and the MMU instructions (PMOVE, PTEST, PLOAD, PFLUSH). Closes with practical guidance on defining and using page tables in an operating system, plus a worked paging-implementation example.

**Subsections:** 9.1 Translation Table Structure · 9.2 Address Translation · 9.3 Transparent Translation · 9.4 Address Translation Cache · 9.5 Translation Table Details · 9.6 MC68030 and MC68851 MMU Differences · 9.7 Registers · 9.8 MMU Instructions · 9.9 Defining and Using Page Tables in an Operating System · 9.10 An Example of Paging Implementation in an Operating System

### 12 — Section 10: Coprocessor Interface Description
`12-section-10-coprocessor-interface.pdf` · 76 pages

The M68000 coprocessor interface as implemented by the MC68030, written for designers building a coprocessor. Explains the coprocessor concept and how it extends the main processor without changing its architecture; the coprocessor instruction types (general, conditional, and the save/restore context instructions); the coprocessor interface register set (CIR) and the CPU-space protocol used to access it; the full set of coprocessor response primitives and the processor's action for each; coprocessor-related exceptions including protocol violations, F-line emulation, and mid-instruction stack frames; and a concluding summary of the interface.

**Subsections:** 10.1 Introduction · 10.2 Coprocessor Instruction Types · 10.3 Coprocessor Interface Register Set · 10.4 Coprocessor Response Primitives · 10.5 Exceptions · 10.6 Coprocessor Summary

### 13 — Section 11: Instruction Execution Timing
`13-section-11-instruction-execution-timing.pdf` · 62 pages

Execution timing expressed in external clock cycles — accurate guidelines rather than exact figures, since real timings depend on memory speed and other variables. Discusses the performance tradeoffs and resource scheduling of the pipelined architecture (overlap, concurrency, and the sources of stalls), then how to perform timing calculations, and the effects of the data cache and of wait states. Contains the bulk instruction timing tables (cache-case and no-cache-case, per instruction and addressing mode), address translation tree search timing, and the interrupt latency and bus arbitration latency figures needed for real-time and multitasking analysis.

**Subsections:** 11.1 Performance Tradeoffs · 11.2 Resource Scheduling · 11.3 Instruction Execution Timing Calculations · 11.4 Effect of Data Cache · 11.5 Effect of Wait States · 11.6 Instruction Timing Tables · 11.7 Address Translation Tree Search Timing · 11.8 Interrupt Latency · 11.9 Bus Arbitration Latency

### 14 — Section 12: Applications Information
`14-section-12-applications-information.pdf` · 46 pages

Practical design guidance. Covers adapting the MC68030 to an existing MC68020 design (possible because the two asynchronous buses are fully compatible) and how to configure an adapter; using the MC68881 and MC68882 floating-point coprocessors; byte select logic; memory interface design and access time calculations; building static RAM memory banks (including two-clock synchronous and burst-mode designs); external caches; debugging aids based on the STATUS and REFILL signals; and power and ground distribution and decoupling considerations.

**Subsections:** 12.1 Adapting the MC68030 to MC68020 Designs · 12.2 Floating-Point Units · 12.3 Byte Select Logic for the MC68030 · 12.4 Memory Interface · 12.5 Static RAM Memory Banks · 12.6 External Caches · 12.7 Debugging Aids · 12.8 Power and Ground Considerations

### 15 — Section 13: Electrical Characteristics
`15-section-13-electrical-characteristics.pdf` · 2 pages

Maximum ratings and thermal characteristics for the PGA package. Note that this section is deliberately brief — it directs readers to `MC68030EC/D`, *MC68030 Electrical Specifications*, for power considerations, DC electrical characteristics, and AC timing specifications.

**Subsections:** 13.1 Maximum Ratings · 13.2 Thermal Characteristics — PGA Package

### 16 — Section 14: Ordering Information and Mechanical Data
`16-section-14-ordering-info-and-mechanical-data.pdf` · 6 pages

Standard ordering information (part numbers by speed grade and package), the pin assignment diagrams for both the pin grid array (RC suffix) and the ceramic surface mount (FE suffix) packages, and the mechanical package dimension drawings.

**Subsections:** 14.1 Standard MC68030 Ordering Information · 14.2 Pin Assignments — Pin Grid Array (RC Suffix) · 14.3 Pin Assignments — Ceramic Surface Mount (FE Suffix) · 14.4 Package Dimensions

### 17 — Appendix A: M68000 Family Summary
`17-appendix-a-m68000-family-summary.pdf` · 4 pages

A comparison table of the characteristics of the M68000 Family processors — MC68000, MC68008, MC68010, MC68020, and MC68030 — covering data and address bus widths, instruction and data caches, addressing modes, register complement, memory management, and word/long-word alignment. Refers to the *M68000 Programmer's Reference Manual* for the detailed MC68000/MC68010 differences.

### 18 — Index
`18-index.pdf` · 16 pages

The alphabetical subject index for the whole manual. Entries reference **printed** page numbers in section-relative form (e.g. `9-86`, `2-20`, `12-14–12-17`), so use the section number to pick the right file from the table above, then the printed page number within it.

---

## How this was produced

Split with `pdftk` on the boundaries given by the PDF's own level-2 bookmarks (verified against the section title pages via `pdftotext`), then each part's sub-bookmarks were remapped to local page numbers and reattached with `pdftk update_info`. Every part was checked to open cleanly, and the per-part page counts sum to exactly the 599 pages of the source.

```
pdftk MC68030UM.pdf cat <first>-<last> output <part>.pdf
pdftk <part>.pdf update_info <part>.info output <part>-with-bookmarks.pdf
```
