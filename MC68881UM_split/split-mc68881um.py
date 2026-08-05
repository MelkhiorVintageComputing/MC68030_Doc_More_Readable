#!/usr/bin/env python3
"""Split MC68881UM.pdf into one PDF per section, with a reconstructed outline.

The source has 23 top-level bookmarks and nothing below them, so every
sub-bookmark here is rebuilt:

  * paragraph headings come from the table of contents (pages 5-12).  The
    printed folio of every body page was read back from the page itself, so
    "12-3" -> PDF page 379 is measured, not assumed; each entry is then
    verified by finding its paragraph number at the head of a line on the
    page it claims.
  * the 49 instruction descriptions in Section 4 come from the running
    headers on pages 76-182.
"""
import os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'MC68881UM.pdf')
OUT = HERE

# ---------------------------------------------------------------- parts -----
# (slug, first PDF page, last PDF page, bookmark root title)
PARTS = [
    ('00-front-matter',                    1,   4,   'Front Matter'),
    ('01-table-of-contents',               5,  12,   'Table of Contents'),
    ('02-list-of-illustrations',          13,  16,   'List of Illustrations'),
    ('03-list-of-tables',                 17,  18,   'List of Tables'),
    ('04-preface',                        19,  20,   'Preface'),
    ('05-section-01-general-description',  21,  36,  'Sec. 1 - General Description'),
    ('06-section-02-programming-model',    37,  44,  'Sec. 2 - Programming Model'),
    ('07-section-03-operand-data-formats', 45,  58,  'Sec. 3 - Operand Data Formats'),
    ('08-section-04-instruction-set',      59, 208,  'Sec. 4 - Instruction Set'),
    ('09-section-05-coprocessor-programming', 209, 224, 'Sec. 5 - Coprocessor Programming'),
    ('10-section-06-exception-processing', 225, 264, 'Sec. 6 - Exception Processing'),
    ('11-section-07-coprocessor-interface', 265, 306, 'Sec. 7 - Coprocessor Interface'),
    ('12-section-08-instruction-execution-timing', 307, 346, 'Sec. 8 - Instruction Execution Timing'),
    ('13-section-09-functional-signal-descriptions', 347, 354, 'Sec. 9 - Functional Signal Descriptions'),
    ('14-section-10-bus-operation',       355, 370, 'Sec. 10 - Bus Operation'),
    ('15-section-11-interfacing-methods', 371, 376, 'Sec. 11 - Interfacing Methods'),
    ('16-section-12-electrical-specifications', 377, 382, 'Sec. 12 - Electrical Specifications'),
    ('17-section-13-ordering-information', 383, 386, 'Sec. 13 - Ordering Information and Mechanical Data'),
    ('18-appendix-a-glossary',            387, 390, 'Appendix A - Glossary'),
    ('19-appendix-b-abbreviations-and-acronyms', 391, 394, 'Appendix B - Abbreviations and Acronyms'),
    ('20-index',                          395, 404, 'Index'),
    ('21-timing-diagram-foldouts',        405, 406, 'Timing Diagram Foldouts'),
    ('22-back-matter',                    407, 409, 'Back Matter'),
]

# section number -> PDF page of its page 1 (each section restarts at N-1)
SEC_START = {'1': 21, '2': 37, '3': 45, '4': 59, '5': 209, '6': 225, '7': 265,
             '8': 307, '9': 347, '10': 355, '11': 371, '12': 377, '13': 383,
             'A': 387, 'B': 391}

# The three foldout diagrams sit side by side on one physical sheet.
FOLDOUT_MARKS = [('Figure 12-2. Asynchronous Read Cycle Timing Diagram', 1),
                 ('Figure 12-3. Asynchronous Write Cycle Timing Diagram', 1),
                 ('Figure 12-4. Synchronous Read Cycle Timing Diagram', 1)]

