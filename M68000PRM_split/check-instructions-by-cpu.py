#!/usr/bin/env python3
"""Cross-check instructions-by-cpu.csv against the rest of the manual.

make-instructions-by-cpu.py reads Table A-1, and Table A-1 is one table. The
manual states the same facts twice more, so neither claim here rests on it:

  A  Tables A-3, A-4, A-6, A-8, A-10, A-12 and A-13 each list one processor's
     instruction set outright. Every one of them should agree with the
     corresponding column of the matrix.
  B  Every instruction description in Sections 4, 5 and 6 is headed with the
     processors it applies to - "(M68000 Family)", "(MC68020, MC68030,
     MC68040)". Every processor named there should carry a mark in the
     matrix.

Usage:  python3 check-instructions-by-cpu.py

Exits non-zero only on an unexplained mismatch. The places where the manual
genuinely disagrees with itself are listed in KNOWN_SOURCE_DEFECTS, and written
up in INSTRUCTIONS-BY-CPU.md. They are reported rather than failed on, so a
mistake in the extraction is still caught while the manual's own bookkeeping is
not relitigated on every run.
"""
import collections
import csv
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

APPENDIX = '12-appendix-a-processor-instruction-summary.pdf'
SECTIONS = ['07-section-04-integer-instructions.pdf',
            '08-section-05-floating-point-instructions.pdf',
            '09-section-06-supervisor-instructions.pdf']

# Which per-processor table states which column of the matrix.
PER_PROCESSOR = [('A-3', ['MC68000', 'MC68008']), ('A-4', ['MC68010']),
                 ('A-6', ['MC68020']), ('A-8', ['MC68030']),
                 ('A-10', ['MC68040']), ('A-12', ['MC68881/2']),
                 ('A-13', ['MC68851'])]

# What a processor annotation names, in the matrix's column names. Appendix A
# says references to the MC68000, MC68020 and MC68030 include the embedded
# MC68EC000, MC68EC020 and MC68EC030, and the MC68040 includes the LC and EC
# parts, so those all fold into the base column.
ANNOTATION = {
    'M68000 Family': ['MC68000', 'MC68008', 'MC68010', 'MC68020', 'MC68030',
                      'MC68040'],
    'MC68000': ['MC68000'], 'MC68EC000': ['MC68000'], 'MC68008': ['MC68008'],
    'MC68010': ['MC68010'], 'MC68020': ['MC68020'], 'MC68EC020': ['MC68020'],
    'MC68030': ['MC68030'], 'MC68EC030': ['MC68030'], 'MC68040': ['MC68040'],
    'MC68LC040': ['MC68040'], 'MC68EC040': ['MC68040'],
    'MC68881': ['MC68881/2'], 'MC68882': ['MC68881/2'],
    'MC6888X': ['MC68881/2'], 'MC68851': ['MC68851'], 'M68851': ['MC68851'],
}
IGNORED_ANNOTATIONS = {'CPU32', 'M68040FPSP', 'MC68040FPSP'}

# Where the manual disagrees with itself. Each is written up in
# INSTRUCTIONS-BY-CPU.md; reported here, never failed on.
KNOWN_SOURCE_DEFECTS = {
    ('FLOGNP1', 'MC68881/2'):
        'Table A-1 leaves the 68881/68882 column blank where Table A-12 lists the '
        'instruction and its own description is headed (MC6888X, M68040FPSP); '
        'corrected to X in the matrix',
    ('PFLUSHA', 'MC68040'):
        'Table A-1 marks only the MC68030 and MC68851 where Table A-10 lists the '
        'instruction and the neighbouring PFLUSH row does carry an MC68040 mark; '
        'corrected to X in the matrix',
    ('BKPT', 'MC68000'):
        'the Section 4 description is headed (MC68EC000, ...), but Table A-1 leaves '
        'the 68000 column blank and Table A-3 does not list BKPT; the tables are '
        'followed here',
    ('DIVSL', 'MC68000'): 'DIVS and DIVSL share a description headed (M68000 Family); '
                          'the long form is MC68020 and later',
    ('DIVSL', 'MC68008'): 'as DIVSL/MC68000',
    ('DIVSL', 'MC68010'): 'as DIVSL/MC68000',
    ('DIVUL', 'MC68000'): 'DIVU and DIVUL share a description headed (M68000 Family); '
                          'the long form is MC68020 and later',
    ('DIVUL', 'MC68008'): 'as DIVUL/MC68000',
    ('DIVUL', 'MC68010'): 'as DIVUL/MC68000',
    ('EXTB', 'MC68000'): 'EXT and EXTB share a description headed (M68000 Family); '
                         'EXTB is MC68020 and later, which the description says only '
                         'in its Assembler Syntax line',
    ('EXTB', 'MC68008'): 'as EXTB/MC68000',
    ('EXTB', 'MC68010'): 'as EXTB/MC68000',
}

