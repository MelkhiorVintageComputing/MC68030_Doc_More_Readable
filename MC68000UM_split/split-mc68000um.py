#!/usr/bin/env python3
"""Split MC68000UM.pdf into one PDF per section, with a reconstructed outline.

The source has no outline at all - not even a top-level one - so every
bookmark here is rebuilt from the document itself:

  * paragraph headings come from the table of contents (pages 8-12).  The
    printed folio of every body page was read back from the page's own
    running footer, so "10-8" -> PDF page 159 is measured, not assumed;
    each entry is then verified by finding its paragraph number at the head
    of a line on the page it claims.
  * figure and table captions come from the *body* pages, not from the two
    front-matter lists.  The lists disagree with the body in several places
    (see README.md, "Where the source contradicts itself"), and the body is
    what a reader actually turns to, so the body wins.
"""
import os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'MC68000UM.pdf')
OUT = HERE

# ---------------------------------------------------------------- parts -----
# (slug, first PDF page, last PDF page, bookmark root title)
PARTS = [
    ('00-front-matter',                       1,   7, 'Front Matter'),
    ('01-table-of-contents',                  8,  12, 'Table of Contents'),
    ('02-list-of-illustrations',             13,  15, 'List of Illustrations'),
    ('03-list-of-tables',                    16,  17, 'List of Tables'),
    ('04-section-01-overview',                18,  21, 'Sec. 1 - Overview'),
    ('05-section-02-introduction',            22,  35, 'Sec. 2 - Introduction'),
    ('06-section-03-signal-description',      36,  45, 'Sec. 3 - Signal Description'),
    ('07-section-04-8-bit-bus-operation',     46,  53, 'Sec. 4 - 8-Bit Bus Operation'),
    ('08-section-05-16-bit-bus-operation',    54,  93, 'Sec. 5 - 16-Bit Bus Operation'),
    ('09-section-06-exception-processing',    94, 113, 'Sec. 6 - Exception Processing'),
    ('10-section-07-8-bit-instruction-execution-times',   114, 125,
     'Sec. 7 - 8-Bit Instruction Execution Times'),
    ('11-section-08-16-bit-instruction-execution-times',  126, 137,
     'Sec. 8 - 16-Bit Instruction Execution Times'),
    ('12-section-09-mc68010-instruction-execution-times', 138, 151,
     'Sec. 9 - MC68010 Instruction Execution Times'),
    ('13-section-10-electrical-and-thermal-characteristics', 152, 181,
     'Sec. 10 - Electrical and Thermal Characteristics'),
    ('14-section-11-ordering-information-and-mechanical-data', 182, 197,
     'Sec. 11 - Ordering Information and Mechanical Data'),
    ('15-appendix-a-mc68010-loop-mode-operation', 198, 201,
     'Appendix A - MC68010 Loop Mode Operation'),
    ('16-appendix-b-m6800-peripheral-interface', 202, 207,
     'Appendix B - M6800 Peripheral Interface'),
    ('17-index',                             208, 213, 'Index'),
    ('18-back-matter',                       214, 216, 'Back Matter'),
]

# Section -> PDF page carrying its page 1.  Read off the running footers of
# all 196 numbered body pages: every folio in the book is N-1 .. N-last with
# no gaps and no repeats, so these offsets are measured, not inferred.
SEC_START = {'1': 18, '2': 22, '3': 36, '4': 46, '5': 54, '6': 94, '7': 114,
             '8': 126, '9': 138, '10': 152, '11': 182, 'A': 198, 'B': 202}

# The two captions the scan lost entirely.  Both pages carry a full-page
# drawing and an empty text layer; both were confirmed by eye from a 110 dpi
# rendering, and both are bracketed by the captions on the facing pages.
CAPTION_EXEMPT = [
    ('Figure', '5-21', 73, '3-Wire Bus Arbitration Timing Diagram—Special Case'),
    ('Figure', '11-1', 183, '64-Pin Dual In Line'),
]

# ------------------------------------------------------------ TOC parsing ---
TAIL = re.compile(r'([0-9AB]{1,2})\s*[-–—]\s*([0-9IlO]{1,3})\s*[\'".,]?$')
NUM = re.compile(r'^[0-9AB][0-9A-Za-z.,:\-]*$')
DIGIT = str.maketrans({'I': '1', 'l': '1', 'O': '0', 'o': '0'})


