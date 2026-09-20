#!/usr/bin/env python3
"""Split MC68020UM.pdf into one PDF per section, keeping and extending its outline.

Unlike the other manuals in this repository this one arrives with an outline
already - 227 bookmarks, one per paragraph heading - and with a real text
layer rather than a scan. So nothing here has to be reconstructed from
running headers. Two things are still done:

  * the outline is carried into the parts and remapped to the new page
    numbering, with each entry verified against the page it claims by
    finding its paragraph number at the head of a line there;
  * the figure and table captions are added, so each part can be navigated
    to a particular diagram. The manual's own outline stops at paragraph
    headings. The titles come from the front-matter lists and the pages from
    the body, because each is better at one of the two jobs: the lists carry
    the whole title and extract cleanly, where the body renders theta as "q"
    and wraps a long title onto a second line that cannot be told from a
    table's own heading row; and the lists give a printed folio where the
    body gives the page itself.

The printed folio of every page is read back from its own running footer.
That is what turns up the two places where this digitisation is not what it
says it is: Section 11's eleven pages carry the footer of a different manual
entirely, and the acronym list is bound out of order. See README.md.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'MC68020UM.pdf')

TITLE = "MC68020/MC68EC020 Microprocessors User's Manual"

# ---------------------------------------------------------------- parts -----
# (slug, first PDF page, last PDF page, bookmark root title). The boundaries
# are the manual's own top-level bookmarks; pages 1-2 come before the first
# of them and make up the front matter.
PARTS = [
    ('00-front-matter',                        1,   2, 'Front Matter'),
    ('01-table-of-contents',                   3,   9, 'Table of Contents'),
    ('02-list-of-illustrations',              10,  13, 'List of Illustrations'),
    ('03-list-of-tables',                     14,  15, 'List of Tables'),
    ('04-acronym-list',                       16,  16, 'MC68020/EC020 Acronym List'),
    ('05-section-01-introduction',            17,  29, 'Sec. 1 - Introduction'),
    ('06-section-02-processing-states',       30,  35, 'Sec. 2 - Processing States'),
    ('07-section-03-signal-description',      36,  43, 'Sec. 3 - Signal Description'),
    ('08-section-04-on-chip-cache-memory',    44,  47, 'Sec. 4 - On-Chip Cache Memory'),
    ('09-section-05-bus-operation',           48, 125, 'Sec. 5 - Bus Operation'),
    ('10-section-06-exception-processing',   126, 153, 'Sec. 6 - Exception Processing'),
    ('11-section-07-coprocessor-interface',  154, 214,
     'Sec. 7 - Coprocessor Interface Description'),
    ('12-section-08-instruction-execution-timing', 215, 254,
     'Sec. 8 - Instruction Execution Timing'),
    ('13-section-09-applications-information', 255, 274,
     'Sec. 9 - Applications Information'),
    ('14-section-10-electrical-characteristics', 275, 288,
     'Sec. 10 - Electrical Characteristics'),
    ('15-section-11-ordering-information-and-mechanical-data', 289, 299,
     'Sec. 11 - Ordering Information and Mechanical Data'),
    ('16-appendix-a-mc68ec020-three-wire-bus-arbitration', 300, 300,
     'Appx. A - Interfacing an MC68EC020 to a DMA Device That Supports a '
     'Three-Wire Bus Arbitration Protocol'),
    ('17-index',                             301, 306, 'Index'),
]

# The section each printed folio belongs to, for the pages whose footer the
# extraction cannot place. Section 11 is printed with another manual's
# running footer, so its folios say 13-1 to 13-11 and name no section of
# this manual at all; page 1 is the cover and carries no footer.
FOLIO_OVERRIDE = {**{p: '11' for p in range(289, 300)}, 1: ''}

CAPTION = re.compile(r'^(\s+)(Figure|Table)\s+([0-9A-Z]{1,2}-[0-9]{1,2})\.\s*(.*?)\s*$')
LIST_NUM = re.compile(r'^\s*([0-9A-Z]{1,2}-[0-9]{1,2})\s+(\S.*?)\s*$')
LIST_END = re.compile(r'^(.*?)\s*\.{3,}\s*[0-9A-Z]+-[0-9]+\s*$')
LIST_SKIP = ('Figure', 'Table', 'Paragraph', 'Number', 'Title', 'Page',
             'For More', 'Go to', 'Freescale')

# The front-matter lists are set in a font the extraction reads correctly;
# the body pages are not, and render the same characters as whatever the
# MacRoman or Symbol code point happens to be in Latin-1. Comparing a body
# line with a list title means putting the list title back into the body's
# spelling first. Whitespace goes too: the overbar font leaves a gap before
# the comma in "DSACK1/DSACK0 , BERR" and none in "tAVDV".
AS_BODY_SPELLS_IT = str.maketrans({
    '—': 'Ñ', '–': 'Ð', '’': 'Õ', '“': 'Ò', '”': 'Ó',
    'θ': 'q', 'µ': 'm', '≤': '£', '≥': '³', '±': '±', '°': 'û',
})


def fold(text):
    return re.sub(r'\s+', '', text).translate(AS_BODY_SPELLS_IT)
HEADING = re.compile(r'^\s*([0-9]{1,2}(?:\.[0-9]{1,2}){0,3})\s')
FOOTER = re.compile(r"USER.S MANUAL")


def pages_of(path):
    out = subprocess.run(['pdftotext', '-layout', path, '-'],
                         capture_output=True, text=True, check=True).stdout
    chunks = out.split('\f')
    while chunks and not chunks[-1].strip():
        chunks.pop()
    return chunks


def read_folios(pages):
    """The printed folio of every page, off its own running footer.

    The footer is MOTOROLA <manual> <folio> on a recto and <folio> <manual>
    MOTOROLA on a verso, so the folio is whichever end is not MOTOROLA.
    """
    out = {}
    for i, page in enumerate(pages, 1):
        for line in page.split('\n'):
            if FOOTER.search(line):
                parts = line.split()
                if parts and parts[0] == 'MOTOROLA':
                    out[i] = parts[-1]
                elif parts:
                    out[i] = parts[0]
                break
    return out


def read_outline():
    """The manual's own 227 bookmarks, as (title, level, page)."""
    dump = subprocess.run(['pdftk', SRC, 'dump_data_utf8'],
                          capture_output=True, text=True, check=True).stdout
    out, title, level = [], None, None
    for line in dump.split('\n'):
        if line.startswith('BookmarkTitle: '):
            title = line[15:]
        elif line.startswith('BookmarkLevel: '):
            level = int(line[15:])
        elif line.startswith('BookmarkPageNumber: '):
            out.append((title, level, int(line[20:])))
    return out