# Mnemonics a per-processor table spells differently from Table A-1.
KNOWN_MISSPELLINGS = {
    'cpTRACPcc': 'Table A-6 transposes the P and the C of cpTRAPcc',
}
MISSPELLED_AS = {'cpTRACPcc': 'cpTRAPcc'}

# Instructions with no description page of their own, documented inside
# another entry, so Section 4/5/6 has no annotation to check them against.
NO_DESCRIPTION = {
    'PFLUSHA', 'PFLUSHS', 'FSABS', 'FDABS', 'FSADD', 'FDADD', 'FSDIV',
    'FDDIV', 'FSMOVE', 'FDMOVE', 'FSMUL', 'FDMUL', 'FSNEG', 'FDNEG',
    'FSSQRT', 'FDSQRT', 'FSSUB', 'FDSUB',
}

LIST_ROW = re.compile(r'^\s{4,}(\S.*?\S|\S)\s{3,}(\S.*?)\s*$')
# Table A-10 emits the footnote markers and the description of FETOX and
# FTWOTOX on the line above the mnemonic, leaving the mnemonic alone on its
# own line with no second column for LIST_ROW to find.
LONE_ROW = re.compile(r'^\s{4,}([A-Za-z][A-Za-z0-9]*(?:,\s?[A-Za-z][A-Za-z0-9]*)*)\s*$')
HEAD = re.compile(r'^\s*\((M?C?68[^)]*|M68000 Family)\)\s*$')


def rows():
    with open(os.path.join(HERE, 'instructions-by-cpu.csv')) as f:
        return list(csv.DictReader(f))


def layout(name):
    return subprocess.run(['pdftotext', '-layout', os.path.join(HERE, name), '-'],
                          capture_output=True, text=True, check=True).stdout


def per_processor_tables():
    """Tables A-3 to A-13, each as the set of mnemonics it lists."""
    lines = layout(APPENDIX).split('\n')
    tables, current = collections.defaultdict(set), None
    for line in lines:
        m = re.search(r'Table (A-\d+)\. ', line)
        if m:
            current = m.group(1)
            continue
        if re.match(r'^\s*(The |Table A-\d+ )', line):
            current = None
        if current is None:
            continue
        m = LIST_ROW.match(line) or LONE_ROW.match(line)
        if not m or m.group(1).startswith('Mnemonic'):
            continue
        for one in re.split(r',\s*', m.group(1).strip()):
            if one and not one.isdigit():
                tables[current].add(one)
    return tables


def strip_marker(name, known):
    """Drop a footnote marker fused to a mnemonic.

    Tables A-8 and A-10 print "MOVES1", "FScc 1" and "FETOXM11,2" - the
    footnote set solid against the mnemonic. Taking the longest prefix that is
    a mnemonic Table A-1 already knows strips those while leaving the genuine
    trailing digits of CMP2, MOVE16, FLOG10 and FETOXM1 alone.
    """
    if name in known:
        return name
    for i in range(len(name) - 1, 0, -1):
        if name[:i] in known:
            return name[:i]
    return name


def check_per_processor(cc, tables):
    """Every per-processor table against its column of the matrix."""
    known = {r['mnemonic'] for r in cc}
    agree = extra = missing = 0
    bad = []
    for tag, columns in PER_PROCESSOR:
        listed = {strip_marker(name, known) for name in tables[tag]}
        listed |= {MISSPELLED_AS[n] for n in listed if n in MISSPELLED_AS}
        for column in columns:
            marked = {r['mnemonic'] for r in cc if r[column]}
            for name in sorted(listed - marked):
                if name in KNOWN_MISSPELLINGS:
                    print('   misspelling   %-10s %-10s %s'
                          % (tag, name, KNOWN_MISSPELLINGS[name]))
                    continue
                extra += 1
                bad.append((name, column, 'listed in %s, not marked in the matrix' % tag))
            for name in sorted(marked - listed):
                if (name, column) in KNOWN_SOURCE_DEFECTS:
                    print('   known defect  %-10s %-10s %s'
                          % (name, column, KNOWN_SOURCE_DEFECTS[(name, column)]))
                    continue
                missing += 1
                bad.append((name, column, 'marked in the matrix, not listed in %s' % tag))
            agree += len(listed & marked)
    print('per-processor tables: %d instructions corroborated across 7 tables, '
          '%d listed but unmarked, %d marked but unlisted' % (agree, extra, missing))
    for name, column, why in bad:
        print('   UNEXPLAINED   %-10s %-10s %s' % (name, column, why))
    return bad