# --------------------------------------------------------- instructions -----
# first page (PDF) -> (mnemonic, title as printed in the running header)
INSTRUCTIONS = [
    (76,  'FABS',     'Absolute Value'),
    (78,  'FACOS',    'Arc Cosine'),
    (80,  'FADD',     'Add'),
    (82,  'FASIN',    'Arc Sine'),
    (84,  'FATAN',    'Arc Tangent'),
    (86,  'FATANH',   'Hyperbolic Arc Tangent'),
    (88,  'FBcc',     'Branch Conditionally'),
    (90,  'FCMP',     'Compare'),
    (92,  'FCOS',     'Cosine'),
    (94,  'FCOSH',    'Hyperbolic Cosine'),
    (96,  'FDBcc',    'Test Condition, Decrement, and Branch'),
    (98,  'FDIV',     'Divide'),
    (100, 'FETOX',    'e^x'),
    (102, 'FETOXM1',  'e^x - 1'),
    (104, 'FGETEXP',  'Get Exponent'),
    (106, 'FGETMAN',  'Get Mantissa'),
    (108, 'FINT',     'Integer Part'),
    (110, 'FINTRZ',   'Integer Part, Round-to-Zero'),
    (112, 'FLOG10',   'Log10'),
    (114, 'FLOG2',    'Log2'),
    (116, 'FLOGN',    'Loge'),
    (118, 'FLOGNP1',  'Loge(x+1)'),
    (120, 'FMOD',     'Modulo Remainder'),
    (122, 'FMOVE',    'Move Floating-Point Data Register'),
    (128, 'FMOVE',    'Move System Control Register'),
    (130, 'FMOVECR',  'Move Constant ROM'),
    (132, 'FMOVEM',   'Move Multiple Data Registers'),
    (136, 'FMOVEM',   'Move Multiple Control Registers'),
    (138, 'FMUL',     'Multiply'),
    (140, 'FNEG',     'Negate'),
    (142, 'FNOP',     'No Operation'),
    (144, 'FREM',     'IEEE Remainder'),
    (146, 'FRESTORE', 'Restore Internal State'),
    (148, 'FSAVE',    'Save Internal State'),
    (151, 'FSCALE',   'Scale Exponent'),
    (154, 'FScc',     'Set According to Condition'),
    (156, 'FSGLDIV',  'Single Precision Divide'),
    (158, 'FSGLMUL',  'Single Precision Multiply'),
    (160, 'FSIN',     'Sine'),
    (162, 'FSINCOS',  'Simultaneous Sine and Cosine'),
    (165, 'FSINH',    'Hyperbolic Sine'),
    (167, 'FSQRT',    'Square Root'),
    (169, 'FSUB',     'Subtract'),
    (171, 'FTAN',     'Tangent'),
    (173, 'FTANH',    'Hyperbolic Tangent'),
    (175, 'FTENTOX',  '10^x'),
    (177, 'FTRAPcc',  'Trap Conditionally'),
    (179, 'FTST',     'Test Operand'),
    (181, 'FTWOTOX',  '2^x'),
]

# TOC entries whose paragraph number the OCR mangled beyond automatic repair,
# and one heading the OCR dropped from the body page altogether.
NUM_FIX = {'7.514.3': '7.5.4.3'}
# Headings the automatic check cannot match, each confirmed by reading the page.
# The scan repeatedly turns the first '.' of a heading number into a '1'.
OCR_EXEMPT = {
    '4.7.1.3': 'heading dropped by the scan; page confirmed by its neighbours '
               '4.7.1.2 and 4.7.1.4, which are on the same page',
    '4.5.5.2': 'printed on the page as "415.5.2 UNDERFLOW, ROUND, OVERFLOW."',
    '6.2.5':   'printed on the page as "612.5 Interrupt"',
}

TAIL = re.compile(r'([0-9AB]{1,2})\s*[-–—]\s*([0-9IlO]{1,3})$')
NUM = re.compile(r'^[0-9AB][0-9A-Za-z.,:\-]*$')
DIGIT = str.maketrans({'I': '1', 'l': '1', 'O': '0'})


def norm_num(t):
    t = t.replace(',', '.').replace(':', '.').replace('-', '.').rstrip('.')
    return NUM_FIX.get(t, t)