def verify(title, page_text):
    """Does this heading's paragraph number start a line on the page?

    Top-level entries name a section rather than a paragraph and are taken
    on trust; everything else has to be found.
    """
    m = re.match(r'^([0-9]{1,2}(?:\.[0-9]{1,2}){1,3})\s', title)
    if not m:
        return True
    want = m.group(1)
    for line in page_text.split('\n'):
        h = HEADING.match(line)
        if h and h.group(1) == want:
            return True
    return False


def parse_list(pages, first, last):
    """One of the front-matter lists, as number -> title.

    An entry is a number, a title and a dotted leader ending in the printed
    folio. A title too long for the line wraps, so lines are accumulated
    until the leader turns up.
    """
    out, cur = {}, None
    for page in pages[first - 1:last]:
        for line in page.split('\n'):
            if FOOTER.search(line):
                continue
            m = LIST_NUM.match(line)
            if m:
                cur = m.group(1)
                out[cur] = m.group(2)
            elif cur and line.strip() and not line.strip().startswith(LIST_SKIP):
                out[cur] += ' ' + line.strip()
            if cur:
                m = LIST_END.match(out[cur])
                if m:
                    out[cur] = m.group(1)
                    cur = None
    return out


def parse_captions(pages, lists):
    """Where in the body each figure and table caption is printed.

    The line has to carry the right number and the beginning of the right
    title. Both halves are needed: prose cites figures by number too, and a
    sentence ending "... as shown in Figure 7-7." puts that number at the
    head of a line with the next sentence running on after it. Requiring the
    rest of the line to open the title as the list gives it rejects that and
    accepts the caption, which may be truncated by wrapping but never
    starts with something else.
    """
    out, seen, missing = [], set(), []
    for i, page in enumerate(pages, 1):
        for n, line in enumerate(page.split('\n')):
            m = CAPTION.match(line)
            if not m or len(m.group(1)) < 8:
                continue
            kind, num, text = m.group(2), m.group(3), m.group(4)
            if (kind, num) in seen:
                continue
            title = lists[kind].get(num)
            if title is None or not fold(title).startswith(fold(text)[:24]):
                continue
            seen.add((kind, num))
            out.append((kind, num, i, n, title))
    for kind in ('Figure', 'Table'):
        for num in lists[kind]:
            if (kind, num) not in seen:
                missing.append((kind, num))
    return out, missing


