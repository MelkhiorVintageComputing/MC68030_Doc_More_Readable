# M68000 Family — Condition Codes by Instruction

Derived from `../M68000PRM.pdf` — Motorola *M68000 Family Programmer's Reference Manual*, 1992
(see [`README.md`](README.md) for the split of that manual into per-section PDFs).

This document lists, for every MC680xx instruction, what it does to the five condition-code bits
X, N, Z, V and C. It is the per-instruction fact that the manual states only inside each
individual instruction description, 122 of them, and never gathers in one place.

**Coprocessor instructions are excluded.** That drops all 47 floating-point descriptions of
Section 5 — which have no `X N Z V C` table at all, but a `Floating-Point Status Register:` block
of a different shape — and 13 descriptions in Section 6 whose processor annotation names only the
MC68851 PMMU or the MC68881/MC68882 FPU. **CPU32-only instructions are excluded** as well
(`BGND`, `LPSTOP`, `TBLS`/`TBLSN`, `TBLU`/`TBLUN`), matching
[`INSTRUCTIONS-BY-CPU.md`](INSTRUCTIONS-BY-CPU.md).

Two kinds of description are deliberately kept. The `cpXXX` instructions (`cpBcc`, `cpDBcc`,
`cpGEN`, `cpRESTORE`, `cpSAVE`, `cpScc`, `cpTRAPcc`) are MC68020/MC68030 *CPU* instructions for
driving a coprocessor, not coprocessor instructions, and the manual prints them in Sections 4 and
6 accordingly. So are the MC68030 and MC68040 forms of `PFLUSH`, `PLOAD`, `PMOVE` and `PTEST`,
which drive those processors' own on-chip MMU.

**See also:** [`INSTRUCTIONS-BY-CPU.md`](INSTRUCTIONS-BY-CPU.md) — which processor supports which
instruction.

## Sources and how this was checked

| # | Source | Where |
|---|---|---|
| 1 | The `Condition Codes:` block of each instruction description | Sections 4 and 6 — PDF pp. 105–302, 455–540 (Section 7, pp. 541–556, is read and checked but excluded) |
| 2 | Table 3-18, *Integer Unit Condition Code Computations* | Section 3 — printed pp. 3-18…3-19 |
| 3 | Table 3-1, *Notational Conventions*, which defines the alphabet | Section 3 — printed p. 3-3 |
| 4 | A second extraction of the same pages with the layout preserver turned off, plus `pdftotext -bbox` for raised glyphs | same pages as 1 |

Source 2 is what makes this more than one reading of one table: it states the same facts for 30
grouped rows in a different notation, so agreement between it and the instruction pages is real
corroboration. Source 4 is the same glyphs read by a different code path in poppler — without
`-layout` the table serialises into runs of bit letters and runs of values instead of two aligned
rows, which is enough of a different problem that a mistake in one parse will not repeat in the
other.

[`check-condition-codes.py`](check-condition-codes.py) runs all of it:

```
Table 3-18: 30 rows, 60 mnemonics, 59 matched to a description, 1 unmatched
Table 3-18: 292 cells corroborate the instruction pages, 3 known defects, 0 unexplained
   known defect  CLR      N   3-18 '*'  page '0'   Table 3-18 groups CLR with thirteen instructions whose result is not constant and gives the group N = '*'; CLR's own page prints 0, which is right because the result of a clear is always zero
   known defect  CLR      Z   3-18 '*'  page '1'   the same grouping; CLR's own page prints 1
   known defect  ASR      V   3-18 '0'  page '*'   ASL and ASR share one description and one table, so ASR gets ASL's conditional V; Table 3-18 gives them separate rows and is right that an arithmetic right shift never changes the most significant bit
   unmatched     DUVU     Table 3-18 spells the DIVU row 'DIVS, DUVU'
Table 3-18: 7 shift-count rows corroborate the sentences rather than the glyphs
Table 3-18: covers 53 of the 120 descriptions carrying a Condition Codes block
second reading: 62 tables reconstructed from the unaligned extraction
second reading: 62 of 62 tables agree glyph for glyph, 0 disagree
glyph/sentence: 377 unconditional cells, 223 asterisk cells reading a condition, 0 wrong
glyph/sentence: 67 notes, each used with exactly one glyph, 0 ambiguous
raised glyphs: 326 explanation lines measured, 2 carry a sub-size digit, 1 distinct
csv integrity: 122 rows, 610 cells, 67 notes, 0 dangling, 0 unused, 0 duplicate keys
```