def parse_toc(text):
    """Yield [paragraph number, title, printed section, printed page].

    The section is taken from the entry's own folio ("8-1" -> section 8)
    rather than from the "Section N" heading above it: the scan reads the
    heading over section 8 as "Section B".
    """
    out, pending = [], None
    for line in text.split('\n'):
        s = re.sub(r'\s+', ' ', line).strip()
        if not s:
            continue
        if re.match(r'^(Section|Appendix)\b', s, re.I):
            pending = None
            continue
        if re.match(r'^(TABLE OF CONTENTS|Paragraph|Number|Title|Page$|M68000|'
                    r'MOTOROLA|[ivx]+$)', s):
            continue
        # "7 .1", "11 .2": the scan splits the paragraph number at the dot
        s = re.sub(r'(?<=\d) +(?=\.\d)', '', s)

        body, page = s, None
        m = TAIL.search(s)
        if m:
            page = (m.group(1).lstrip('0') or m.group(1),
                    int(m.group(2).translate(DIGIT)))
            body = s[:m.start()]
        body = body.strip(' .')

        parts = body.split(' ', 1)
        if len(parts) == 2 and NUM.match(parts[0]) and re.search(r'\d', parts[0]):
            num = parts[0].replace(',', '.').replace(':', '.').rstrip('.')
            title = re.sub(r'\s+', ' ', parts[1].replace('.', ' ')).strip()
            # "8.1 O Multiprecision ...": a trailing zero read as a letter O
            m2 = re.match(r'^[Oo]\s+(\S.*)$', title)
            if m2:
                num, title = num + '0', m2.group(1)
            if page:
                out.append([num, title, page[0], page[1]])
                pending = None
            else:
                pending = [num, title]              # title wrapped to next line
        elif pending is not None:
            extra = re.sub(r'\s+', ' ', body.replace('.', ' ')).strip()
            if extra:
                pending[1] = (pending[1] + ' ' + extra).strip()
            if page:
                out.append(pending + [page[0], page[1]])
                pending = None
    return out


# Part numbers the scan renders with capital O for zero.  Listing them is
# clearer than a rule: every one of these is a documented Motorola part.
PARTS_OCR = {
    'MC68HCOOO': 'MC68HC000', 'MC68ECOOO': 'MC68EC000', 'MC6801O': 'MC68010',
    'MC6801 O': 'MC68010', '68HCOOO': '68HC000', '68ECOOO': '68EC000',
    '6801 O': '68010',
}

TITLE_FIX = {
    # The signal is BERR.  The scan reads its double R as A in the contents
    # and as AR in the body ("BEAR"); the list of tables gets it right.
    'The Relationship of DTACK, BERA, and HALT':
        'The Relationship of DTACK, BERR, and HALT',
}


def tidy(title):
    for bad, good in PARTS_OCR.items():
        title = title.replace(bad, good)
    title = title.replace('Spec ifications', 'Specifications')
    # the headings print an em dash: "AC ELECTRICAL SPECIFICATIONS-CLOCK TIMING"
    title = re.sub(r'\s*-\s*(?=(Clock|Read|MC68000|Bus)\b)', '—', title)
    title = re.sub(r'\s+([,;:])', r'\1', title)
    title = re.sub(r'\s+', ' ', title).strip(' .,;:')
    return TITLE_FIX.get(title, title)


# Headings the automatic check cannot match, confirmed by reading the page.
OCR_EXEMPT = {
    '3.10': 'printed on the page as "a:10 POWER SUPPLY (Vcc and GND)"',
}


def verify(num, page_text):
    """Is `num` the paragraph number of a heading on this page?

    The scan splits paragraph numbers at the dot ("2 .1 .1", "6.3. 7") and
    reads a trailing zero as a letter O ("6.3.1 O"), so the leading run of
    number-ish characters is squeezed and letter-mapped before comparing.
    """
    want = re.sub(r'[^0-9]', '', num)
    for line in page_text.split('\n'):
        t = line.strip()
        t = re.sub(r'^(\d{1,2})\s{2,}', '', t)   # stray marginal section digit
        # a trailing O/l/I is only a digit when a letter does not follow it,
        # so that "6.3.6 Illegal" does not read as 6.3.6111
        m = re.match(r'^[0-9][0-9.,:;\- ]*[OolI]?(?![A-Za-z])', t)
        if not m:
            continue
        got = re.sub(r'[^0-9]', '', m.group(0).translate(DIGIT))
        if got == want or (got.startswith(want) and len(got) - len(want) <= 1):
            return True
    return False


