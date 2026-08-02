# M68000 Family Programmer's Reference Manual — Split Index

Source: `../M68000PRM.pdf` — Motorola *M68000 Family Programmer's Reference Manual (Includes CPU32 Instructions)*, © Motorola Inc. 1992, 646 pages, 4.7 MB.

This is the companion volume referenced throughout the MC68030 User's Manual (as `M68000PM/AD`) for per-instruction detail. It covers the whole family — MC68000/68008/68010, MC68020, MC68030, MC68040, the MC68881/MC68882 floating-point coprocessors, the MC68851 PMMU, and the CPU32.

The manual has been split into **15 PDFs**, one per front-matter part, numbered section, and appendix. Page ranges are contiguous and non-overlapping and account for all 646 source pages. This manual has **no index**; it ends with Appendix C.

Page ranges below are **PDF page numbers in the original file**, not the printed page numbers (the front matter is Roman-numbered and each section restarts its printed numbering at *n*-1).

| # | File | Title | Source pages | Pages |
|---|------|-------|--------------|-------|
| 00 | [00-front-matter.pdf](00-front-matter.pdf) | Front Matter | 1–2 | 2 |
| 01 | [01-table-of-contents.pdf](01-table-of-contents.pdf) | Table of Contents | 3–7 | 5 |
| 02 | [02-list-of-figures.pdf](02-list-of-figures.pdf) | List of Figures | 8–9 | 2 |
| 03 | [03-list-of-tables.pdf](03-list-of-tables.pdf) | List of Tables | 10–11 | 2 |
| 04 | [04-section-01-introduction.pdf](04-section-01-introduction.pdf) | Section 1 — Introduction | 12–41 | 30 |
| 05 | [05-section-02-addressing-capabilities.pdf](05-section-02-addressing-capabilities.pdf) | Section 2 — Addressing Capabilities | 42–71 | 30 |
| 06 | [06-section-03-instruction-set-summary.pdf](06-section-03-instruction-set-summary.pdf) | Section 3 — Instruction Set Summary | 72–104 | 33 |
| 07 | [07-section-04-integer-instructions.pdf](07-section-04-integer-instructions.pdf) | Section 4 — Integer Instructions | 105–302 | 198 |
| 08 | [08-section-05-floating-point-instructions.pdf](08-section-05-floating-point-instructions.pdf) | Section 5 — Floating-Point Instructions | 303–454 | 152 |
| 09 | [09-section-06-supervisor-instructions.pdf](09-section-06-supervisor-instructions.pdf) | Section 6 — Supervisor (Privileged) Instructions | 455–540 | 86 |
| 10 | [10-section-07-cpu32-instructions.pdf](10-section-07-cpu32-instructions.pdf) | Section 7 — CPU32 Instructions | 541–556 | 16 |
| 11 | [11-section-08-instruction-format-summary.pdf](11-section-08-instruction-format-summary.pdf) | Section 8 — Instruction Format Summary | 557–596 | 40 |
| 12 | [12-appendix-a-processor-instruction-summary.pdf](12-appendix-a-processor-instruction-summary.pdf) | Appendix A — Processor Instruction Summary | 597–627 | 31 |
| 13 | [13-appendix-b-exception-processing-reference.pdf](13-appendix-b-exception-processing-reference.pdf) | Appendix B — Exception Processing Reference | 628–640 | 13 |
| 14 | [14-appendix-c-s-record-output-format.pdf](14-appendix-c-s-record-output-format.pdf) | Appendix C — S-Record Output Format | 641–646 | 6 |

Sections 4–7 are the bulk of the manual (452 of 646 pages) and are pure alphabetical instruction references, **175 instruction descriptions** in total.

**See also:** [`INSTRUCTIONS-BY-CPU.md`](INSTRUCTIONS-BY-CPU.md) — which instructions each processor and coprocessor in the family supports, built from Appendix A's Table A-1 and cross-checked against the per-processor tables and the section 4/5/6 instruction headers, with the documentation discrepancies that check turned up.

---