def clean_part(text):
    """One processor out of an annotation, without its qualifiers.

    The annotations qualify some parts - "(MC68030 only, MC68851)",
    "(MC68881, MC68882, MC68040 only)" - and that word is all that has to come
    off. Nothing more may be stripped: every part number ends in digits, so
    trimming trailing digits would turn MC68010 into MC, and "M68000 Family"
    ends in a letter that a character-set strip would eat.
    """
    return re.sub(r'\s*\bonly\b\s*$', '', text.strip())


def description_headers():
    """Every instruction description's processor annotation.

    Returns the processors named, keyed by mnemonic. The head names every
    form the description covers, so "DIVS, DIVSL" claims its annotation for
    both - but only when the description states one annotation. Where it
    states two, as "EXT, EXTB" does, the forms are being distinguished and
    there is no way to tell from the header which annotation belongs to
    which, so only the first form is claimed.
    """
    seen = collections.defaultdict(list)
    for name in SECTIONS:
        for page in layout(name).split('\f'):
            lines = page.split('\n')
            head = None
            for i, line in enumerate(lines):
                if line.startswith('Operation:'):
                    break
                text = line.strip()
                if not text:
                    continue
                if text.startswith('(') and head:
                    while text.count('(') > text.count(')') and i + 1 < len(lines):
                        i += 1
                        text += ' ' + lines[i].strip()
                    m = HEAD.match(text)
                    if m:
                        parts = frozenset(clean_part(p) for p in m.group(1).split(','))
                        if parts not in seen[head]:
                            seen[head].append(parts)
                    break
                m = re.match(r'^(\S+(?:\s\S+)*?)\s{2,}', line)
                if head is None and m:
                    head = tuple(re.split(r',\s*', m.group(1)))
    out = collections.defaultdict(set)
    for head, annotations in seen.items():
        names = head if len(annotations) == 1 else head[:1]
        for one in names:
            for parts in annotations:
                out[one] |= parts
    return out


def check_headers(cc, headers):
    """Every processor an instruction's own description names must be marked."""
    index = {r['mnemonic']: r for r in cc}
    agree = 0
    bad = []
    for mnemonic, parts in headers.items():
        row = index.get(mnemonic)
        if row is None:
            continue
        for part in parts:
            if part in IGNORED_ANNOTATIONS or part not in ANNOTATION:
                continue
            for column in ANNOTATION[part]:
                if row[column]:
                    agree += 1
                elif (mnemonic, column) in KNOWN_SOURCE_DEFECTS:
                    print('   known defect  %-10s %-10s %s'
                          % (mnemonic, column, KNOWN_SOURCE_DEFECTS[(mnemonic, column)]))
                else:
                    bad.append((mnemonic, column,
                                'named by the description header, not marked'))
    print('description headers: %d descriptions read, %d processor claims '
          'corroborated, %d unexplained' % (len(headers), agree, len(bad)))
    for name, column, why in bad:
        print('   UNEXPLAINED   %-10s %-10s %s' % (name, column, why))
    return bad


def check_integrity(cc):
    counts = collections.Counter(r['mnemonic'] for r in cc)
    duplicate = [m for m, n in counts.items() if n > 1]
    unsupported = [r['mnemonic'] for r in cc
                   if not any(r[c] for c in r if c not in ('mnemonic', 'description',
                                                           'notes'))]
    print('csv integrity: %d instructions, %d duplicate mnemonics, %d with no support'
          % (len(cc), len(duplicate), len(unsupported)))
    return [(m, '', 'duplicate') for m in duplicate] + \
           [(m, '', 'no processor marked') for m in unsupported]


def main():
    cc = rows()
    bad = check_per_processor(cc, per_processor_tables())
    bad += check_headers(cc, description_headers())
    bad += check_integrity(cc)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