def locate(num, claimed, pages, section):
    """The PDF page the heading is really on, or None.

    A handful of table-of-contents page numbers are simply wrong in the
    source; when the claimed page does not carry the heading, look a couple
    of pages either side before giving up.
    """
    if num in OCR_EXEMPT:
        return claimed
    lo, hi = SEC_START[section], claimed + 2
    for pg in [claimed] + [claimed + d for d in (1, -1, 2, -2)]:
        if lo <= pg <= min(hi, len(pages)) and verify(num, pages[pg - 1]):
            return pg
    return None


# -------------------------------------------------------- caption parsing ---
CAP = re.compile(r'^(\s*)(Figure|Table)\s*([0-9AB]{1,2})\s*[-·.•‐]\s*'
                 r'([0-9IlO]{1,3})\s*[-·.•,]?\s+([A-Z0-9(].*)$')

CAPTION_FIX = {
    'External VMATiming': 'External VMA Timing',
    'Case 8408-01-FU Suffix': 'Case 840B-01-FU Suffix',
    'BEAR and HALT Negation Results': 'BERR and HALT Negation Results',
    'DTACK,BERR, and HALT Assertion Results': 'DTACK, BERR, and HALT Assertion Results',
    # Both power-dissipation tables carry a theta subscript the scan cannot
    # render; 10-1 is the junction-to-ambient case and 10-2 the
    # junction-to-case one, read off a 300 dpi rendering of page 10-4.
    'Power Dissipation and Junction Temperature vs Temperature (0JC=0JA)':
        'Power Dissipation and Junction Temperature vs Temperature (ΘJA)',
    'Power Dissipation and Junction Temperature vs Temperature (OJc.. eJc)':
        'Power Dissipation and Junction Temperature vs Temperature (ΘJC)',
}


def centre(line):
    s = line.rstrip()
    return (len(s) - len(s.lstrip()) + len(s)) / 2.0


def tidy_caption(t):
    for bad, good in PARTS_OCR.items():
        t = t.replace(bad, good)
    t = t.replace('{', '(')                       # a brace read for a paren
    if t.count('(') == t.count('}') + t.count(')') and '}' in t:
        t = t.replace('}', ')')
    t = t.replace('(Po)', '(PD)')                 # P with a subscript D
    # "Timing Diagram-Special Case", "Timing- Idle Bus Case": an em dash
    t = re.sub(r'\s*-\s*(?=(Processor|Bus|Special|Idle|Multiple|Active|Best|Worst)\b)',
               '—', t)
    t = re.sub(r'\s+', ' ', t).strip(' .,;:·')
    return CAPTION_FIX.get(t, t)


def parse_captions(pages, folio_section):
    """Find every figure and table caption on the body pages.

    A caption is a centred line; body prose that happens to open with
    "Figure 5-19." is not.  Three filters separate them, and each one is
    needed: an indent (prose starts at the left margin), an upper-case first
    word (prose continues "... shows the timing for ..."), and agreement
    between the caption's own section number and the section the page is in
    (a stub-head reading "Table 4-4" inside Table 5-6 is not a caption).
    """
    out = []
    for pdfpage, text in enumerate(pages, 1):
        sec = folio_section.get(pdfpage)
        if sec is None:
            continue
        lines = [l.rstrip() for l in text.split('\n')]
        for i, line in enumerate(lines):
            m = CAP.match(line)
            if not m or len(m.group(1)) < 3:
                continue
            if m.group(3).upper() != sec:
                continue
            body = m.group(5).strip()
            # a two-line caption: the second line is centred under the first
            if i + 1 < len(lines) and lines[i + 1].strip():
                nxt = lines[i + 1].strip()
                if abs(centre(lines[i + 1]) - centre(line)) <= 3 and len(nxt) <= 45:
                    body += ' ' + nxt
            out.append((m.group(2), '%s-%s' % (m.group(3).upper(),
                                               m.group(4).translate(DIGIT)),
                        pdfpage, i, tidy_caption(body)))
    return out


def read_folios(pages):
    """PDF page -> section, from each body page's own running footer."""
    out = {}
    for i, text in enumerate(pages, 1):
        for line in reversed([l.strip() for l in text.split('\n') if l.strip()][-3:]):
            if 'MANUAL' not in line.upper():
                continue
            tok = line.split()
            folio = None
            if tok[0].upper().startswith('MOTOROLA'):
                folio = tok[-1]
            elif tok[-1].upper().startswith('MOTOROLA'):
                folio = tok[0]
            if folio:
                m = re.match(r'^([0-9]{1,2}|[AB8])[-–—]', folio)
                if m:
                    # the scan reads B-3 and B-5 as 8-3 and 8-5; sections 8
                    # and B are 76 pages apart, so the page number settles it
                    s = m.group(1)
                    if s == '8' and i >= SEC_START['B']:
                        s = 'B'
                    out[i] = s
                break
    return out