The two disagreements it reports — Table 3-18's `CLR` row and its `ASR` V — are the first two
entries under [Documentation discrepancies](#documentation-discrepancies) below. Everything else
corroborates.

## Reading the table

The alphabet is the manual's own. Table 3-1, *Notational Conventions*, defines it on printed page
3-3, under the heading *Register Codes*:

| Symbol | Table 3-1's definition | Here |
|---|---|---|
| `*` | General Case | replaced by a note number — see below |
| `U` | Undefined, Reserved for Motorola Use. | `U` |
| `—` | Not Affected or Applicable. | `—` |
| `0` | *(not defined in Table 3-1)* | `0`, always cleared |
| `1` | *(not defined in Table 3-1)* | `1`, always set |

The manual's `*` means "read the sentence printed under the table". Those sentences are the
substance of the whole thing, so each one becomes a numbered note below and the `*` is replaced by
its number, set as a superscript link: <sup>[4](#n4)</sup>. Identical sentences share a number —
the commonest is used 28 times — so the 193 asterisk cells reduce to 60 notes.

**A superscript number is a note reference; a plain digit is the manual's own value.** The two can
only be confused in one place: `CLR`'s Z cell prints `1`, meaning *always set*, and it is the only
`1` in the manual. It is set as a plain digit, and note 1 is set as a superscript.

`—`, `0`, `1` and `U` need no note: every one of the 117 table cells carrying them reads exactly
*Not affected.*, *Always cleared.*, *Always set.* or *Undefined.* respectively, with no
exceptions, and no `*` cell ever reads one of those four sentences.

Where the manual prints one sentence in place of the whole table, the `Form` is *prose*. *Not
affected.* is the exact prose equivalent of five em dashes and is shown as such; the six
conditional bodies get one note, repeated across all five bits, because that is precisely what the
manual says — the sentence covers the register, not a bit.

## Condition codes by instruction

122 instructions, in the manual's own order: Section 4 alphabetically, then
Section 6. `Form` is *table* where the manual prints the five cells, *prose* where
it prints one sentence instead, and *absent* where it prints nothing at all.

| Instruction | Description | Form | X | N | Z | V | C |
|---|---|---|:-:|:-:|:-:|:-:|:-:|
| `ABCD` | Add Decimal with Extend | table | <sup>[1](#n1)</sup> | U | <sup>[2](#n2)</sup> | U | <sup>[3](#n3)</sup> |
| `ADD` | Add | table | <sup>[1](#n1)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[6](#n6)</sup> | <sup>[7](#n7)</sup> |
| `ADDA` | Add Address | prose | — | — | — | — | — |
| `ADDI` | Add Immediate | table | <sup>[1](#n1)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[6](#n6)</sup> | <sup>[7](#n7)</sup> |
| `ADDQ` | Add Quick | table | <sup>[1](#n1)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[8](#n8)</sup> | <sup>[9](#n9)</sup> |
| `ADDX` | Add Extended | table | <sup>[1](#n1)</sup> | <sup>[4](#n4)</sup> | <sup>[2](#n2)</sup> | <sup>[8](#n8)</sup> | <sup>[7](#n7)</sup> |
| `AND` | AND Logical | table | — | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `ANDI` | AND Immediate | table | — | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `ANDI to CCR` | CCR AND Immediate | table | <sup>[11](#n11)</sup> | <sup>[12](#n12)</sup> | <sup>[13](#n13)</sup> | <sup>[14](#n14)</sup> | <sup>[15](#n15)</sup> |
| `ASL, ASR` | Arithmetic Shift | table | <sup>[16](#n16)</sup> | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | <sup>[17](#n17)</sup> | <sup>[18](#n18)</sup> |
| `Bcc` | Branch Conditionally | prose | — | — | — | — | — |
| `BCHG` | Test a Bit and Change | table | — | — | <sup>[19](#n19)</sup> | — | — |
| `BCLR` | Test a Bit and Clear | table | — | — | <sup>[19](#n19)</sup> | — | — |
| `BFCHG` | Test Bit Field and Change | table | — | <sup>[20](#n20)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BFCLR` | Test Bit Field and Clear | table | — | <sup>[20](#n20)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BFEXTS` | Extract Bit Field Signed | table | — | <sup>[20](#n20)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BFEXTU` | Extract Bit Field Unsigned | table | — | <sup>[22](#n22)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BFFFO` | Find First One in Bit Field | table | — | <sup>[20](#n20)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BFINS` | Insert Bit Field | table | — | <sup>[20](#n20)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BFSET` | Test Bit Field and Set | table | — | <sup>[20](#n20)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BFTST` | Test Bit Field | table | — | <sup>[20](#n20)</sup> | <sup>[21](#n21)</sup> | 0 | 0 |
| `BKPT` | Breakpoint | prose | — | — | — | — | — |
| `BRA` | Branch Always | prose | — | — | — | — | — |
| `BSET` | Test a Bit and Set | table | — | — | <sup>[19](#n19)</sup> | — | — |
| `BSR` | Branch to Subroutine | prose | — | — | — | — | — |
| `BTST` | Test a Bit | table | — | — | <sup>[19](#n19)</sup> | — | — |
| `CALLM` | Call Module | prose | — | — | — | — | — |
| `CAS, CAS2` | Compare and Swap with Operand | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[6](#n6)</sup> | <sup>[23](#n23)</sup> |
| `CHK` | Check Register Against Bounds | table | — | <sup>[24](#n24)</sup> | U | U | U |
| `CHK2` | Check Register Against Bounds | table | — | U | <sup>[25](#n25)</sup> | U | <sup>[26](#n26)</sup> |
| `CLR` | Clear an Operand | table | — | 0 | 1 | 0 | 0 |
| `CMP` | Compare | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[8](#n8)</sup> | <sup>[27](#n27)</sup> |
| `CMPA` | Compare Address | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[6](#n6)</sup> | <sup>[23](#n23)</sup> |
| `CMPI` | Compare Immediate | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[8](#n8)</sup> | <sup>[27](#n27)</sup> |
| `CMPM` | Compare Memory | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[6](#n6)</sup> | <sup>[23](#n23)</sup> |
| `CMP2` | Compare Register Against Bounds | table | — | U | <sup>[25](#n25)</sup> | U | <sup>[26](#n26)</sup> |
| `cpBcc` | Branch on Coprocessor Condition | prose | — | — | — | — | — |
| `cpDBcc` | Test Coprocessor Condition Decrement and Branch | prose | — | — | — | — | — |
| `cpGEN` | Coprocessor General Function | prose | <sup>[28](#n28)</sup> | <sup>[28](#n28)</sup> | <sup>[28](#n28)</sup> | <sup>[28](#n28)</sup> | <sup>[28](#n28)</sup> |
| `cpScc` | Set on Coprocessor Condition | prose | — | — | — | — | — |
| `cpTRAPcc` | Trap on Coprocessor Condition | prose | — | — | — | — | — |
| `DBcc` | Test Condition, Decrement, and Branch | prose | — | — | — | — | — |
| `DIVS, DIVSL` | Signed Divide | table | — | <sup>[29](#n29)</sup> | <sup>[30](#n30)</sup> | <sup>[31](#n31)</sup> | 0 |
| `DIVU, DIVUL` | Unsigned Divide | table | — | <sup>[29](#n29)</sup> | <sup>[30](#n30)</sup> | <sup>[32](#n32)</sup> | 0 |
| `EOR` | Exclusive-OR Logical | table | — | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `EORI` | Exclusive-OR Immediate | table | — | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `EORI to CCR` | Exclusive-OR Immediate to Condition Code | table | <sup>[33](#n33)</sup> | <sup>[34](#n34)</sup> | <sup>[35](#n35)</sup> | <sup>[36](#n36)</sup> | <sup>[37](#n37)</sup> |
| `EXG` | Exchange Registers | prose | — | — | — | — | — |
| `EXT, EXTB` | Sign-Extend | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `ILLEGAL` | Take Illegal Instruction Trap | prose | — | — | — | — | — |
| `JMP` | Jump | prose | — | — | — | — | — |
| `JSR` | Jump to Subroutine | prose | — | — | — | — | — |
| `LEA` | Load Effective Address | prose | — | — | — | — | — |
| `LINK` | Link and Allocate | prose | — | — | — | — | — |
| `LSL, LSR` | Logical Shift | table | <sup>[16](#n16)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | 0 | <sup>[18](#n18)</sup> |
| `MOVE` | Move Data from Source to Destination | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `MOVEA` | Move Address | prose | — | — | — | — | — |
| `MOVE from CCR` | Move from the Condition Code Register | prose | — | — | — | — | — |
| `MOVE to CCR` | Move to Condition Code Register | table | <sup>[38](#n38)</sup> | <sup>[39](#n39)</sup> | <sup>[40](#n40)</sup> | <sup>[41](#n41)</sup> | <sup>[42](#n42)</sup> |
| `MOVE from SR` | Move from the Status Register (MC68000, MC68008) | prose | — | — | — | — | — |
| `MOVE16` | Move 16-Byte Block | prose | — | — | — | — | — |
| `MOVEM` | Move Multiple Registers | prose | — | — | — | — | — |
| `MOVEP` | Move Peripheral Data | prose | — | — | — | — | — |
| `MOVEQ` | Move Quick | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `MULS` | Signed Multiply | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[43](#n43)</sup> | 0 |
| `MULU` | Unsigned Multiply | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[43](#n43)</sup> | 0 |
| `NBCD` | Negate Decimal with Extend | table | <sup>[1](#n1)</sup> | U | <sup>[2](#n2)</sup> | U | <sup>[44](#n44)</sup> |
| `NEG` | Negate | table | <sup>[1](#n1)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[8](#n8)</sup> | <sup>[45](#n45)</sup> |
| `NEGX` | Negate with Extend | table | <sup>[1](#n1)</sup> | <sup>[4](#n4)</sup> | <sup>[2](#n2)</sup> | <sup>[8](#n8)</sup> | <sup>[27](#n27)</sup> |
| `NOP` | No Operation | prose | — | — | — | — | — |
| `NOT` | Logical Complement | table | — | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `OR` | Inclusive-OR Logical | table | — | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `ORI` | Inclusive-OR | table | — | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | 0 |
| `ORI to CCR` | Inclusive-OR Immediate to Condition Codes | table | <sup>[46](#n46)</sup> | <sup>[47](#n47)</sup> | <sup>[48](#n48)</sup> | <sup>[49](#n49)</sup> | <sup>[50](#n50)</sup> |
| `PACK` | Pack | prose | — | — | — | — | — |
| `PEA` | Push Effective Address | prose | — | — | — | — | — |
| `ROL, ROR` | Rotate (Without Extend) | table | — | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | <sup>[51](#n51)</sup> |
| `ROXL, ROXR` | Rotate with Extend | table | <sup>[52](#n52)</sup> | <sup>[10](#n10)</sup> | <sup>[5](#n5)</sup> | 0 | <sup>[53](#n53)</sup> |
| `RTD` | Return and Deallocate | prose | — | — | — | — | — |
| `RTM` | Return from Module | prose | <sup>[54](#n54)</sup> | <sup>[54](#n54)</sup> | <sup>[54](#n54)</sup> | <sup>[54](#n54)</sup> | <sup>[54](#n54)</sup> |
| `RTR` | Return and Restore Condition Codes | prose | <sup>[55](#n55)</sup> | <sup>[55](#n55)</sup> | <sup>[55](#n55)</sup> | <sup>[55](#n55)</sup> | <sup>[55](#n55)</sup> |
| `RTS` | Return from Subroutine | prose | — | — | — | — | — |
| `SBCD` | Subtract Decimal with Extend | table | <sup>[1](#n1)</sup> | U | <sup>[2](#n2)</sup> | U | <sup>[56](#n56)</sup> |
| `Scc` | Set According to Condition | prose | — | — | — | — | — |
| `SUB` | Subtract | table | <sup>[57](#n57)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[6](#n6)</sup> | <sup>[23](#n23)</sup> |
| `SUBA` | Subtract Address | prose | — | — | — | — | — |
| `SUBI` | Subtract Immediate | table | <sup>[57](#n57)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[8](#n8)</sup> | <sup>[27](#n27)</sup> |
| `SUBQ` | Subtract Quick | table | <sup>[57](#n57)</sup> | <sup>[4](#n4)</sup> | <sup>[5](#n5)</sup> | <sup>[8](#n8)</sup> | <sup>[27](#n27)</sup> |
| `SUBX` | Subtract with Extend | table | <sup>[57](#n57)</sup> | <sup>[4](#n4)</sup> | <sup>[2](#n2)</sup> | <sup>[8](#n8)</sup> | <sup>[27](#n27)</sup> |
| `SWAP` | Swap Register Halves | table | — | <sup>[58](#n58)</sup> | <sup>[59](#n59)</sup> | 0 | 0 |
| `TAS` | Test and Set an Operand | table | — | <sup>[60](#n60)</sup> | <sup>[61](#n61)</sup> | 0 | 0 |
| `TRAP` | Trap | prose | — | — | — | — | — |
| `TRAPcc` | Trap on Condition | prose | — | — | — | — | — |
| `TRAPV` | Trap on Overflow | prose | — | — | — | — | — |
| `TST` | Test an Operand | table | — | <sup>[62](#n62)</sup> | <sup>[63](#n63)</sup> | 0 | 0 |
| `UNLK` | Unlink | prose | — | — | — | — | — |
| `UNPK` | Unpack BCD | prose | — | — | — | — | — |
| `ANDI to SR` | AND Immediate to the Status Register | table | <sup>[11](#n11)</sup> | <sup>[12](#n12)</sup> | <sup>[13](#n13)</sup> | <sup>[14](#n14)</sup> | <sup>[15](#n15)</sup> |
| `CINV` | Invalidate Cache Lines | prose | — | — | — | — | — |
| `cpRESTORE` | Coprocessor Restore Functions | prose | — | — | — | — | — |
| `cpSAVE` | Coprocessor Save Function | prose | — | — | — | — | — |
| `CPUSH` | Push and Invalidate Cache Lines | prose | — | — | — | — | — |
| `EORI to SR` | Exclusive-OR Immediate to the Status Register | table | <sup>[33](#n33)</sup> | <sup>[34](#n34)</sup> | <sup>[35](#n35)</sup> | <sup>[36](#n36)</sup> | <sup>[37](#n37)</sup> |
| `MOVE from SR` | Move from the Status Register (MC68EC000, MC68010, MC68020, MC68030, MC68040, CPU32) | prose | — | — | — | — | — |
| `MOVE to SR` | Move to the Status Register | prose | <sup>[64](#n64)</sup> | <sup>[64](#n64)</sup> | <sup>[64](#n64)</sup> | <sup>[64](#n64)</sup> | <sup>[64](#n64)</sup> |
| `MOVE USP` | Move User Stack Pointer | prose | — | — | — | — | — |
| `MOVEC` | Move Control Register | prose | — | — | — | — | — |
| `MOVES` | Move Address Space | prose | — | — | — | — | — |
| `ORI to SR` | Inclusive-OR Immediate to the Status Register | table | <sup>[46](#n46)</sup> | <sup>[47](#n47)</sup> | <sup>[48](#n48)</sup> | <sup>[49](#n49)</sup> | <sup>[50](#n50)</sup> |
| `PFLUSH` | Flush Entry in the ATC (MC68030 only) | prose | — | — | — | — | — |
| `PFLUSH` | Flush ATC Entries (MC68040, MC68LC040) | prose | — | — | — | — | — |
| `PFLUSH` | Flush ATC Entries (MC68EC040) | prose | — | — | — | — | — |
| `PLOAD` | Load an Entry into the ATC | absent | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> |
| `PMOVE` | Move to/from MMU Registers (MC68030 only) | prose | — | — | — | — | — |
| `PMOVE` | Move to/from MMU Registers (MC68EC030) | prose | — | — | — | — | — |
| `PTEST` | Test a Logical Address (MC68030 only) | prose | — | — | — | — | — |
| `PTEST` | Test a Logical Address (MC68EC030) | prose | — | — | — | — | — |
| `PTEST` | Test a Logical Address (MC68040, MC68LC040) | prose | — | — | — | — | — |
| `PTEST` | Test a Logical Address (MC68EC040) | absent | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> | <sup>[65](#n65)</sup> |
| `RESET` | Reset External Devices | prose | — | — | — | — | — |
| `RTE` | Return from Exception | prose | <sup>[66](#n66)</sup> | <sup>[66](#n66)</sup> | <sup>[66](#n66)</sup> | <sup>[66](#n66)</sup> | <sup>[66](#n66)</sup> |
| `STOP` | Load Status Register and Stop | prose | <sup>[67](#n67)</sup> | <sup>[67](#n67)</sup> | <sup>[67](#n67)</sup> | <sup>[67](#n67)</sup> | <sup>[67](#n67)</sup> |

## Notes

The sentence the manual prints under the table for each `*` cell. Identical
sentences share a number; `uses` is how many cells point here.

| # | Explanation | Uses |
|--:|---|--:|
| <a id="n1"></a>1 | Set the same as the carry bit. | 9 |
| <a id="n2"></a>2 | Cleared if the result is nonzero; unchanged otherwise. | 6 |
| <a id="n3"></a>3 | Set if a decimal carry was generated; cleared otherwise. | 1 |
| <a id="n4"></a>4 | Set if the result is negative; cleared otherwise. | 22 |
| <a id="n5"></a>5 | Set if the result is zero; cleared otherwise. | 28 |
| <a id="n6"></a>6 | Set if an overflow is generated; cleared otherwise. | 6 |
| <a id="n7"></a>7 | Set if a carry is generated; cleared otherwise. | 3 |
| <a id="n8"></a>8 | Set if an overflow occurs; cleared otherwise. | 9 |
| <a id="n9"></a>9 | Set if a carry occurs; cleared otherwise. | 1 |
| <a id="n10"></a>10 | Set if the most significant bit of the result is set; cleared otherwise. | 9 |
| <a id="n11"></a>11 | Cleared if bit 4 of immediate operand is zero; unchanged otherwise. | 2 |
| <a id="n12"></a>12 | Cleared if bit 3 of immediate operand is zero; unchanged otherwise. | 2 |
| <a id="n13"></a>13 | Cleared if bit 2 of immediate operand is zero; unchanged otherwise. | 2 |
| <a id="n14"></a>14 | Cleared if bit 1 of immediate operand is zero; unchanged otherwise. | 2 |
| <a id="n15"></a>15 | Cleared if bit 0 of immediate operand is zero; unchanged otherwise. | 2 |
| <a id="n16"></a>16 | Set according to the last bit shifted out of the operand; unaffected for a shift count of zero. | 2 |
| <a id="n17"></a>17 | Set if the most significant bit is changed at any time during the shift operation; cleared otherwise. | 1 |
| <a id="n18"></a>18 | Set according to the last bit shifted out of the operand; cleared for a shift count of zero. | 2 |
| <a id="n19"></a>19 | Set if the bit tested is zero; cleared otherwise. | 4 |
| <a id="n20"></a>20 | Set if the most significant bit of the field is set; cleared otherwise. | 7 |
| <a id="n21"></a>21 | Set if all bits of the field are zero; cleared otherwise. | 8 |
| <a id="n22"></a>22 | Set if the most significant bit of the source field is set; cleared otherwise. | 1 |
| <a id="n23"></a>23 | Set if a borrow is generated; cleared otherwise. | 4 |
| <a id="n24"></a>24 | Set if Dn < 0; cleared if Dn > effective address operand; undefined otherwise. | 1 |
| <a id="n25"></a>25 | Set if Rn is equal to either bound; cleared otherwise. | 2 |
| <a id="n26"></a>26 | Set if Rn is out of bounds; cleared otherwise. | 2 |
| <a id="n27"></a>27 | Set if a borrow occurs; cleared otherwise. | 6 |
| <a id="n28"></a>28 | May be modified by coprocessor; unchanged otherwise. | 5 |
| <a id="n29"></a>29 | Set if the quotient is negative; cleared otherwise; undefined if overflow or divide by zero occurs. | 2 |
| <a id="n30"></a>30 | Set if the quotient is zero; cleared otherwise; undefined if overflow or divide by zero occurs. | 2 |
| <a id="n31"></a>31 | Set if division overflow occurs; undefined if divide by zero occurs; cleared otherwise. | 1 |
| <a id="n32"></a>32 | Set if division overflow occurs; cleared otherwise; undefined if divide by zero occurs. | 1 |
| <a id="n33"></a>33 | Changed if bit 4 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n34"></a>34 | Changed if bit 3 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n35"></a>35 | Changed if bit 2 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n36"></a>36 | Changed if bit 1 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n37"></a>37 | Changed if bit 0 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n38"></a>38 | Set to the value of bit 4 of the source operand. | 1 |
| <a id="n39"></a>39 | Set to the value of bit 3 of the source operand. | 1 |
| <a id="n40"></a>40 | Set to the value of bit 2 of the source operand. | 1 |
| <a id="n41"></a>41 | Set to the value of bit 1 of the source operand. | 1 |
| <a id="n42"></a>42 | Set to the value of bit 0 of the source operand. | 1 |
| <a id="n43"></a>43 | Set if overflow; cleared otherwise. | 2 |
| <a id="n44"></a>44 | Set if a decimal borrow occurs; cleared otherwise. | 1 |
| <a id="n45"></a>45 | Cleared if the result is zero; set otherwise. | 1 |
| <a id="n46"></a>46 | Set if bit 4 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n47"></a>47 | Set if bit 3 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n48"></a>48 | Set if bit 2 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n49"></a>49 | Set if bit 1 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n50"></a>50 | Set if bit 0 of immediate operand is one; unchanged otherwise. | 2 |
| <a id="n51"></a>51 | Set according to the last bit rotated out of the operand; cleared when the rotate count is zero. | 1 |
| <a id="n52"></a>52 | Set to the value of the last bit rotated out of the operand; unaffected when the rotate count is zero. | 1 |
| <a id="n53"></a>53 | Set according to the last bit rotated out of the operand; when the rotate count is zero, set to the value of the extend bit. | 1 |
| <a id="n54"></a>54 | Set according to the content of the word on the stack. | 5 |
| <a id="n55"></a>55 | Set to the condition codes from the stack. | 5 |
| <a id="n56"></a>56 | Set if a borrow (decimal) is generated; cleared otherwise. | 1 |
| <a id="n57"></a>57 | Set to the value of the carry bit. | 4 |
| <a id="n58"></a>58 | Set if the most significant bit of the 32-bit result is set; cleared otherwise. | 1 |
| <a id="n59"></a>59 | Set if the 32-bit result is zero; cleared otherwise. | 1 |
| <a id="n60"></a>60 | Set if the most significant bit of the operand is currently set; cleared otherwise. | 1 |
| <a id="n61"></a>61 | Set if the operand was zero; cleared otherwise. | 1 |
| <a id="n62"></a>62 | Set if the operand is negative; cleared otherwise. | 1 |
| <a id="n63"></a>63 | Set if the operand is zero; cleared otherwise. | 1 |
| <a id="n64"></a>64 | Set according to the source operand. | 5 |
| <a id="n65"></a>65 | The manual prints no Condition Codes section for this description. | 10 |
| <a id="n66"></a>66 | Set according to the condition code bits in the status register value restored from the stack. | 5 |
| <a id="n67"></a>67 | Set according to the immediate operand. | 5 |

## Qualifications printed with the table

Nine descriptions print something further under the explanations — eight a centred
`NOTE`, and `ADDQ` a bare sentence. They qualify the table above them, so they are
carried here verbatim.

| Instruction | Printed under the table |
|---|---|
| `ABCD` | Normally, the Z condition code bit is set via programming before the start of an operation. This allows successful tests for zero results upon completion of multiple-precision operations. |
| `ADDQ` | The condition codes are not affected when the destination is an address register. |
| `ADDX` | Normally, the Z condition code bit is set via programming before the start of an operation. This allows successful tests for zero results upon completion of multiple-precision operations. |
| `MULS` | Overflow (V = 1) can occur only when multiplying 32-bit operands to yield a 32-bit result. Overflow occurs if the high-order 32 bits of the quad-word product are not the sign extension of the low-order 32 bits. |
| `MULU` | Overflow (V = 1) can occur only when multiplying 32-bit operands to yield a 32-bit result. Overflow occurs if any of the high-order 32 bits of the quad-word product are not equal to zero. |
| `NBCD` | Normally the Z condition code bit is set via programming before the start of the operation. This allows successful tests for zero results upon completion of multiple-precision operations. |
| `NEGX` | Normally the Z condition code bit is set via programming before the start of the operation. This allows successful tests for zero results upon completion of multiple-precision operations. |
| `SBCD` | Normally the Z condition code bit is set via programming before the start of an operation. This allows successful tests for zero results upon completion of multiple-precision operations. |
| `SUBX` | Normally the Z condition code bit is set via programming before the start of an operation. This allows successful tests for zero results upon completion of multiple-precision operations. |

## Cross-check against Table 3-18

Table 3-18, *Integer Unit Condition Code Computations* (printed pages 3-18 and 3-19), states the
same facts a second time, in a different notation and with the instructions grouped: `*` there
means *set by the standard definition*, `?` means *see the Special Definition column*, and the
column then gives the boolean formula. Both map onto the instruction pages' `*`; `—`, `0` and `U`
map onto themselves.

That makes it a genuine independent statement rather than a restatement, and
[`check-condition-codes.py`](check-condition-codes.py) compares the two cell by cell.
It is carried here as
[`table-3-18-condition-code-computations.csv`](table-3-18-condition-code-computations.csv).

The seven shift-count-qualified rows — `ASL (r = 0)`, `ROXL (r = 0)` and so on — are finer-grained
than the instruction pages, which fold the zero-count case into the sentence rather than giving it
a row. They corroborate the *sentences*: Table 3-18 gives `ASL (r = 0)` an X of `—` and a C of
`0`, which is exactly what `ASL`'s own notes say happens when the shift count is zero.

**The Special Definition column's formulas are transcribed but should not be relied on.** They
come out of the text layer as, for instance, `V = Sm Λ Dm Λ Rm V Sm Λ Dm Λ Rm` — the same term
twice, which cannot be what is meant. The two differ by complement bars that the extraction drops,
and there is no way to recover an overbar from a text layer. The value columns are unaffected;
only the formulas are.

## Documentation discrepancies

Eighteen places where the manual contradicts itself, misprints something, or says
one thing two ways. Each was checked against the page it cites. Nothing here is
corrected in the table or the CSVs — what the manual prints is what lands there.

### 1. Table 3-18 gives `CLR` a computed N and Z where its own page gives constants — *substantive*

Table 3-18 groups `CLR` into the fourteen-instruction row
`AND, ANDI, EOR, EORI, MOVEQ, MOVE, OR, ORI, CLR, EXT, EXTB, NOT, TAS, TST` and gives the whole
group N = `*` and Z = `*` — set from the result in the standard way. `CLR`'s own description
(printed page 4-73) gives N = `0` and Z = `1`.

Both describe the same behaviour, since the result of a clear is always zero, so the standard
computation always yields N = 0 and Z = 1. But only the instruction page says so as a constant,
which is the more useful statement and the one a reader wants. Read as an artefact of grouping
`CLR` with thirteen instructions whose result is not constant. This document follows the
instruction page.

### 2. Table 3-18 splits `ASL` from `ASR` on V, where the shared description cannot — *substantive*

`ASL` and `ASR` are documented together, in one description with one table, which gives V = `*`
and the sentence *"Set if the most significant bit is changed at any time during the shift
operation; cleared otherwise."*

Table 3-18 gives them separate rows and different values: `ASL` has V = `?`, with an overflow
formula in the Special Definition column, while `ASR, LSR, ROXR` has V = `0`.

Table 3-18 is right, and the shared table cannot express it. An arithmetic shift right replicates
the sign bit, so the most significant bit never changes and V is always cleared — which is what
`LSR`, `ROR` and `ROXR` all print as a flat `0` on their own pages. `ASR` gets a conditional V
only because it shares a table with `ASL`, where the condition is real. This is the one cell where
the two sources genuinely disagree.

### 3. `PTEST (MC68EC040)` has no condition-code section at all — *substantive*

Alone among the 139 instruction descriptions in Sections 4, 6 and 7, the MC68EC040 form of
`PTEST` (printed page 6-72) carries neither a `Condition Codes:` block nor any status-register
block in its place. Its four sibling `PTEST` descriptions all carry one: the MC68030, MC68EC030
and MC68040/MC68LC040 forms print `Condition Codes: / Not affected.`, and the MC68851 form prints
a `PMMU Status Register:` table.

There is no reason to think the MC68EC040 form behaves differently from the other three; the
statement is simply missing. Shown here with all five bits carrying a note saying so, rather than
guessed at.

### 4. `PLOAD` never states its effect on the condition codes — *substantive*

`PLOAD (MC68030 only, MC68851)` (printed page 6-43) documents only the PMMU status register.
Its neighbour `PFLUSH (MC68030 only)`, an instruction of the same kind on the same processor, does
print `Condition Codes: / Not affected.`

So for the MC68030 form of `PLOAD` — an instruction of the CPU, not of a coprocessor — the effect
on the CCR is never stated anywhere in the manual.

### 5. Table 3-18 spells a row label `DIVS, DUVU` — *typo*

The row giving the divide instructions their condition codes is labelled `DIVS, DUVU`.
It is `DIVU`. The row's values match both `DIVS, DIVSL` and `DIVU, DIVUL` on their own pages.

### 6. Table 3-18 loses `LSL (r = 0)` and lists `LSR` twice — *typo*

The continued half of Table 3-18 opens with a row `LSR (r = 0)`. Four rows later comes
`ASR, LSR (r = 0)`, so `LSR`'s zero-count case is given twice, with identical values.

The first of the two should be `LSL (r = 0)`: the preceding half ends with `LSL, ROXL`, every
other shift and rotate in the table has its `(r = 0)` companion, and without it `LSL` is the only
one that does not. As printed, `LSL`'s zero-count case is undocumented in Table 3-18 — though
`LSL`'s own page covers it, in the sentence *"Set according to the last bit shifted out of the
operand; cleared for a shift count of zero."*

### 7. Table 3-18's `CHK2`/`CMP2` carry formula has a stray letter and an unbalanced bracket — *typo*

The Special Definition for `CHK2, CMP2` reads

> C = (LB ≤ UB) Λ (IR < LB) V (R > UB)) V (UB < LB) Λ (R > UB) Λ (R < LB)

`(IR < LB)` is `(R < LB)` — `R` is defined in the table's own legend as *Register Tested*, and
`IR` is not defined anywhere. `(R > UB))` has one closing bracket too many.

### 8. Table 3-18's `ASL` overflow formula mixes two spellings in one expression — *typo*

The Special Definition for `ASL` reads

> V = Dm Λ Dm–1 V…V Dm– r V Dm Λ (DM –1 V …+ Dm – r)

`DM` is `Dm`, and `V …+` uses `V` and `+` for the same OR within a single expression — the rest of
the table uses `V` throughout.

### 9. `DIVS` sets one explanation line without spaces around the dash — *typo*

`DIVS, DIVSL`'s X line is set `X—Not affected.` where its own N, Z, V and C lines four lines
below, `DIVU, DIVUL` on the facing pages, and all 58 other Section 4 tables are set
`X — Not affected.` with spaces.

It is the only such line in Section 4. Section 6 sets all fifteen of its explanation lines the
compressed way, so the manual is inconsistent between sections as well as within `DIVS`.

### 10. `DIVS` and `DIVU` state one rule in opposite clause order — *imprecision*

`DIVS, DIVSL`'s V reads *"Set if division overflow occurs; undefined if divide by zero
occurs; cleared otherwise."* and `DIVU, DIVUL`'s reads *"Set if division overflow occurs; cleared
otherwise; undefined if divide by zero occurs."*

Same rule, clauses swapped, so two notes exist below where one would do.

### 11. The carry, borrow and overflow sentences split without a pattern — *imprecision*

The same event is *generated* in some descriptions and *occurs* in others, with no
distinction that the manual explains:

| Sentence | Instructions |
|---|---|
| Set if an overflow **is generated**; cleared otherwise. | `ADD`, `ADDI`, `CAS, CAS2`, `CMPA`, `CMPM`, `SUB` |
| Set if an overflow **occurs**; cleared otherwise. | `ADDQ`, `ADDX`, `CMP`, `CMPI`, `NEG`, `NEGX`, `SUBI`, `SUBQ`, `SUBX` |
| Set if a carry **is generated**; cleared otherwise. | `ADD`, `ADDI`, `ADDX` |
| Set if a carry **occurs**; cleared otherwise. | `ADDQ` |
| Set if a borrow **is generated**; cleared otherwise. | `CAS, CAS2`, `CMPA`, `CMPM`, `SUB` |
| Set if a borrow **occurs**; cleared otherwise. | `CMP`, `CMPI`, `NEGX`, `SUBI`, `SUBQ`, `SUBX` |

`ADD` and `ADDQ` differ on both bits; `ADDX` takes *is generated* for C and *occurs* for V, in the
same table.

### 12. The X bit splits the same way, cleanly along add against subtract — *imprecision*

*"Set the same as the carry bit."* is used by `ABCD`, `ADD`, `ADDI`, `ADDQ`, `ADDX`, `NBCD`,
`NEG` and `NEGX`; *"Set to the value of the carry bit."* by `SUB`, `SUBI`, `SUBQ` and `SUBX`.

Unlike the previous entry this one is at least consistent — every subtract uses the second form
and nothing else does — but the two sentences say the same thing.

### 13. `MULS` and `MULU` give the only condition-code sentence with no verb — *imprecision*

Both read *"Set if overflow; cleared otherwise."* for V. Every other overflow sentence in the
manual is *"Set if an overflow occurs"* or *"…is generated"*.

### 14. `BFEXTU` says *source field* where its seven siblings say *field* — *imprecision*

`BFEXTU`'s N reads *"Set if the most significant bit of the source field is set; cleared
otherwise."* `BFCHG`, `BFCLR`, `BFEXTS`, `BFFFO`, `BFINS`, `BFSET` and `BFTST` all read *"…of the
field…"*, `BFEXTS` — its signed twin, doing the same thing to the same operand — included.

### 15. The three BCD carry sentences are all different — *imprecision*

`ABCD` reads *"Set if a decimal carry was generated; cleared otherwise."* — the only past
tense in any condition-code sentence in the manual. `NBCD` reads *"Set if a decimal borrow occurs;
cleared otherwise."* `SBCD` reads *"Set if a borrow (decimal) is generated; cleared otherwise."*
Three instructions of one family, three constructions.

### 16. The NOTE about presetting Z is printed in three versions — *imprecision*

Eight instructions carry the same NOTE about setting Z before a multiple-precision operation,
in three wordings: *"Normally, the Z condition code bit … of an operation."* (`ABCD`, `ADDX`),
*"Normally the Z condition code bit … of an operation."* (`SBCD`, `SUBX`), and *"Normally the Z
condition code bit … of the operation."* (`NBCD`, `NEGX`). The comma and the article each vary
independently.

### 17. Table 3-18 defines `?` and leaves the rest of its alphabet to Table 3-1 — *imprecision*

The legend under Table 3-18 defines `? = Other—See Special Definition` and then goes on to
the operand abbreviations. `*`, `—`, `U` and `0` — four of the five symbols in its own value
columns — are not defined there at all. They are defined in Table 3-1, fifteen printed pages
earlier, under the heading *Register Codes*, where `*` is given as *General Case*, which is not
the sense Table 3-18 uses it in.

### 18. The three `… to CCR` instructions have three styles of title — *imprecision*

`ANDI to CCR` is titled *CCR AND Immediate*, `EORI to CCR` is *Exclusive-OR Immediate to
Condition Code* (singular), and `ORI to CCR` is *Inclusive-OR Immediate to Condition Codes*
(plural). The three are the same instruction over three operations, and their `… to SR`
counterparts in Section 6 are titled uniformly.

### Not discrepancies

Things that look wrong in a mechanical comparison and are not.

- **`BGND` prints a full table of five em dashes** where the 52 other instructions whose codes are untouched
  print the sentence *Not affected.* The two are the same statement in the manual's two available forms.
- **`MOVE from SR` is documented twice** — in Section 4 as `(MC68000, MC68008)` and in Section 6 as
  `(MC68EC000, MC68010, MC68020, MC68030, MC68040, CPU32)` — because it is unprivileged on the
  first two parts and privileged on the rest. Both say *Not affected.*, as do all three `PFLUSH`
  descriptions, both non-coprocessor `PMOVE`s and the three `PTEST`s that state anything.
- **`CHK`'s N cell is `*` while X, Z, V and C are `U`.** The sentence is a three-way one, *"Set if
  Dn < 0; cleared if Dn > effective address operand; undefined otherwise."* — so N is genuinely
  conditional and `*` is right. Table 3-18 independently prints `CHK` as `— * U U U`.
- **`TAS` says *"was zero"* and *"is currently set"*** where other instructions use the present
  tense, because `TAS` writes the operand it has just tested; the tense is carrying real meaning.
- **`SWAP` says *"the 32-bit result"*** rather than *"the result"* because `SWAP` is long-only.
- **`ANDI to CCR`, `EORI to CCR` and `ORI to CCR` use three different sentences** — *Cleared if bit
  n of immediate operand is zero*, *Changed if bit n … is one*, *Set if bit n … is one*. Each is
  correct for its own operation, and each is shared exactly with the corresponding `… to SR`
  instruction in Section 6.
- **`∗` and `*` are one symbol.** The manual sets 151 of its asterisks in Symbol (U+2217 ASTERISK
  OPERATOR) and 48 in Helvetica (U+002A). The split follows the font, never the meaning.

## Method and caveats

Everything in the table and the notes was extracted mechanically by
[`make-condition-codes.py`](make-condition-codes.py) from the split PDFs in this directory, and
checked by [`check-condition-codes.py`](check-condition-codes.py) against three independent
readings. Nothing was transcribed by hand. Both scripts read the tracked split parts rather than
`../M68000PRM.pdf`, which is deliberately untracked, so they run on a fresh clone.

- Descriptions are delimited by their `Operation:` line — 139 of them across Sections 4, 6 and 7.
  The mnemonic, title and processor annotation come from the running head, which needs three
  patterns: the ordinary `MNEM  Title  MNEM`, the two-line form where the mnemonic itself wraps
  (`ANDI` / `to CCR`), and the form where a wide title squeezes the separators down to single
  spaces (`cpTRAPcc Trap on Coprocessor Condition cpTRAPcc`).
- The `Condition Codes:` anchor has to allow the label mid-line: in `MOVE`, alone among the 139, it
  is run on to the end of the preceding paragraph — `…or long. Condition Codes:`. Requiring the
  line to *end* at `Codes:` is what keeps the `Operation:` lines, the `RTR Return and Restore
  Condition Codes RTR` running head and the `ORI to CCR` title out.
- Values are read **by token order, never by column**: the value row is not always aligned under
  its header. Binding the table to the `X N Z V C` header row is also what keeps the `MMUSR:`,
  `MMU Status Register:` and `ACUSR:` tables out — they use the same `*` and `0` alphabet, but a
  different header.
- Sixteen explanation sentences wrap onto a second line. They are rejoined by reading on until the
  sentence ends in a full stop; a fragment left ending in a hyphen is a split word and rejoins with
  no space, which happens once — `DIVS`'s *"cleared oth-"* / *"erwise."*

**Superscripts are lost by the text layer.** The V sentence of `TBLS` and `TBLU` extracts as
`– (223) ≤ Result ≤ (223) – 1`, which is `−(2^23) ≤ Result ≤ (2^23) − 1`. Those two are CPU32-only
and so fall outside the table above, but the extraction repairs them anyway, and that they are the
only affected sentences is not assumed: `pdftotext -bbox` measures every explanation line in all
three sections and finds sub-size digits on exactly those two.

**Overbars are lost too**, which is why Table 3-18's Special Definition column is carried but not
relied on — see [Cross-check against Table 3-18](#cross-check-against-table-3-18) above.

One count worth reconciling. [`README.md`](README.md) describes Sections 4–7 as *"175 instruction
descriptions"*, counting the entries in its own reconstructed bookmark lists. Segmenting by
`Operation:` gives 186 across those four sections — the difference being the mnemonics documented
more than once, which the bookmark list names once and this count reaches separately.

## Regenerating

```sh
python3 make-condition-codes.py    # rewrites the three CSVs and this document
python3 check-condition-codes.py   # re-reads the PDFs and checks them
```