## Contents of each part

### 00 — Front Matter
`00-front-matter.pdf` · 2 pages

Blank leading page and the title page (Motorola, *M68000 Family Programmer's Reference Manual*, 1992).

### 01 — Table of Contents
`01-table-of-contents.pdf` · 5 pages

Paragraph-level contents for all eight sections and the three appendices. Note that the alphabetical instruction descriptions in Sections 4–7 are *not* itemised here — use the per-instruction bookmarks in those files, or the mnemonic lists below, to locate an instruction.

### 02 — List of Figures
`02-list-of-figures.pdf` · 2 pages

Numbered list of all figures with their printed page numbers.

### 03 — List of Tables
`03-list-of-tables.pdf` · 2 pages

Numbered list of all tables with their printed page numbers.

### 04 — Section 1: Introduction
`04-section-01-introduction.pdf` · 30 pages

The programming models and data formats shared across the family. Covers the integer unit user programming model (data registers, address registers, PC, condition code register); the floating-point unit user programming model (FP data registers and the FPCR, FPSR, and FPIAR); and the supervisor programming model (status register, vector base register, alternate function code registers, MMU status register, and the transparent translation / access control registers). Then the data formats: integer formats, the packed decimal real and binary floating-point formats, and the floating-point data types — normalized and denormalized numbers, zeros, infinities, and NaNs — with a format and type summary. Ends with the organization of integer and FPU data in registers and in memory.

**Subsections:** 1.1 Integer Unit User Programming Model · 1.2 Floating-Point Unit User Programming Model · 1.3 Supervisor Programming Model · 1.4 Integer Data Formats · 1.5 Floating-Point Data Formats · 1.6 Floating-Point Data Types · 1.7 Organization of Data in Registers

### 05 — Section 2: Addressing Capabilities
`05-section-02-addressing-capabilities.pdf` · 30 pages

The instruction format and the complete set of effective addressing modes, each described individually with its assembler syntax and effective-address computation: register direct (data and address), address register indirect and its postincrement, predecrement, displacement, and index variants, memory indirect postindexed and preindexed, the corresponding PC-relative forms, absolute short and long, and immediate data. Followed by the effective addressing mode summary tables, brief extension word format compatibility across family members, the full extension word format (with and without memory indirect action), and the standard data structures — the system stack and queues.

**Subsections:** 2.1 Instruction Format · 2.2 Effective Addressing Modes (18 modes) · 2.3 Effective Addressing Mode Summary · 2.4 Brief Extension Word Format Compatibility · 2.5 Full Extension Addressing Modes · 2.6 Other Data Structures

### 06 — Section 3: Instruction Set Summary
`06-section-03-instruction-set-summary.pdf` · 33 pages

Overview of the instruction set in Motorola assembly syntax and notation, grouped by category, plus the floating-point semantics that the individual instruction descriptions assume. Covers the instruction summary tables for data movement, integer arithmetic, logical, shift and rotate, bit manipulation, bit field, BCD, program control, system control, cache control, multiprocessor, MMU, and floating-point arithmetic instructions; integer unit condition code computation; worked examples (CAS/CAS2, MOVES, nested subroutine calls, bit field operations, pipeline synchronization with NOP); and floating-point computational accuracy — intermediate result format, rounding, and the postprocessing step applied to arithmetic results.

**Subsections:** 3.1 Instruction Summary · 3.2 Integer Unit Condition Code Computation · 3.3 Instruction Examples · 3.4 Floating-Point Instruction Details · 3.5 Floating-Point Computational Accuracy · 3.6 Floating-Point Postprocessing · 3.7 Instruction Descriptions

### 07 — Section 4: Integer Instructions
`07-section-04-integer-instructions.pdf` · 198 pages — **the largest part**

Detailed descriptions of the integer instructions, alphabetical by mnemonic. Each entry gives the operation, assembler syntax, attributes (sizes), a prose description, condition code effects, and the binary instruction format with field encodings, along with the family members that support it. **97 entries:**

> ABCD, ADD, ADDA, ADDI, ADDQ, ADDX, AND, ANDI, ANDI to CCR, ASL, ASR, Bcc, BCHG, BCLR, BFCHG, BFCLR, BFEXTS, BFEXTU, BFFFO, BFINS, BFSET, BFTST, BKPT, BRA, BSET, BSR, BTST, CALLM, CAS, CAS2, CHK, CHK2, CLR, CMP, CMPA, CMPI, CMPM, CMP2, cpBcc, cpDBcc, cpGEN, cpScc, cpTRAPcc, DBcc, DIVS, DIVSL, DIVU, DIVUL, EOR, EORI, EORI to CCR, EXG, EXT, EXTB, ILLEGAL, JMP, JSR, LEA, LINK, LSL, LSR, MOVE, MOVEA, MOVE from CCR, MOVE to CCR, MOVE from SR, MOVE16, MOVEM, MOVEP, MOVEQ, MULS, MULU, NBCD, NEG, NEGX, NOP, NOT, OR, ORI, ORI to CCR, PACK, PEA, ROL, ROR, ROXL, ROXR, RTD, RTM, RTR, RTS, SBCD, Scc, SUB, SUBA, SUBI, SUBQ, SUBX, SWAP, TAS, TRAP, TRAPcc, TRAPV, TST, UNLK, UNPK

### 08 — Section 5: Floating-Point Instructions
`08-section-05-floating-point-instructions.pdf` · 152 pages

Detailed descriptions of the floating-point instructions for the MC68881, MC68882, and MC68040 (references to the MC68040 exclude the MC68LC040 and MC68EC040), alphabetical by mnemonic. Covers the arithmetic and transcendental operations, data movement, and FP program control. **45 entries:**

> FABS, FACOS, FADD, FASIN, FATAN, FATANH, FBcc, FCMP, FCOS, FCOSH, FDBcc, FDIV, FETOX, FETOXM1, FGETEXP, FGETMAN, FINT, FINTRZ, FLOG10, FLOG2, FLOGN, FLOGNP1, FMOD, FMOVE, FMOVECR, FMOVEM, FMUL, FNEG, FNOP, FREM, FSCALE, FScc, FSGLDIV, FSGLMUL, FSIN, FSINCOS, FSINH, FSQRT, FSUB, FTAN, FTANH, FTENTOX, FTRAPcc, FTST, FTWOTOX

Note that many of these are MC68881/MC68882 transcendentals that the MC68040 implements in software rather than hardware — each entry states which parts support it.

### 09 — Section 6: Supervisor (Privileged) Instructions
`09-section-06-supervisor-instructions.pdf` · 86 pages

Detailed descriptions of the privileged instructions, alphabetical by mnemonic — status register access, cache maintenance, coprocessor and FPU state save/restore, MMU control (the MC68851 and on-chip PMMU instructions), and processor control. **29 entries:**

> ANDI to SR, CINV, cpRESTORE, cpSAVE, CPUSH, EORI to SR, FRESTORE, FSAVE, MOVE from SR, MOVE to SR, MOVE, MOVEC, MOVES, ORI to SR, PBcc, PDBcc, PFLUSH, PFLUSHR, PLOAD, PMOVE, PRESTORE, PSAVE, PScc, PTEST, PTRAPcc, PVALID, RESET, RTE, STOP

### 10 — Section 7: CPU32 Instructions
`10-section-07-cpu32-instructions.pdf` · 16 pages

The instructions specific to the CPU32 core (used in the MC683xx embedded controllers), which otherwise executes MC68000/MC68010 object code and many MC68020 instructions. **4 entries:**

> BGND (enter background mode), LPSTOP (low-power stop), TBLS (table lookup and interpolate, signed), TBLU (table lookup and interpolate, unsigned)

TBLS and TBLU each also cover their rounded/non-rounded variants (TBLSN, TBLUN).

### 11 — Section 8: Instruction Format Summary
`11-section-08-instruction-format-summary.pdf` · 40 pages

Every M68000 family instruction in binary format, listed in opcode order. Describes the instruction format fields — coprocessor ID, effective address, register/memory, source specifier, destination register, conditional predicate, shift and rotate, size, opmode, and address/data — and then gives the full operation code map. This is the section to use for decoding or emitting machine code.

**Subsections:** 8.1 Instruction Format (field definitions) · 8.2 Operation Code Map

### 12 — Appendix A: Processor Instruction Summary
`12-appendix-a-processor-instruction-summary.pdf` · 31 pages

Quick reference organized by processor rather than by mnemonic: which instructions and which addressing modes each part supports. Covers MC68000/MC68008/MC68010, MC68020, MC68030, MC68040, the MC68881/MC68882 coprocessors, and the MC68851 PMMU. References to the MC68000, MC68020, and MC68030 include the corresponding embedded controllers (MC68EC000, MC68EC020, MC68EC030). This is the fastest way to answer "does part *X* have instruction *Y*".

**Subsections:** A.1 MC68000, MC68008, MC68010 · A.2 MC68020 · A.3 MC68030 · A.4 MC68040 · A.5 MC68881/MC68882 · A.6 MC68851

### 13 — Appendix B: Exception Processing Reference
`13-appendix-b-exception-processing-reference.pdf` · 13 pages

Quick reference for system programmers already familiar with the stack frames (the per-part user's manuals carry the full treatment). Gives the exception vector assignments for the M68000 family, the layouts of every exception stack frame format, and the floating-point stack frames.

**Subsections:** B.1 Exception Vector Assignments for the M68000 Family · B.2 Exception Stack Frames · B.3 Floating-Point Stack Frames

### 14 — Appendix C: S-Record Output Format
`14-appendix-c-s-record-output-format.pdf` · 6 pages

The Motorola S-record format for encoding programs or data in a printable form for transfer between systems: record content and field layout, the S-record types (S0–S9), how S-records are created from an assembly, a worked example, and an ASCII code table.

**Subsections:** C.1 S-Record Content · C.2 S-Record Types · C.3 S-Record Creation

---

## How this was produced

Split with `pdftk` on the boundaries given by the PDF's own level-2 bookmarks, each boundary verified against the actual page text with `pdftotext`. Every part opens cleanly and the per-part page counts sum to exactly the 646 pages of the source.

Two things differ from a plain `pdftk cat`:

- **Bookmarks are preserved per file.** Each section's own sub-bookmarks are remapped to the new page numbering, with level gaps closed so pdftk does not insert blank placeholder entries.
- **Per-instruction bookmarks were generated for Sections 4–7.** The source PDF has *no* sub-bookmarks at all for these four sections — 452 pages of alphabetical instruction reference with no navigation. They were reconstructed by scanning each page's running header for the instruction mnemonic and its description, giving 175 bookmarks (`ABCD - Add Decimal with Extend`, `LINK - Link and Allocate`, …). Qualified forms such as `MOVE from CCR` and `ANDI to SR` are kept distinct from their base mnemonics.

Two caveats about that generated index, since it is derived rather than authored:

- 13 of the 175 entries show the mnemonic alone, with no description — the header text on those pages did not extract in a usable order (ADD, BKPT, CMPI, MOVE, SUBA, FDBcc, FETOX, FMOVEM, FScc, FTENTOX, FTWOTOX, FRESTORE, MOVE from SR). The page targets for these are still correct.
- The descriptions come from a scanned text layer, so occasional OCR imperfections are possible in the bookmark labels. The mnemonics themselves were checked against the section contents.

**Encryption note:** the source PDF carries an owner password (RC4, permissions set to disallow modification). No password was supplied or needed to read it — pdftk warns and proceeds, since the user password is empty — but the resulting split files are **not** encrypted and carry no permission flags. If those restrictions matter to you, re-apply them with `pdftk … output … owner_pw <pw> allow printing`.

```
pdftk M68000PRM.pdf cat <first>-<last> output <part>.pdf
pdftk <part>.pdf update_info <part>.info output <part>-with-bookmarks.pdf
```
