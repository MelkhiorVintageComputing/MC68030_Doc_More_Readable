# M68000 Family — Instruction Support by Processor

Derived from `../M68000PRM.pdf` — Motorola *M68000 Family Programmer's Reference Manual*, 1992
(see [`README.md`](README.md) for the split of that manual into per-section PDFs).

This document lists, for every processor and coprocessor in the family, which instructions it
supports. Per your request, **CPU32 is excluded** — only the 68xxx processors and the two
coprocessors are covered. (The manual's own Table A-1 has a CPU32 column; the four CPU32-only
instructions BGND, LPSTOP, TBLS and TBLU are therefore omitted here.)

## Sources and how this was checked

The support data is taken from **Table A-1, "M68000 Family Instruction Set and Processor
Cross-Reference"** (PDF pp. 597–603 of the source; Appendix A, printed pp. A-1…A-7). Because a
single OCR-adjacent table is easy to mis-read, every entry was cross-checked against two
independent statements of the same fact elsewhere in the manual:

| # | Source | Where |
|---|--------|-------|
| 1 | Table A-1 cross-reference matrix | PDF pp. 597–603 |
| 2 | The per-processor instruction lists — Tables A-3 (MC68000/08), A-4 (MC68010), A-6 (MC68020), A-8 (MC68030), A-10 (MC68040), A-12 (MC68881/2), A-13 (MC68851) | PDF pp. 608–627 |
| 3 | The processor annotation printed in the header of each instruction description, e.g. `(M68000 Family)`, `(MC68020, MC68030, MC68040)`, `(MC6888X, M68040FPSP)` | Sections 4, 5 and 6 — PDF pp. 105–540 |