def main():
    pages = pages_of(SRC)
    assert len(pages) == 306, len(pages)
    folios = read_folios(pages)

    outline = read_outline()
    placed, rejected = [], []
    for title, level, page in outline:
        if verify(title, pages[page - 1]):
            placed.append((title, level, page))
        else:
            rejected.append((title, page))
    print('outline: %d bookmarks, %d verified against the page they claim, '
          '%d unverified' % (len(outline), len(placed), len(rejected)))
    for title, page in rejected:
        print('   unverified: %-58s PDF page %d' % (title[:58], page))

    lists = {'Figure': parse_list(pages, 10, 13),
             'Table': parse_list(pages, 14, 15)}
    caps, missing = parse_captions(pages, lists)
    print('captions: %d listed in the front matter (%d figures, %d tables), '
          '%d located in the body, %d not found'
          % (len(lists['Figure']) + len(lists['Table']), len(lists['Figure']),
             len(lists['Table']), len(caps), len(missing)))
    for kind, num in missing:
        print('   not found: %s %s' % (kind, num))

    strange = sorted(p for p, f in folios.items()
                     if p not in FOLIO_OVERRIDE and '-' in f
                     and not re.fullmatch(r'(?:[0-9]{1,2}|A|INDEX)-[0-9]{1,2}', f))
    if strange:
        print('   odd folios: %s' % strange)

    total, nmarks = 0, 0
    for slug, first, last, root in PARTS:
        dest = os.path.join(HERE, slug + '.pdf')
        subprocess.run(['pdftk', SRC, 'cat', '%d-%d' % (first, last),
                        'output', dest], check=True)

        marks = [(root, 1, 1, (-2, -1))]
        for title, level, page in placed:
            # Every level-1 entry of the source outline names one of these
            # parts, and becomes that part's root rather than an entry in it.
            if first <= page <= last and level > 1:
                marks.append((title, level, page - first + 1, (-1, 0)))
        for kind, num, page, line, title in caps:
            if first <= page <= last:
                marks.append(('%s %s. %s' % (kind, num, title), 9,
                              page - first + 1, (line, 1)))

        # Captions hang off the heading above them rather than off each
        # other, so a run of figures does not staircase away to the right.
        marks.sort(key=lambda m: (m[2], m[3]))
        heading, fixed = 1, []
        for t, lv, pg, _ in marks:
            if lv == 9:
                lv = heading + 1
            else:
                lv = min(lv, heading + 1)
                heading = lv
            fixed.append((t, lv, pg))

        data = ['InfoBegin', 'InfoKey: Title',
                'InfoValue: %s - %s' % (TITLE, root)]
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
                                         capture_output=True,
                                         text=True).stdout).group(1))
        assert n == last - first + 1, (slug, n)
        total += n
        nmarks += len(fixed)
        print('%-58s pp %3d-%3d  %3d pages  %3d bookmarks'
              % (slug + '.pdf', first, last, n, len(fixed)))
    print('total %d pages (source has 306), %d bookmarks (source has %d)'
          % (total, nmarks, len(outline)))


if __name__ == '__main__':
    if not os.path.exists(SRC):
        sys.exit('%s not found - see the root README for how to identify it' % SRC)
    main()