def parse_toc(text):
    """Yield [section, paragraph number, title, printed section, printed page]."""
    cur, out, pending = None, [], None
    for line in text.split('\n'):
        s = re.sub(r'\s+', ' ', line).strip()
        if not s:
            continue
        m = re.match(r'^Section (\d+)$', s) or re.match(r'^Appendix ([AB])$', s, re.I)
        if m:
            cur, pending = m.group(1).upper(), None
            continue
        if re.match(r'^(TABLE OF CONTENTS|Paragraph|Number|Title|MC68881|FREESCALE|Page$|[ivxIVX]+$)', s):
            continue

        body, page = s, None
        m = TAIL.search(s)
        if not m and cur:
            # "12.4 DC Electrical Characteristics . . . .12-2 . . . ." - the leader
            # dots run past the folio, so it is not at the end of the line
            m = re.search(r'(?<![0-9])(%s)[-–—]([0-9IlO]{1,3})(?![0-9])' % re.escape(cur), s)
        if m:
            page = (m.group(1), int(m.group(2).translate(DIGIT)))
            body = s[:m.start()]
        body = body.strip(' .')

        parts = body.split(' ', 1)
        if len(parts) == 2 and NUM.match(parts[0]) and re.search(r'\d', parts[0]):
            num = norm_num(parts[0])
            title = re.sub(r'\s+', ' ', parts[1].replace('.', ' ')).strip()
            if page:
                out.append([cur, num, title, page[0], page[1]])
                pending = None
            else:
                pending = [cur, num, title]          # title wrapped to next line
        elif pending is not None:
            extra = re.sub(r'\s+', ' ', body.replace('.', ' ')).strip()
            if extra:
                pending[2] = (pending[2] + ' ' + extra).strip()
            if page:
                out.append(pending + [page[0], page[1]])
                pending = None
    return out


def despace(m):
    """C h a r a c t e r i s t i c s -> Characteristics.

    The scan loses the wider inter-word gap along with the inter-letter one, so
    a run may swallow a word boundary ("ThermalCharacteristics").  Restoring it
    at each lower-to-upper transition recovers the original in every title here.
    """
    run = m.group(0).replace(' ', '')
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', run)


# Glue the OCR left behind that no rule can undo.
TITLE_FIX = {
    'Recoveryfrom Exceptions': 'Recovery from Exceptions',
    'Thermal Characteristics - PGA Package': 'Thermal Characteristics — PGA Package',
}


def tidy(title):
    title = re.sub(r'(?:[A-Za-z] ){3,}[A-Za-z]\b', despace, title)
    # "- -", "= -" and "--" are all the scan's rendering of an em dash
    title = re.sub(r'(?<= )[-=]\s*[-=](?= )', '—', title)
    # a lowercase l or an exclamation mark standing in for a capital I
    title = re.sub(r'\bCl(?=R\b)', 'CI', title)
    title = re.sub(r'(?<=-)lnstruction', 'Instruction', title)
    title = re.sub(r'^!(?=[a-z])', 'I', title)
    # an acronym run swallowed the space before the next word: IEEEAware.
    # The trailing {3,} keeps mnemonics such as FDBcc and FTRAPcc intact.
    title = re.sub(r'(?<=[A-Z]{3})(?=[A-Z][a-z]{3,})', ' ', title)
    # the scan spaces out hyphens: "Coprocessor - Detected"
    title = re.sub(r'(?<=[a-z]) - (?=[A-Z][a-z])', '-', title)
    title = re.sub(r'(?<=[a-z]) / (?=[A-Z])', '/', title)
    # a closing parenthesis read as a brace
    if title.count('(') == 1 and '}' in title and ')' not in title:
        title = title.replace('}', ')')
    title = re.sub(r'\s+([,;:])', r'\1', title)
    title = re.sub(r'^[•·]+\s*|[•·"\']+\s*$', '', title)
    title = re.sub(r'\s+', ' ', title).strip(' .,;:')
    return TITLE_FIX.get(title, title)


def verify(num, page_text):
    """Is `num` the paragraph number of a heading on this page?"""
    want = re.sub(r'[^0-9]', '', num)
    for line in page_text.split('\n'):
        t = line.strip()
        # a stray marginal section digit is often OCR'd in front of the heading
        t = re.sub(r'^(\d{1,2})\s{2,}', '', t)
        m = re.match(r'^([0-9][0-9.,:;\-]*)', t)
        if not m:
            continue
        got = re.sub(r'[^0-9]', '', m.group(1))
        # "6.1.30perand Error" - the number ran into the title
        if got == want or (got.startswith(want) and len(got) - len(want) <= 1):
            return True
    return False