def main():
    pages = subprocess.run(['pdftotext', '-layout', SRC, '-'],
                           capture_output=True, text=True).stdout.split('\f')
    while pages and not pages[-1].strip():
        pages.pop()
    assert len(pages) == 216, len(pages)

    folio_section = read_folios(pages)
    # page 1-1 loses its footer to the scan; its neighbours make it certain
    folio_section.setdefault(SEC_START['1'], '1')

    # ---- paragraph headings ------------------------------------------------
    toc = parse_toc(subprocess.run(['pdftotext', '-layout', '-f', '8', '-l', '12',
                                    SRC, '-'], capture_output=True, text=True).stdout)
    entries, rejected, moved = [], [], []
    for num, title, psec, ppage in toc:
        if psec not in SEC_START:
            rejected.append((num, title, 'unknown section %s' % psec))
            continue
        claimed = SEC_START[psec] + ppage - 1
        pdfpage = locate(num, claimed, pages, psec)
        if pdfpage is None:
            rejected.append((num, title, 'not found on PDF page %d' % claimed))
            continue
        if pdfpage != claimed:
            moved.append((num, title, '%s-%d claimed, found on %s-%d'
                          % (psec, ppage, psec, ppage + pdfpage - claimed)))
        entries.append((num, tidy(title), pdfpage))
    print('table of contents: %d entries, %d placed, %d relocated, %d rejected'
          % (len(toc), len(entries), len(moved), len(rejected)))
    for r in moved:
        print('   relocated: %-9s %-52s %s' % r)
    for r in rejected:
        print('   rejected:  %-9s %-52s %s' % r)
    for num, why in sorted(OCR_EXEMPT.items()):
        print('   exempt:    %-9s %s' % (num, why))

    # ---- figure and table captions -----------------------------------------
    caps = parse_captions(pages, folio_section)
    for kind, num, pg, title in CAPTION_EXEMPT:
        caps.append((kind, num, pg, 0, title))
    print('captions: %d found in the body (%d figures, %d tables), '
          '%d supplied by hand' % (len(caps),
                                   len({c[1] for c in caps if c[0] == 'Figure'}),
                                   len({c[1] for c in caps if c[0] == 'Table'}),
                                   len(CAPTION_EXEMPT)))

    os.makedirs(OUT, exist_ok=True)
    total, nmarks = 0, 0
    for slug, first, last, root in PARTS:
        dest = os.path.join(OUT, slug + '.pdf')
        subprocess.run(['pdftk', SRC, 'cat', '%d-%d' % (first, last),
                        'output', dest], check=True)

        # (title, level, page, sort key).  Paragraph headings sort by their
        # number, captions by the line they sit on, so a figure that shares a
        # page with the heading above it lands after that heading.
        marks = [(root, 1, 1, (-1, -1))]
        for num, title, pg in entries:
            if first <= pg <= last:
                marks.append(('%s %s' % (num, title), 1 + num.count('.'),
                              pg - first + 1,
                              (-1, 0) + tuple(int(x) if x.isdigit() else 0
                                              for x in num.split('.'))))
        for kind, num, pg, line, title in caps:
            if first <= pg <= last:
                marks.append(('%s %s. %s' % (kind, num, title), 9,
                              pg - first + 1, (line, 1)))

        # Captions hang off the heading they follow rather than off each
        # other, so a run of figures does not staircase away to the right.
        marks.sort(key=lambda m: (m[2], m[3]))
        heading, fixed = 1, []
        for t, lv, pg, _ in marks:
            if lv == 9:
                lv = heading + 1
            else:
                lv = min(lv, heading + 1)        # never skip an outline level
                heading = lv
            fixed.append((t, lv, pg))

        data = ['InfoBegin', 'InfoKey: Title',
                'InfoValue: M68000 8-/16-/32-Bit Microprocessors User\'s Manual - %s'
                % root]
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
        nmarks += len(fixed)
        print('%-58s pp %3d-%3d  %3d pages  %3d bookmarks'
              % (slug + '.pdf', first, last, n, len(fixed)))
    print('total %d pages (source has 216), %d bookmarks' % (total, nmarks))


if __name__ == '__main__':
    if not os.path.exists(SRC):
        sys.exit('%s not found - see the root README for how to identify it' % SRC)
    main()