The corroboration is broad: the seven per-processor tables between them confirm 729 of Table A-1's
marks, and the instruction descriptions confirm 629 processor claims. Seven instructions are where
the three sources genuinely disagree — `BKPT`, `cpTRAPcc`, `DIVSL`, `DIVUL`, `EXTB`, `FLOGNP1` and
`PFLUSHA`. Those, with three misprints found along the way, are the ten entries under
[Documentation discrepancies](#documentation-discrepancies) below, and the only places where this
document departs from, or annotates, Table A-1.

[`check-instructions-by-cpu.py`](check-instructions-by-cpu.py) runs the comparison:

```
   misspelling   A-6        cpTRACPcc  Table A-6 transposes the P and the C of cpTRAPcc
per-processor tables: 729 instructions corroborated across 7 tables, 0 listed but unmarked, 0 marked but unlisted
   known defect  BKPT       MC68000    the Section 4 description is headed (MC68EC000, ...), but Table A-1 leaves the 68000 column blank and Table A-3 does not list BKPT; the tables are followed here
   known defect  DIVSL      MC68000    DIVS and DIVSL share a description headed (M68000 Family); the long form is MC68020 and later
   known defect  DIVSL      MC68008    as DIVSL/MC68000
   known defect  DIVSL      MC68010    as DIVSL/MC68000
   known defect  DIVUL      MC68000    DIVU and DIVUL share a description headed (M68000 Family); the long form is MC68020 and later
   known defect  DIVUL      MC68008    as DIVUL/MC68000
   known defect  DIVUL      MC68010    as DIVUL/MC68000
   known defect  EXTB       MC68000    EXT and EXTB share a description headed (M68000 Family); EXTB is MC68020 and later, which the description says only in its Assembler Syntax line
   known defect  EXTB       MC68008    as EXTB/MC68000
   known defect  EXTB       MC68010    as EXTB/MC68000
description headers: 165 descriptions read, 629 processor claims corroborated, 0 unexplained
csv integrity: 196 instructions, 0 duplicate mnemonics, 0 with no support
```

## Reading the tables

| Symbol | Meaning |
|---|---|
| `X` | Supported |
| `S` | Supported on the MC68040 **in software only**, via the M68040FPSP floating-point support package (Table A-1 footnote 3) |
| `X`⚠ | Supported, but **Table A-1 omits the mark** — added here on the evidence of the other two sources (see discrepancies 1 and 2) |
| *(blank)* | Not supported |

Footnote conditions from Table A-1 are carried into the Notes column: *privileged*, *not on
EC/LC040* (MC68EC040 and MC68LC040), *not on EC030* (MC68EC030), and *not privileged on
68000/68008*.

Throughout, `MC68881/2` means the MC68881 and MC68882 floating-point coprocessors (the manual
writes this `MC6888X`), and per Appendix A's own preamble, references to the MC68000, MC68020 and
MC68030 include the embedded MC68EC000, MC68EC020 and MC68EC030 unless a footnote says otherwise.

## Instruction counts

| Processor | Instructions | Of which software-only |
|---|--:|--:|
| MC68000 | 84 | — |
| MC68008 | 84 | — |
| MC68010 | 89 | — |
| MC68020 | 116 | — |
| MC68030 | 119 | — |
| MC68040 | 176 | 29 |
| MC68881/2 | 47 | — |
| MC68851 | 14 | — |

The MC68040's total is much larger than the MC68030's chiefly because it absorbs the
floating-point instruction set: of its 176 instructions, 63 are the FPU set, and 29 of those are
provided by the software FPSP rather than in hardware.

## Instructions by processor

### MC68000 — 84 instructions

> `ABCD`, `ADD`, `ADDA`, `ADDI`, `ADDQ`, `ADDX`, `AND`, `ANDI`, `ANDI to CCR`, `ANDI to SR`, `ASL`, `ASR`, `Bcc`, `BCHG`, `BCLR`, `BRA`, `BSET`, `BSR`, `BTST`, `CHK`, `CLR`, `CMP`, `CMPA`, `CMPI`, `CMPM`, `DBcc`, `DIVS`, `DIVU`, `EOR`, `EORI`, `EORI to CCR`, `EORI to SR`, `EXG`, `EXT`, `ILLEGAL`, `JMP`, `JSR`, `LEA`, `LINK`, `LSL`, `LSR`, `MOVE`, `MOVEA`, `MOVE to CCR`, `MOVE from SR`, `MOVE to SR`, `MOVE USP`, `MOVEM`, `MOVEP`, `MOVEQ`, `MULS`, `MULU`, `NBCD`, `NEG`, `NEGX`, `NOP`, `NOT`, `OR`, `ORI`, `ORI to CCR`, `ORI to SR`, `PEA`, `RESET`, `ROL`, `ROR`, `ROXL`, `ROXR`, `RTE`, `RTR`, `RTS`, `SBCD`, `Scc`, `STOP`, `SUB`, `SUBA`, `SUBI`, `SUBQ`, `SUBX`, `SWAP`, `TAS`, `TRAP`, `TRAPV`, `TST`, `UNLK`

### MC68008 — 84 instructions

> `ABCD`, `ADD`, `ADDA`, `ADDI`, `ADDQ`, `ADDX`, `AND`, `ANDI`, `ANDI to CCR`, `ANDI to SR`, `ASL`, `ASR`, `Bcc`, `BCHG`, `BCLR`, `BRA`, `BSET`, `BSR`, `BTST`, `CHK`, `CLR`, `CMP`, `CMPA`, `CMPI`, `CMPM`, `DBcc`, `DIVS`, `DIVU`, `EOR`, `EORI`, `EORI to CCR`, `EORI to SR`, `EXG`, `EXT`, `ILLEGAL`, `JMP`, `JSR`, `LEA`, `LINK`, `LSL`, `LSR`, `MOVE`, `MOVEA`, `MOVE to CCR`, `MOVE from SR`, `MOVE to SR`, `MOVE USP`, `MOVEM`, `MOVEP`, `MOVEQ`, `MULS`, `MULU`, `NBCD`, `NEG`, `NEGX`, `NOP`, `NOT`, `OR`, `ORI`, `ORI to CCR`, `ORI to SR`, `PEA`, `RESET`, `ROL`, `ROR`, `ROXL`, `ROXR`, `RTE`, `RTR`, `RTS`, `SBCD`, `Scc`, `STOP`, `SUB`, `SUBA`, `SUBI`, `SUBQ`, `SUBX`, `SWAP`, `TAS`, `TRAP`, `TRAPV`, `TST`, `UNLK`

### MC68010 — 89 instructions

> `ABCD`, `ADD`, `ADDA`, `ADDI`, `ADDQ`, `ADDX`, `AND`, `ANDI`, `ANDI to CCR`, `ANDI to SR`, `ASL`, `ASR`, `Bcc`, `BCHG`, `BCLR`, `BKPT`, `BRA`, `BSET`, `BSR`, `BTST`, `CHK`, `CLR`, `CMP`, `CMPA`, `CMPI`, `CMPM`, `DBcc`, `DIVS`, `DIVU`, `EOR`, `EORI`, `EORI to CCR`, `EORI to SR`, `EXG`, `EXT`, `ILLEGAL`, `JMP`, `JSR`, `LEA`, `LINK`, `LSL`, `LSR`, `MOVE`, `MOVEA`, `MOVE from CCR`, `MOVE to CCR`, `MOVE from SR`, `MOVE to SR`, `MOVE USP`, `MOVEC`, `MOVEM`, `MOVEP`, `MOVEQ`, `MOVES`, `MULS`, `MULU`, `NBCD`, `NEG`, `NEGX`, `NOP`, `NOT`, `OR`, `ORI`, `ORI to CCR`, `ORI to SR`, `PEA`, `RESET`, `ROL`, `ROR`, `ROXL`, `ROXR`, `RTD`, `RTE`, `RTR`, `RTS`, `SBCD`, `Scc`, `STOP`, `SUB`, `SUBA`, `SUBI`, `SUBQ`, `SUBX`, `SWAP`, `TAS`, `TRAP`, `TRAPV`, `TST`, `UNLK`

### MC68020 — 116 instructions

> `ABCD`, `ADD`, `ADDA`, `ADDI`, `ADDQ`, `ADDX`, `AND`, `ANDI`, `ANDI to CCR`, `ANDI to SR`, `ASL`, `ASR`, `Bcc`, `BCHG`, `BCLR`, `BFCHG`, `BFCLR`, `BFEXTS`, `BFEXTU`, `BFFFO`, `BFINS`, `BFSET`, `BFTST`, `BKPT`, `BRA`, `BSET`, `BSR`, `BTST`, `CALLM`, `CAS`, `CAS2`, `CHK`, `CHK2`, `CLR`, `CMP`, `CMPA`, `CMPI`, `CMPM`, `CMP2`, `cpBcc`, `cpDBcc`, `cpGEN`, `cpRESTORE`, `cpSAVE`, `cpScc`, `cpTRAPcc`, `DBcc`, `DIVS`, `DIVSL`, `DIVU`, `DIVUL`, `EOR`, `EORI`, `EORI to CCR`, `EORI to SR`, `EXG`, `EXT`, `EXTB`, `ILLEGAL`, `JMP`, `JSR`, `LEA`, `LINK`, `LSL`, `LSR`, `MOVE`, `MOVEA`, `MOVE from CCR`, `MOVE to CCR`, `MOVE from SR`, `MOVE to SR`, `MOVE USP`, `MOVEC`, `MOVEM`, `MOVEP`, `MOVEQ`, `MOVES`, `MULS`, `MULU`, `NBCD`, `NEG`, `NEGX`, `NOP`, `NOT`, `OR`, `ORI`, `ORI to CCR`, `ORI to SR`, `PACK`, `PEA`, `RESET`, `ROL`, `ROR`, `ROXL`, `ROXR`, `RTD`, `RTE`, `RTM`, `RTR`, `RTS`, `SBCD`, `Scc`, `STOP`, `SUB`, `SUBA`, `SUBI`, `SUBQ`, `SUBX`, `SWAP`, `TAS`, `TRAP`, `TRAPcc`, `TRAPV`, `TST`, `UNLK`, `UNPK`

### MC68030 — 119 instructions

> `ABCD`, `ADD`, `ADDA`, `ADDI`, `ADDQ`, `ADDX`, `AND`, `ANDI`, `ANDI to CCR`, `ANDI to SR`, `ASL`, `ASR`, `Bcc`, `BCHG`, `BCLR`, `BFCHG`, `BFCLR`, `BFEXTS`, `BFEXTU`, `BFFFO`, `BFINS`, `BFSET`, `BFTST`, `BKPT`, `BRA`, `BSET`, `BSR`, `BTST`, `CAS`, `CAS2`, `CHK`, `CHK2`, `CLR`, `CMP`, `CMPA`, `CMPI`, `CMPM`, `CMP2`, `cpBcc`, `cpDBcc`, `cpGEN`, `cpRESTORE`, `cpSAVE`, `cpScc`, `cpTRAPcc`, `DBcc`, `DIVS`, `DIVSL`, `DIVU`, `DIVUL`, `EOR`, `EORI`, `EORI to CCR`, `EORI to SR`, `EXG`, `EXT`, `EXTB`, `ILLEGAL`, `JMP`, `JSR`, `LEA`, `LINK`, `LSL`, `LSR`, `MOVE`, `MOVEA`, `MOVE from CCR`, `MOVE to CCR`, `MOVE from SR`, `MOVE to SR`, `MOVE USP`, `MOVEC`, `MOVEM`, `MOVEP`, `MOVEQ`, `MOVES`, `MULS`, `MULU`, `NBCD`, `NEG`, `NEGX`, `NOP`, `NOT`, `OR`, `ORI`, `ORI to CCR`, `ORI to SR`, `PACK`, `PEA`, `PFLUSH`, `PFLUSHA`, `PLOAD`, `PMOVE`, `PTEST`, `RESET`, `ROL`, `ROR`, `ROXL`, `ROXR`, `RTD`, `RTE`, `RTR`, `RTS`, `SBCD`, `Scc`, `STOP`, `SUB`, `SUBA`, `SUBI`, `SUBQ`, `SUBX`, `SWAP`, `TAS`, `TRAP`, `TRAPcc`, `TRAPV`, `TST`, `UNLK`, `UNPK`

### MC68040 — 176 instructions

Hardware (147):

> `ABCD`, `ADD`, `ADDA`, `ADDI`, `ADDQ`, `ADDX`, `AND`, `ANDI`, `ANDI to CCR`, `ANDI to SR`, `ASL`, `ASR`, `Bcc`, `BCHG`, `BCLR`, `BFCHG`, `BFCLR`, `BFEXTS`, `BFEXTU`, `BFFFO`, `BFINS`, `BFSET`, `BFTST`, `BKPT`, `BRA`, `BSET`, `BSR`, `BTST`, `CAS`, `CAS2`, `CHK`, `CHK2`, `CINV`, `CLR`, `CMP`, `CMPA`, `CMPI`, `CMPM`, `CMP2`, `CPUSH`, `DBcc`, `DIVS`, `DIVSL`, `DIVU`, `DIVUL`, `EOR`, `EORI`, `EORI to CCR`, `EORI to SR`, `EXG`, `EXT`, `EXTB`, `FABS`, `FSABS`, `FDABS`, `FADD`, `FSADD`, `FDADD`, `FBcc`, `FCMP`, `FDBcc`, `FDIV`, `FSDIV`, `FDDIV`, `FMOVE`, `FSMOVE`, `FDMOVE`, `FMOVEM`, `FMUL`, `FSMUL`, `FDMUL`, `FNEG`, `FSNEG`, `FDNEG`, `FNOP`, `FRESTORE`, `FSAVE`, `FScc`, `FSQRT`, `FSSQRT`, `FDSQRT`, `FSUB`, `FSSUB`, `FDSUB`, `FTRAPcc`, `FTST`, `ILLEGAL`, `JMP`, `JSR`, `LEA`, `LINK`, `LSL`, `LSR`, `MOVE`, `MOVEA`, `MOVE from CCR`, `MOVE to CCR`, `MOVE from SR`, `MOVE to SR`, `MOVE USP`, `MOVE16`, `MOVEC`, `MOVEM`, `MOVEP`, `MOVEQ`, `MOVES`, `MULS`, `MULU`, `NBCD`, `NEG`, `NEGX`, `NOP`, `NOT`, `OR`, `ORI`, `ORI to CCR`, `ORI to SR`, `PACK`, `PEA`, `PFLUSH`, `PFLUSHA`, `PTEST`, `RESET`, `ROL`, `ROR`, `ROXL`, `ROXR`, `RTD`, `RTE`, `RTR`, `RTS`, `SBCD`, `Scc`, `STOP`, `SUB`, `SUBA`, `SUBI`, `SUBQ`, `SUBX`, `SWAP`, `TAS`, `TRAP`, `TRAPcc`, `TRAPV`, `TST`, `UNLK`, `UNPK`

Software, via M68040FPSP (29):

> `FACOS`, `FASIN`, `FATAN`, `FATANH`, `FCOS`, `FCOSH`, `FETOX`, `FETOXM1`, `FGETEXP`, `FGETMAN`, `FINT`, `FINTRZ`, `FLOG10`, `FLOG2`, `FLOGN`, `FLOGNP1`, `FMOD`, `FMOVECR`, `FREM`, `FSCALE`, `FSGLDIV`, `FSGLMUL`, `FSIN`, `FSINCOS`, `FSINH`, `FTAN`, `FTANH`, `FTENTOX`, `FTWOTOX`

### MC68881/2 — 47 instructions

> `FABS`, `FACOS`, `FADD`, `FASIN`, `FATAN`, `FATANH`, `FBcc`, `FCMP`, `FCOS`, `FCOSH`, `FDBcc`, `FDIV`, `FETOX`, `FETOXM1`, `FGETEXP`, `FGETMAN`, `FINT`, `FINTRZ`, `FLOG10`, `FLOG2`, `FLOGN`, `FLOGNP1`, `FMOD`, `FMOVE`, `FMOVECR`, `FMOVEM`, `FMUL`, `FNEG`, `FNOP`, `FREM`, `FRESTORE`, `FSAVE`, `FSCALE`, `FScc`, `FSGLDIV`, `FSGLMUL`, `FSIN`, `FSINCOS`, `FSINH`, `FSQRT`, `FSUB`, `FTAN`, `FTANH`, `FTENTOX`, `FTRAPcc`, `FTST`, `FTWOTOX`

### MC68851 — 14 instructions

> `PBcc`, `PDBcc`, `PFLUSH`, `PFLUSHA`, `PFLUSHR`, `PFLUSHS`, `PLOAD`, `PMOVE`, `PRESTORE`, `PSAVE`, `PScc`, `PTEST`, `PTRAPcc`, `PVALID`

## Documentation discrepancies

Ten places where the manual contradicts itself or is imprecise. Each was verified by reading the
relevant page directly; page numbers are **PDF pages of `M68000PRM.pdf`**, with the split file in
brackets.

### 1. Table A-1 omits MC68881/MC68882 support for `FLOGNP1` — *substantive*

Table A-1 (p. 600) gives the `FLOGNP1` row a `2,3` mark in the MC68040 column and **leaves the
68881/68882 column blank**. Every adjacent transcendental row (`FMOD`, `FMOVECR`, `FREM`, `FSCALE`,
`FSGLDIV`, …) has an `X` there. Both other sources say the coprocessors do support it:

- Table A-12, MC68881/MC68882 Instruction Set (p. 626), lists `FLOGNP1`.
- The Section 5 description of `FLOGNP1` (p. 369) is headed `(MC6888X, M68040FPSP)`.

Read as a dropped mark in Table A-1. Marked `X`⚠ for MC68881/2 in this document.

### 2. Table A-1 omits MC68040 support for `PFLUSHA` — *substantive*

Table A-1 (p. 602) marks `PFLUSHA` for the MC68030 (`X`, footnote 5) and the MC68851 only. But
Table A-10, MC68040 Instruction Set (p. 624), lists `PFLUSHA`; and the neighbouring `PFLUSH` row in
Table A-1 *does* carry an MC68040 mark. Marked `X`⚠ for MC68040 here.

### 3. `cpTRAPcc` is misspelled `cpTRACPcc` in Table A-6 — *typo*

Table A-6, MC68020 Instruction Set Summary (p. 614), reads `cpTRACPcc` — the `P` and `C` are
transposed. The instruction is spelled `cpTRAPcc` in Table A-1 (p. 598), in Table A-2 (p. 605), in
Table A-8 for the MC68030 (p. 618), and in its own description (p. 193).

### 4. `BKPT` — Section 4 claims MC68EC000, the tables do not

The Section 4 description of `BKPT` (p. 157) is headed
`(MC68EC000, MC68010, MC68020, MC68030, MC68040, CPU32)`. But Table A-1 leaves the 68000 column
blank for `BKPT`, and Table A-3, the MC68000/MC68008 instruction set (pp. 608–609), does not list
it — `BKPT` first appears in Table A-4, for the MC68010 (p. 610).

Appendix A states that references to the MC68000 include the MC68EC000, so the two cannot both be
right. This document follows the tables (no MC68000/MC68008 support), but the conflict is
unresolved in the manual and the MC68EC000 is a later part than the tables' vintage.

### 5. `DIVSL`, `DIVUL` and `EXTB` inherit an over-broad header — *imprecision*

`DIVS` and `DIVSL` share one description (pp. 196–199), as do `DIVU` and `DIVUL` (pp. 200–203) and
`EXT` and `EXTB` (p. 210). Every one of those pages is headed `(M68000 Family)`. But the long forms
`DIVSL`, `DIVUL` and `EXTB` are all MC68020-and-later, as Table A-1 and Tables A-3/A-4 state.

Only `EXT, EXTB` says so anywhere on the page, and it says it in the Assembler Syntax block rather
than in the header:

> `EXTB.L Dn` extend byte to long word (MC68020, MC68030 MC68040, CPU32)

`DIVS`/`DIVSL` and `DIVU`/`DIVUL` leave the restriction to the body prose. In all three cases the
header, read alone, claims MC68000 support the instruction does not have.

### 6. Malformed processor list on `EXTB` — *typo*

That Assembler Syntax annotation reads `(MC68020, MC68030 MC68040, CPU32)` — the comma between
`MC68030` and `MC68040` is missing. It is the only processor list in the manual that runs two part
numbers together.

### 7. Malformed header on `PTRAPcc` — *typo*

The Section 6 description of `PTRAPcc` (p. 532) is headed `(M68851)`. Every other PMMU instruction
uses the part number `(MC68851)`; `M68851` is not a Motorola part designation.

### 8. `FSABS`/`FDABS` appear as `FSFABS`/`FDFABS` in Table A-2 — *typo*

Table A-2 (p. 605) lists `FSFABS, FDFABS — Floating-Point Absolute Value (Single/Double
Precision)`. The instructions are `FSABS`/`FDABS`: that is the spelling in Table A-1 (p. 600), in
Table A-10 (MC68040), and in the Section 5 `FABS` description. The stray `F` is unique to
Table A-2.

### 9. `FSAVE` carries a footnote marker Table A-1 never defines — *typo*

Table A-1 (p. 603) prints the row as `FSAVE*`. The table's own NOTES list runs 1 to 5 and has no
asterisk in it, so the marker points at nothing.

It should be footnote 1, *Privileged (Supervisor) Instruction*. `FSAVE` is privileged — it is
documented in Section 6, Supervisor (Privileged) Instructions (p. 468) — and `FRESTORE`, its twin
on the line above, does carry footnote 1. The consequence is visible in the table below: `FSAVE`
is the one privileged instruction in the manual whose Notes cell does not say so, because the
marker it was given cannot be resolved.

### 10. Table A-2 gives `ADDA` the description `Address` — *typo*

Table A-2 (p. 604) lists `ADDA — Address`. It is *Add Address*, which is what Table A-3 (p. 608),
Table A-4, Table A-6, Table A-8 and Table A-10 all print, and what the Section 4 description
(p. 111) is titled. The verb has simply dropped out.

Descriptions in the table below come from Table A-2 verbatim, so this one reads `Address`.

### Not discrepancies

Three differences that look like conflicts but are correct as printed:

- **`MOVE from SR` is documented twice** — in Section 4 (p. 229, headed `(MC68000, MC68008)`) and
  again in Section 6 (p. 471, headed `(MC68EC000, MC68010, MC68020, MC68030, MC68040, CPU32)`).
  This is deliberate: the instruction is unprivileged on the MC68000/MC68008 and privileged from
  the MC68010 on, which is exactly what Table A-1's footnote 4 records, and why its 68000/68008
  cells carry a bare `4` rather than an `X`.
- **`PFLUSHA` and `PFLUSHS` have no description pages of their own** — they are documented inside
  the `PFLUSH` entry (p. 486), whose four headers between them cover the MC68030, MC68040/LC040,
  MC68EC040 and MC68851.
- **The single/double-precision forms** (`FSADD`/`FDADD`, `FSMUL`/`FDMUL`, …) likewise have no
  separate descriptions; each is covered by its parent entry in Section 5.

## Master cross-reference

One row per instruction; this is Table A-1 restated with the CPU32 column dropped, grouped
mnemonics split into their individual forms (so `ASL, ASR` becomes two rows), and the two
omissions noted above filled in and marked ⚠.

| Instruction | Description | MC68000 | MC68008 | MC68010 | MC68020 | MC68030 | MC68040 | MC68881/2 | MC68851 | Notes |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `ABCD` | Add Decimal with Extend | X | X | X | X | X | X |  |  |  |
| `ADD` | Add | X | X | X | X | X | X |  |  |  |
| `ADDA` | Address | X | X | X | X | X | X |  |  |  |
| `ADDI` | Add Immediate | X | X | X | X | X | X |  |  |  |
| `ADDQ` | Add Quick | X | X | X | X | X | X |  |  |  |
| `ADDX` | Add with Extend | X | X | X | X | X | X |  |  |  |
| `AND` | Logical AND | X | X | X | X | X | X |  |  |  |
| `ANDI` | Logical AND Immediate | X | X | X | X | X | X |  |  |  |
| `ANDI to CCR` | AND Immediate to Condition Code Register | X | X | X | X | X | X |  |  |  |
| `ANDI to SR` | AND Immediate to Status Register | X | X | X | X | X | X |  |  | privileged |
| `ASL` | Arithmetic Shift Left and Right | X | X | X | X | X | X |  |  |  |
| `ASR` | Arithmetic Shift Left and Right | X | X | X | X | X | X |  |  |  |
| `Bcc` | Branch Conditionally | X | X | X | X | X | X |  |  |  |
| `BCHG` | Test Bit and Change | X | X | X | X | X | X |  |  |  |
| `BCLR` | Test Bit and Clear | X | X | X | X | X | X |  |  |  |
| `BFCHG` | Test Bit Field and Change |  |  |  | X | X | X |  |  |  |
| `BFCLR` | Test Bit Field and Clear |  |  |  | X | X | X |  |  |  |
| `BFEXTS` | Signed Bit Field Extract |  |  |  | X | X | X |  |  |  |
| `BFEXTU` | Unsigned Bit Field Extract |  |  |  | X | X | X |  |  |  |
| `BFFFO` | Bit Field Find First One |  |  |  | X | X | X |  |  |  |
| `BFINS` | Bit Field Insert |  |  |  | X | X | X |  |  |  |
| `BFSET` | Test Bit Field and Set |  |  |  | X | X | X |  |  |  |
| `BFTST` | Test Bit Field |  |  |  | X | X | X |  |  |  |
| `BKPT` | Breakpoint |  |  | X | X | X | X |  |  |  |
| `BRA` | Branch | X | X | X | X | X | X |  |  |  |
| `BSET` | Test Bit and Set | X | X | X | X | X | X |  |  |  |
| `BSR` | Branch to Subroutine | X | X | X | X | X | X |  |  |  |
| `BTST` | Test Bit | X | X | X | X | X | X |  |  |  |
| `CALLM` | CALL Module |  |  |  | X |  |  |  |  |  |
| `CAS` | Compare and Swap Operands |  |  |  | X | X | X |  |  |  |
| `CAS2` | Compare and Swap Dual Operands |  |  |  | X | X | X |  |  |  |
| `CHK` | Check Register Against Bound | X | X | X | X | X | X |  |  |  |
| `CHK2` | Check Register Against Upper and Lower Bounds |  |  |  | X | X | X |  |  |  |
| `CINV` | Invalidate Cache Entries |  |  |  |  |  | X |  |  | privileged |
| `CLR` | Clear | X | X | X | X | X | X |  |  |  |
| `CMP` | Compare | X | X | X | X | X | X |  |  |  |
| `CMPA` | Compare Address | X | X | X | X | X | X |  |  |  |
| `CMPI` | Compare Immediate | X | X | X | X | X | X |  |  |  |
| `CMPM` | Compare Memory to Memory | X | X | X | X | X | X |  |  |  |
| `CMP2` | Compare Register Against Upper and Lower Bounds |  |  |  | X | X | X |  |  |  |
| `cpBcc` | Branch on Coprocessor Condition |  |  |  | X | X |  |  |  |  |
| `cpDBcc` | Test Coprocessor Condition Decrement and Branch |  |  |  | X | X |  |  |  |  |
| `cpGEN` | Coprocessor General Function |  |  |  | X | X |  |  |  |  |
| `cpRESTORE` | Coprocessor Restore Function |  |  |  | X | X |  |  |  | privileged |
| `cpSAVE` | Coprocessor Save Function |  |  |  | X | X |  |  |  | privileged |
| `cpScc` | Set on Coprocessor Condition |  |  |  | X | X |  |  |  |  |
| `cpTRAPcc` | Trap on Coprocessor Condition |  |  |  | X | X |  |  |  |  |
| `CPUSH` | Push then Invalidate Cache Entries |  |  |  |  |  | X |  |  | privileged |
| `DBcc` | Test Condition, Decrement and Branch | X | X | X | X | X | X |  |  |  |
| `DIVS` | Signed Divide | X | X | X | X | X | X |  |  |  |
| `DIVSL` | Signed Divide |  |  |  | X | X | X |  |  |  |
| `DIVU` | Unsigned Divide | X | X | X | X | X | X |  |  |  |
| `DIVUL` | Unsigned Divide |  |  |  | X | X | X |  |  |  |
| `EOR` | Logical Exclusive-OR | X | X | X | X | X | X |  |  |  |
| `EORI` | Logical Exclusive-OR Immediate | X | X | X | X | X | X |  |  |  |
| `EORI to CCR` | Exclusive-OR Immediate to Condition Code Register | X | X | X | X | X | X |  |  |  |
| `EORI to SR` | Exclusive-OR Immediate to Status Register | X | X | X | X | X | X |  |  | privileged |
| `EXG` | Exchange Registers | X | X | X | X | X | X |  |  |  |
| `EXT` | Sign Extend | X | X | X | X | X | X |  |  |  |
| `EXTB` | Sign Extend |  |  |  | X | X | X |  |  |  |
| `FABS` | Floating-Point Absolute Value |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSABS` | Floating-Point Absolute Value (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDABS` | Floating-Point Absolute Value (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FACOS` | Floating-Point Arc Cosine |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FADD` | Floating-Point Add |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSADD` | Floating-Point Add (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDADD` | Floating-Point Add (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FASIN` | Floating-Point Arc Sine |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FATAN` | Floating-Point Arc Tangent |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FATANH` | Floating-Point Hyperbolic Arc Tangent |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FBcc` | Floating-Point Branch |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FCMP` | Floating-Point Compare |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FCOS` | Floating-Point Cosine |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FCOSH` | Floating-Point Hyperbolic Cosine |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FDBcc` | Floating-Point Decrement and Branch |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FDIV` | Floating-Point Divide |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSDIV` | Floating-Point Divide (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDDIV` | Floating-Point Divide (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FETOX` | Floating-Point ex |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FETOXM1` | Floating-Point ex - 1 |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FGETEXP` | Floating-Point Get Exponent |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FGETMAN` | Floating-Point Get Mantissa |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FINT` | Floating-Point Integer Part |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FINTRZ` | Floating-Point Integer Part, Round-to-Zero |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FLOG10` | Floating-Point Log10 |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FLOG2` | Floating-Point Log2 |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FLOGN` | Floating-Point Loge |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FLOGNP1` | Floating-Point Loge (x + 1) |  |  |  |  |  | S | **X**⚠ |  | not on EC/LC040; 68040: software (FPSP) |
| `FMOD` | Floating-Point Modulo Remainder |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FMOVE` | Move Floating-Point Register |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSMOVE` | Move Floating-Point Register (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDMOVE` | Move Floating-Point Register (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FMOVECR` | Move Constant ROM |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FMOVEM` | Move Multiple Floating-Point Registers |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FMUL` | Floating-Point Multiply |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSMUL` | Floating-Point Multiply (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDMUL` | Floating-Point Multiply (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FNEG` | Floating-Point Negate |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSNEG` | Floating-Point Negate (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDNEG` | Floating-Point Negate (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FNOP` | Floating-Point No Operation |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FREM` | IEEE Remainder |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FRESTORE` | Restore Floating-Point Internal State |  |  |  |  |  | X | X |  | privileged; not on EC/LC040 |
| `FSAVE` | Save Floating-Point Internal State |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSCALE` | Floating-Point Scale Exponent |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FScc` | Floating-Point Set According to Condition |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSGLDIV` | Single-Precision Divide |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FSGLMUL` | Single-Precision Multiply |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FSIN` | Sine |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FSINCOS` | Simultaneous Sine and Cosine |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FSINH` | Hyperbolic Sine |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FSQRT` | Floating-Point Square Root |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSSQRT` | Floating-Point Square Root (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDSQRT` | Floating-Point Square Root (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FSUB` | Floating-Point Subtract |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FSSUB` | Floating-Point Subtract (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FDSUB` | Floating-Point Subtract (Single/Double Precision) |  |  |  |  |  | X |  |  | not on EC/LC040 |
| `FTAN` | Tangent |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FTANH` | Hyperbolic Tangent |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FTENTOX` | Floating-Point 10x |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `FTRAPcc` | Floating-Point Trap On Condition |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FTST` | Floating-Point Test |  |  |  |  |  | X | X |  | not on EC/LC040 |
| `FTWOTOX` | Floating-Point 2x |  |  |  |  |  | S | X |  | not on EC/LC040; 68040: software (FPSP) |
| `ILLEGAL` | Take Illegal Instruction Trap | X | X | X | X | X | X |  |  |  |
| `JMP` | Jump | X | X | X | X | X | X |  |  |  |
| `JSR` | Jump to Subroutine | X | X | X | X | X | X |  |  |  |
| `LEA` | Load Effective Address | X | X | X | X | X | X |  |  |  |
| `LINK` | Link and Allocate | X | X | X | X | X | X |  |  |  |
| `LSL` | Logical Shift Left and Right | X | X | X | X | X | X |  |  |  |
| `LSR` | Logical Shift Left and Right | X | X | X | X | X | X |  |  |  |
| `MOVE` | Move | X | X | X | X | X | X |  |  |  |
| `MOVEA` | Move Address | X | X | X | X | X | X |  |  |  |
| `MOVE from CCR` | Move from Condition Code Register |  |  | X | X | X | X |  |  |  |
| `MOVE to CCR` | Move to Condition Code Register | X | X | X | X | X | X |  |  |  |
| `MOVE from SR` | Move from Status Register | X | X | X | X | X | X |  |  | privileged; not privileged on 68000/68008 |
| `MOVE to SR` | Move to Status Register | X | X | X | X | X | X |  |  | privileged |
| `MOVE USP` | Move User Stack Pointer | X | X | X | X | X | X |  |  | privileged |
| `MOVE16` | 16-Byte Block Move |  |  |  |  |  | X |  |  |  |
| `MOVEC` | Move Control Register |  |  | X | X | X | X |  |  | privileged |
| `MOVEM` | Move Multiple Registers | X | X | X | X | X | X |  |  |  |
| `MOVEP` | Move Peripheral | X | X | X | X | X | X |  |  |  |
| `MOVEQ` | Move Quick | X | X | X | X | X | X |  |  |  |
| `MOVES` | Move Alternate Address Space |  |  | X | X | X | X |  |  | privileged |
| `MULS` | Signed Multiply | X | X | X | X | X | X |  |  |  |
| `MULU` | Unsigned Multiply | X | X | X | X | X | X |  |  |  |
| `NBCD` | Negate Decimal with Extend | X | X | X | X | X | X |  |  |  |
| `NEG` | Negate | X | X | X | X | X | X |  |  |  |
| `NEGX` | Negate with Extend | X | X | X | X | X | X |  |  |  |
| `NOP` | No Operation | X | X | X | X | X | X |  |  |  |
| `NOT` | Logical Complement | X | X | X | X | X | X |  |  |  |
| `OR` | Logical Inclusive-OR | X | X | X | X | X | X |  |  |  |
| `ORI` | Logical Inclusive-OR Immediate | X | X | X | X | X | X |  |  |  |
| `ORI to CCR` | Inclusive-OR Immediate to Condition Code Register | X | X | X | X | X | X |  |  |  |
| `ORI to SR` | Inclusive-OR Immediate to Status Register | X | X | X | X | X | X |  |  | privileged |
| `PACK` | Pack BCD |  |  |  | X | X | X |  |  |  |
| `PBcc` | Branch on PMMU Condition |  |  |  |  |  |  |  | X | privileged |
| `PDBcc` | Test, Decrement, and Branch on PMMU Condition |  |  |  |  |  |  |  | X | privileged |
| `PEA` | Push Effective Address | X | X | X | X | X | X |  |  |  |
| `PFLUSH` | Flush Entry(ies) in the ATCs |  |  |  |  | X | X |  | X | privileged; not on EC030 |
| `PFLUSHA` | Flush Entry(ies) in the ATCs |  |  |  |  | X | **X**⚠ |  | X | privileged; not on EC030 |
| `PFLUSHR` | Flush Entry(ies) in the ATCs and RPT Entries |  |  |  |  |  |  |  | X | privileged |
| `PFLUSHS` | Flush Entry(ies) in the ATCs |  |  |  |  |  |  |  | X | privileged |
| `PLOAD` | Load an Entry into the ATC |  |  |  |  | X |  |  | X | privileged; not on EC030 |
| `PMOVE` | Move PMMU Register |  |  |  |  | X |  |  | X | privileged |
| `PRESTORE` | PMMU Restore Function |  |  |  |  |  |  |  | X | privileged |
| `PSAVE` | PMMU Save Function |  |  |  |  |  |  |  | X | privileged |
| `PScc` | Set on PMMU Condition |  |  |  |  |  |  |  | X | privileged |
| `PTEST` | Test a Logical Address |  |  |  |  | X | X |  | X | privileged |
| `PTRAPcc` | Trap on PMMU Condition |  |  |  |  |  |  |  | X | privileged |
| `PVALID` | Validate a Pointer |  |  |  |  |  |  |  | X |  |
| `RESET` | Reset External Devices | X | X | X | X | X | X |  |  | privileged |
| `ROL` | Rotate Left and Right | X | X | X | X | X | X |  |  |  |
| `ROR` | Rotate Left and Right | X | X | X | X | X | X |  |  |  |
| `ROXL` | Rotate with Extend Left and Right | X | X | X | X | X | X |  |  |  |
| `ROXR` | Rotate with Extend Left and Right | X | X | X | X | X | X |  |  |  |
| `RTD` | Return and Deallocate |  |  | X | X | X | X |  |  |  |
| `RTE` | Return from Exception | X | X | X | X | X | X |  |  | privileged |
| `RTM` | Return from Module |  |  |  | X |  |  |  |  |  |
| `RTR` | Return and Restore | X | X | X | X | X | X |  |  |  |
| `RTS` | Return from Subroutine | X | X | X | X | X | X |  |  |  |
| `SBCD` | Subtract Decimal with Extend | X | X | X | X | X | X |  |  |  |
| `Scc` | Set Conditionally | X | X | X | X | X | X |  |  |  |
| `STOP` | Stop | X | X | X | X | X | X |  |  | privileged |
| `SUB` | Subtract | X | X | X | X | X | X |  |  |  |
| `SUBA` | Subtract Address | X | X | X | X | X | X |  |  |  |
| `SUBI` | Subtract Immediate | X | X | X | X | X | X |  |  |  |
| `SUBQ` | Subtract Quick | X | X | X | X | X | X |  |  |  |
| `SUBX` | Subtract with Extend | X | X | X | X | X | X |  |  |  |
| `SWAP` | Swap Register Words | X | X | X | X | X | X |  |  |  |
| `TAS` | Test Operand and Set | X | X | X | X | X | X |  |  |  |
| `TRAP` | Trap | X | X | X | X | X | X |  |  |  |
| `TRAPcc` | Trap Conditionally |  |  |  | X | X | X |  |  |  |
| `TRAPV` | Trap on Overflow | X | X | X | X | X | X |  |  |  |
| `TST` | Test Operand | X | X | X | X | X | X |  |  |  |
| `UNLK` | Unlink | X | X | X | X | X | X |  |  |  |
| `UNPK` | Unpack BCD |  |  |  | X | X | X |  |  |  |

## Method and caveats

Everything above was extracted mechanically from the PDF's text layer and then reconciled; nothing
was transcribed by hand, and no support claim rests on a single table.

- **Table A-1 is not read from the text layer at all.** Its column widths shift from page to page,
  its footnote markers are superscripts that the extraction drops onto whichever line it likes, and
  a mnemonic too wide for its column is broken across two or three lines with the marks stranded on
  the line between — so `PLOAD`, `PRESTORE` and `PSAVE` have their marks emitted *above* the
  mnemonic, and `ROXL,` / marks / `ROXR` spreads one row over three lines. Instead
  `pdftotext -bbox` gives every word's bounding box; words are clustered into lines by their
  **bottom** edge, and columns assigned by centre against the header row of that same page.
- Clustering on the bottom edge rather than the top is the whole trick. A superscript's top is
  5.3 pt above its line's, which is further than the gap to the line above, so any rule keyed on
  the top strands it; its bottom is only 3.1 pt off. Once the markers land on their own rows, all
  four row layouts come out identically and no special case is needed for any of them.
- A word is a footnote marker rather than a mnemonic or a mark if its box is under 7 pt tall: body
  text in these tables is set at about 8.3 pt and superscripts at about 6 pt. That is what keeps
  the genuine trailing digits of `CMP2`, `CHK2`, `MOVE16`, `FLOG2`, `FLOG10`, `FETOXM1` and
  `FLOGNP1` intact while stripping the fused markers from `MOVES`, `STOP` and `FSAVE`.
- Grouped entries were expanded to their individual mnemonics, so `ASL, ASR` and `CAS, CAS2`
  contribute one row each to the matrix.
- A cell can be marked in three ways. Most carry an `X`. Where a footnote applies the `X` may be
  dropped and the marker left standing alone — `FMOVECR`'s MC68040 cell is a bare `2,3` and
  `MOVE from SR`'s MC68000 and MC68008 cells are a bare `4` — and those still mean supported. A
  cell whose footnotes include 3 is marked `S` here rather than `X`.

Two caveats worth stating:

- **The MC68040 count includes the FPSP.** 29 of its 176 instructions are marked `S`: they are
  provided by the M68040FPSP software package, not by hardware. If you want hardware-only
  capability, exclude them. The MC68EC040 and MC68LC040 lack the FPU entirely — the *not on
  EC/LC040* note in the Notes column marks the affected instructions.
- **Embedded variants are folded in.** Following Appendix A's own preamble, the MC68000 column
  covers the MC68EC000, MC68020 the MC68EC020, and MC68030 the MC68EC030, except where a footnote
  says otherwise (*not on EC030* appears on the MMU instructions, which the MC68EC030 lacks).

The 10 discrepancies above are those where the three sources genuinely disagree. During extraction a
further set of apparent conflicts turned out to be artefacts of the text layer rather than errors
in the manual — descriptions wrapping onto the preceding line in Table A-10, and the `cpTRAPcc`
description page (p. 193) whose header collapses onto a single line, `cpTRAPcc Trap on Coprocessor
Condition cpTRAPcc`, unlike every other instruction page. Those were resolved by reading the pages
concerned and are not reported as documentation defects.

## Regenerating

```sh
python3 make-instructions-by-cpu.py    # rewrites the CSV and this document
python3 check-instructions-by-cpu.py   # re-reads the PDFs and checks them
```