def main():
    pages = subprocess.run(['pdftotext', '-layout', SRC, '-'],
                           capture_output=True, text=True).stdout.split('\f')
    toc = parse_toc(subprocess.run(['pdftotext', '-layout', '-f', '5', '-l', '12', SRC, '-'],
                                   capture_output=True, text=True).stdout)

    # ---- resolve every TOC entry to a PDF page and check it lands there ----
    entries, unverified = [], []
    for sec, num, title, psec, ppage in toc:
        if psec not in SEC_START:
            unverified.append((num, title, 'unknown section %s' % psec))
            continue
        pdfpage = SEC_START[psec] + ppage - 1
        if not verify(num, pages[pdfpage - 1]) and num not in OCR_EXEMPT:
            unverified.append((num, title, 'not found on PDF page %d' % pdfpage))
            continue
        entries.append((num, tidy(title), pdfpage))
    print('table of contents: %d entries, %d placed, %d rejected'
          % (len(toc), len(entries), len(unverified)))
    for u in unverified:
        print('   rejected: %-10s %-50s %s' % u)

    os.makedirs(OUT, exist_ok=True)
    total = 0
    for slug, first, last, root in PARTS:
        dest = os.path.join(OUT, slug + '.pdf')
        subprocess.run(['pdftk', SRC, 'cat', '%d-%d' % (first, last),
                        'output', dest], check=True)

        # (title, level, page, sort key).  Several headings share a page, so the
        # key has to be the paragraph number - ordering by depth would put
        # "1.4 Instruction Set" ahead of "1.3.4 Data Format Summary".
        marks = [(root, 1, 1, ())]
        if slug == '21-timing-diagram-foldouts':
            marks += [(t, 2, p, (i,)) for i, (t, p) in enumerate(FOLDOUT_MARKS)]
        for num, title, pg in entries:
            if first <= pg <= last:
                key = tuple(int(x) for x in num.split('.'))
                marks.append(('%s %s' % (num, title), 1 + num.count('.'),
                              pg - first + 1, key))
        if slug == '08-section-04-instruction-set':
            for i, (pg, mn, ti) in enumerate(INSTRUCTIONS):
                # nested under 4.6 Individual Instruction Descriptions
                marks.append(('%s - %s' % (mn, ti), 3, pg - first + 1, (4, 6, i)))

        # document order, and never skip an outline level
        marks.sort(key=lambda m: (m[2], m[3]))
        marks = [(t, lv, pg) for t, lv, pg, _ in marks]
        prev = 0
        fixed = []
        for t, lv, pg in marks:
            lv = min(lv, prev + 1)
            prev = lv
            fixed.append((t, lv, pg))

        data = ['InfoBegin', 'InfoKey: Title',
                'InfoValue: MC68881/MC68882 User\'s Manual - %s' % root]
        for t, lv, pg in fixed:
            data += ['BookmarkBegin', 'BookmarkTitle: %s' % t,
                     'BookmarkLevel: %d' % lv, 'BookmarkPageNumber: %d' % pg]
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
            fh.write('\n'.join(data) + '\n')
            info = fh.name
        try:
            subprocess.run(['pdftk', dest, 'update_info_utf8', info,
                            'output', dest + '.tmp'], check=True)
        finally:
            os.unlink(info)
        os.replace(dest + '.tmp', dest)

        n = int(re.search(r'NumberOfPages: (\d+)',
                          subprocess.run(['pdftk', dest, 'dump_data'],
                                         capture_output=True, text=True).stdout).group(1))
        assert n == last - first + 1, (slug, n)
        total += n
        print('%-46s pp %3d-%3d  %3d pages  %3d bookmarks'
              % (slug + '.pdf', first, last, n, len(fixed)))
    print('total %d pages (source has 409)' % total)


if __name__ == '__main__':
    if not os.path.exists(SRC):
        sys.exit('%s not found - see the root README for how to identify it' % SRC)
    main()
