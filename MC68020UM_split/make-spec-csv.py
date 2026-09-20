#!/usr/bin/env python3
"""Write the Section 10 electrical specification CSVs.

This manual has a real text layer, so unlike the scanned data sheets
elsewhere in this repository nothing here is transcribed by hand: the tables
are parsed out of the document itself.

What the text layer does not do is decode. The Type 1 fonts are MacRoman
encoded and the extraction hands back the raw code points, so an em dash
arrives as 0xD1 and a bullet as 0xA5; and every Greek letter and relation
comes from the Symbol font, where "q" is theta and "m" is mu. That last one
is not cosmetic - it is the difference between the 400 microamps of the
output high voltage test condition and the 3.2 milliamps of the output low
voltage one, which the layout-preserving extraction renders identically as
"mA". So the text is rebuilt here from mutool's character stream, which
carries the font and the size of every glyph, rather than taken from
pdftotext.

The same character stream settles the footnote markers. They are set solid
against the specification number - "31A3" is specification 31A carrying
footnote 3, and "9B11" is 9B carrying footnote 11, not 9B carrying 1 twice -
and the only thing that distinguishes them is that a marker is set two
points smaller.

check-spec-csv.py re-reads the same pages through poppler instead, and
compares.
"""
import collections
import csv
import os
import re
import statistics
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'MC68020UM.pdf')

# Where each table is printed, as PDF pages of MC68020UM.pdf.
P_MAXIMUM = 275
P_MC68020_DC = (276, 277)
P_THERMAL_TABLES = 277
P_MC68EC020_DC = (278, 279)
P_AC_CLOCK = 281
P_AC_READ_WRITE = (282, 284)

# The printed folio of a PDF page: Section 10 runs 10-1 to 10-14 on 275-288.
def folio(page):
    return '10-%d' % (page - 274)


# The Type 1 fonts are MacRoman encoded and the extraction reports the raw
# code point. Only the characters that actually occur in Section 10 are
# listed; anything else raises, so a new one cannot slip through unnoticed.
MACROMAN = {
    0xA5: '•',   # bullet, used in the thermal equations as a multiply
    0xD0: '–',   # en dash, used throughout as a minus sign
    0xD1: '—',   # em dash, the tables' "not specified"
    0xD2: '“', 0xD3: '”',
    0xD5: '’',
    0xFB: '°',   # ring above, used as a degree sign
    0xFFFD: ' ',      # an undecodable glyph at the end of a drawn text line
}

# The Symbol font carries every Greek letter and relation in the section.
SYMBOL = {
    0x61: 'α', 0x64: 'δ', 0x6D: 'µ', 0x71: 'θ',
    0xA3: '≤', 0xB0: '°', 0xB1: '±', 0xB3: '≥',
    0xB4: '×', 0xB8: '÷',
    0xBB: '≈',   # "approximately equal", printed after DSACK - see README
}

CHAR = re.compile(r'<char quad="([\d.-]+) ([\d.-]+) [\d.-]+ [\d.-]+ '
                  r'[\d.-]+ [\d.-]+ ([\d.-]+) ([\d.-]+)"[^>]*c="([^"]*)"')
FONT = re.compile(r'<font name="([^"]+)" size="([\d.]+)"')
# Every page carries a "Freescale Semiconductor, Inc." watermark set on its
# side, and the reprint's own footer. Neither is part of the manual.
LINE = re.compile(r'<line [^>]*dir="([\d.-]+) ([\d.-]+)"')
FURNITURE = ('Freescale Semiconductor', 'For More Information',
             'Go to: www.freescale.com')
ENTITY = {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&apos;': "'"}

AC_COLS = ['table', 'pdf_page', 'printed_page', 'num', 'footnotes',
           'characteristic', 'condition', 'f16_67_min', 'f16_67_max',
           'f20_min', 'f20_max', 'f25_min', 'f25_max', 'f33_33_min',
           'f33_33_max', 'unit', 'note']
NOTE_COLS = ['table', 'marker', 'applies_to', 'text']
DC_COLS = ['table', 'pdf_page', 'printed_page', 'applies_to', 'characteristic',
           'condition', 'symbol', 'min', 'max', 'unit', 'note']
THERMAL_COLS = ['table', 'pdf_page', 'printed_page', 'applies_to', 'row',
                'column', 'value', 'unit', 'note']


def decode(raw, font):
    """One character of the stream, as the manual prints it."""
    if raw in ENTITY:
        raw = ENTITY[raw]
    if raw.startswith('&#x'):
        code = int(raw[3:-1], 16)
    elif len(raw) == 1:
        code = ord(raw)
    else:
        raise ValueError(raw)
    if font.startswith('Symbol'):
        if code == 0x20:
            return ' '
        if code in SYMBOL:
            return SYMBOL[code]
        raise ValueError('unmapped Symbol character %#x' % code)
    if code < 128:
        return chr(code)
    if code in MACROMAN:
        return MACROMAN[code]
    if code in (0x2013, 0x2014, 0x2019):
        return chr(code)
    raise ValueError('unmapped character %#x in %s' % (code, font))


def text_of(tokens):
    """The line as text, with subscripts set solid against what they modify."""
    out = ''
    for x0, x1, text, kind in tokens:
        if out and not (kind == 'sub' and not out.endswith(' ')):
            out += ' '
        out += text
    return out.strip()


def lines_of(page):
    """One page as lines of tokens, each (x0, x1, text, kind).

    Characters are gathered into lines by their baseline and then into
    tokens by the gap between them. kind is "sup" for a token set smaller
    and higher than the line, "sub" for one set smaller and level or lower,
    and empty otherwise. The distinction is what separates the footnote
    marker of "31A3" from the subscript of "VCC": both are set two points
    smaller, and only the baseline tells them apart.
    """
    xml = subprocess.run(['mutool', 'draw', '-F', 'stext', '-o', '-', SRC,
                          str(page)], capture_output=True, text=True,
                         check=True).stdout
    chars, font, size, upright = [], '', 0.0, True
    for line in xml.split('\n'):
        m = LINE.search(line)
        if m:
            upright = abs(float(m.group(1)) - 1.0) < 0.01 \
                and abs(float(m.group(2))) < 0.01
        m = FONT.search(line)
        if m:
            font, size = m.group(1), float(m.group(2))
        m = CHAR.search(line)
        if m and upright:
            x0, y0, x1, y1 = (float(m.group(i)) for i in (1, 2, 3, 4))
            text = decode(m.group(5), font)
            if text.strip():
                chars.append((y1, x0, x1, text, size))

    chars.sort(key=lambda c: (round(c[0], 1), c[1]))
    rows = []
    for c in chars:
        # 3 pt, because a footnote marker is set 2.3 pt above the number it
        # belongs to and has to join that line; table rows are 16 pt apart.
        if rows and abs(c[0] - rows[-1][0][0]) <= 3.0:
            rows[-1].append(c)
        else:
            rows.append([c])

    out = []
    for row in rows:
        row.sort(key=lambda c: c[1])
        # against the median, not the maximum: the asterisk that marks a
        # specification as MC68020-only is set larger than the text it sits
        # in front of, and would otherwise make the whole line look small.
        big = statistics.median(c[4] for c in row)
        base = statistics.median(c[0] for c in row if c[4] >= big - 0.5)
        tokens, cur = [], None
        for y1, x0, x1, text, size in row:
            kind = ''
            if size < big - 0.5:
                kind = 'sup' if y1 < base - 1.0 else 'sub'
            if cur and x0 - cur[1] < 1.6 and cur[3] == kind:
                cur = (cur[0], x1, cur[2] + text, kind)
            else:
                if cur:
                    tokens.append(cur)
                cur = (x0, x1, text, kind)
        if cur:
            tokens.append(cur)
        # A subscript is part of the word it follows - "V" and "IH" are one
        # symbol - so it is folded in. A superscript is a footnote marker
        # and stays a token of its own.
        folded = []
        for t in tokens:
            if t[3] == 'sub' and folded and t[0] - folded[-1][1] < 3.0:
                folded[-1] = (folded[-1][0], t[1], folded[-1][2] + t[2],
                              folded[-1][3])
            else:
                folded.append(t)
        tokens = folded
        if not any(f in text_of(tokens) for f in FURNITURE):
            out.append(tokens)
    return out


def columns_from(tokens, labels):
    """The x centre of each named column heading on a header line."""
    out = {}
    for x0, x1, text, _ in tokens:
        if text in labels:
            out.setdefault(text, []).append((x0 + x1) / 2)
    return out


# ------------------------------------------------- AC electrical tables ----
GRADES = ['f16_67', 'f20', 'f25', 'f33_33']
# A specification number, optionally asterisked as MC68020-only. The clock
# table numbers two specifications together where one line of the diagram
# carries both, as "2,3" for the two clock pulse widths.
NUM = re.compile(r'^\*?[0-9]{1,2}[AB]?(?:,[0-9]{1,2}[AB]?)*$')


def value_columns(header):
    """The eight Min/Max centres and the Unit centre, from a header line."""
    cols = [(x0 + x1) / 2 for x0, x1, t, _ in header if t in ('Min', 'Max')]
    unit = [(x0 + x1) / 2 for x0, x1, t, _ in header if t == 'Unit']
    assert len(cols) == 8 and len(unit) == 1, (cols, unit)
    return sorted(cols), unit[0]


def parse_ac(table, first, last):
    """One AC table, as one row per specification.

    A row opens on a line whose first token is a specification number, and
    runs on through any line that carries no number: the manual breaks a
    long characteristic across two lines, and puts a characteristic set in
    the overbar font on a line of its own because that font sits a little
    higher than the text around it. A continuation line that does carry
    values is a second set of limits for the same specification under a
    different condition, which is how #45 gives one figure for a read and
    another for a write.
    """
    rows = []
    for page in range(first, last + 1):
        lines = lines_of(page)
        header = next((l for l in lines
                       if [t[2] for t in l][:2] == ['Num.', 'Characteristics']
                       or [t[2] for t in l][:2] == ['Num.', 'Characteristic']), None)
        if header is None:
            continue
        cols, unit_x = value_columns(header)
        edge = cols[0] - 16
        body = lines[lines.index(header) + 1:]
        # The left edge of the characteristic column, taken from the rows
        # themselves. A line that starts there is a new specification even
        # when it carries no number; a line that starts further in is a
        # condition qualifying the specification above it.
        starts = [min((t[0] for t in l if t[0] < edge), default=999)
                  for l in body]
        char_left = min((x for x in starts if 95 < x < edge), default=0) + 2
        # Where a specification is given twice under two conditions the
        # manual sets the condition in a sub-column of its own. The second
        # condition sits on a line by itself, which gives that sub-column's
        # position; the first shares the line with the number.
        cond_x = [min(t[0] for t in l if t[0] < edge) for l in body
                  if any(t[0] >= edge for t in l)
                  and not NUM.match(l[0][2])
                  and min((t[0] for t in l if t[0] < edge), default=0) > char_left + 60]
        for line in body:
            text = text_of(line)
            if 'USER' in text and 'MANUAL' in text:
                break
            if text.startswith(('*', 'NOTES', 'MOTOROLA')) and not NUM.match(line[0][2]):
                break
            left = [t for t in line if t[0] < edge]
            right = [t for t in line if t[0] >= edge]
            if not left and not right:
                continue
            num, marks = '', []
            while left and (NUM.match(left[0][2]) or left[0][3] == 'sup'):
                if left[0][3] == 'sup':
                    marks += left[0][2].split(',')
                else:
                    num = left[0][2]
                left.pop(0)
            cond = ''
            if cond_x and left:
                at = [i for i, t in enumerate(left)
                      if any(abs(t[0] - c) < 2 for c in cond_x)]
                if at:
                    cond = ' '.join(t[2] for t in left[at[0]:])
                    left = left[:at[0]]
            words = ' '.join(t[2] for t in left)

            values = ['' for _ in range(8)]
            unit = ''
            for x0, x1, t, _ in right:
                mid = (x0 + x1) / 2
                if abs(mid - unit_x) < 14:
                    unit = t
                    continue
                j = min(range(8), key=lambda k: abs(cols[k] - mid))
                if abs(cols[j] - mid) < 16:
                    values[j] = t
            if num:
                rows.append({'table': table, 'pdf_page': page,
                             'printed_page': folio(page), 'num': num,
                             'footnotes': ','.join(marks), 'characteristic': words,
                             'condition': cond, 'unit': unit, 'note': '',
                             **{'%s_%s' % (g, k): values[i * 2 + j]
                                for i, g in enumerate(GRADES)
                                for j, k in enumerate(('min', 'max'))}})
            elif any(values) and left and left[0][0] <= char_left:
                rows.append({'table': table, 'pdf_page': page,
                             'printed_page': folio(page), 'num': '',
                             'footnotes': '', 'characteristic': words,
                             'condition': '', 'unit': unit, 'note': '',
                             **{'%s_%s' % (g, k): values[i * 2 + j]
                                for i, g in enumerate(GRADES)
                                for j, k in enumerate(('min', 'max'))}})
            elif rows and any(values):
                prev = rows[-1]
                rows.append({**prev, 'condition': words or cond,
                             'unit': unit or prev['unit'],
                             **{'%s_%s' % (g, k): values[i * 2 + j]
                                for i, g in enumerate(GRADES)
                                for j, k in enumerate(('min', 'max'))}})
            elif rows and words:
                rows[-1]['characteristic'] = (rows[-1]['characteristic']
                                              + ' ' + words).strip()
    return rows


# ------------------------------------------------- DC electrical tables ----
def parse_dc(table, applies_to, page, heading):
    """One DC table, as one row per pair of limits.

    The manual gives several characteristics more than one limit, one per
    group of signals, and sets the groups down the middle of the row; each
    of those becomes a row here, carrying the characteristic, symbol and
    unit of the block it belongs to. A cell too wide for its column is
    broken across two lines - the minimum input low voltage is "GND" over
    "-0.5", meaning GND minus half a volt - so a line carrying a limit and
    nothing else continues the line above rather than starting a row.
    """
    lines = lines_of(page)
    start = next(i for i, l in enumerate(lines) if heading in text_of(l))
    header = next(l for l in lines[start:]
                  if [t[2] for t in l][:2] == ['Characteristics', 'Symbol'])
    cond = text_of(lines[start + 1])
    cols = {t[2]: (t[0] + t[1]) / 2 for t in header
            if t[2] in ('Symbol', 'Min', 'Max', 'Unit')}
    left_edge = min(t[0] for t in header)

    rows = []
    characteristic, symbol, unit = '', '', ''
    pending = []
    for line in lines[lines.index(header) + 1:]:
        text = text_of(line)
        if 'USER' in text and 'MANUAL' in text:
            break
        if text.startswith('NOTE'):
            break
        cell = {k: '' for k in cols}
        words = []
        for x0, x1, t, kind in line:
            mid = (x0 + x1) / 2
            near = min(cols, key=lambda k: abs(cols[k] - mid))
            if abs(cols[near] - mid) < 15 and x0 > cols['Symbol'] - 22:
                cell[near] = (cell[near] + t) if kind == 'sub' else \
                    (cell[near] + ' ' + t).strip()
            else:
                words.append((x0, x1, t, kind))
        head = text_of(words)
        # A characteristic and the group of signals it applies to share a
        # line, set in two columns with a wide gap between them. There is no
        # ruled heading for the second, so the gap is what finds it.
        split = ''
        for i in range(1, len(words)):
            if words[i][0] - words[i - 1][1] > 24:
                split = text_of(words[i:])
                head = text_of(words[:i])
                break
        if cell['Symbol']:
            if words and words[0][0] <= left_edge + 2:
                characteristic, head, split = head, split, ''
                pending = []
            symbol, unit = cell['Symbol'], cell['Unit'] or unit
        elif words and words[0][0] <= left_edge + 2 and not any(cell.values()):
            characteristic, pending = head, [split] if split else []
            continue
        if not (cell['Min'] or cell['Max']):
            # a group of signals, or a test condition, printed above the
            # limits it applies to
            pending += [w for w in (head, split) if w]
            continue
        if not head and rows and not cell['Symbol']:
            for k in ('Min', 'Max'):
                if cell[k]:
                    rows[-1][k.lower()] = (rows[-1][k.lower()] + ' '
                                           + cell[k]).strip()
            continue
        rows.append({'table': table, 'pdf_page': page,
                     'printed_page': folio(page), 'applies_to': applies_to,
                     'characteristic': characteristic,
                     'condition': ' '.join(pending + [w for w in (head, split) if w]),
                     'symbol': symbol, 'min': cell['Min'], 'max': cell['Max'],
                     'unit': cell['Unit'] or unit, 'note': cond})
        pending = []
    return rows


# --------------------------------------- maximum ratings and thermal data ----
def parse_maximum(page=P_MAXIMUM):
    """Table 10.1, Maximum Ratings.

    A block of prose about static protection is set beside the table rather
    than under it, so everything to the right of the Unit column is dropped.
    A rating whose value depends on the package is given a heading and then
    one line per package, and the heading is carried onto those lines.
    """
    lines = lines_of(page)
    header = next(l for l in lines if [t[2] for t in l][:4]
                  == ['Rating', 'Symbol', 'Value', 'Unit'])
    cols = {t[2]: (t[0] + t[1]) / 2 for t in header[:4]}
    edge = cols['Symbol'] - 30
    margin = cols['Unit'] + 30
    body = lines[lines.index(header) + 1:]
    body_left = min((min(t[0] for t in l) for l in body[:8]), default=0)
    rows, heading = [], ''
    for line in body:
        line = [t for t in line if t[0] < margin]
        text = text_of(line)
        if not text:
            continue
        if ('USER' in text and 'MANUAL' in text) or text.startswith('10.2') \
                or (line and line[0][0] < body_left - 2):
            break
        words = [t for t in line if t[0] < edge]
        cell = {k: '' for k in cols}
        for x0, x1, t, kind in line:
            if x0 < edge:
                continue
            near = min(('Symbol', 'Value', 'Unit'),
                       key=lambda k: abs(cols[k] - (x0 + x1) / 2))
            cell[near] = (cell[near] + t) if kind == 'sub' \
                else (cell[near] + ' ' + t).strip()
        name = text_of(words)
        if not cell['Symbol']:
            heading = name
            continue
        rows.append({'table': 'maximum-ratings', 'pdf_page': page,
                     'printed_page': folio(page), 'applies_to': 'MC68020/EC020',
                     'characteristic': (heading + ' ' + name).strip()
                     if words and words[0][0] > body_left + 8 else name,
                     'condition': '', 'symbol': cell['Symbol'],
                     'min': '', 'max': cell['Value'], 'unit': cell['Unit'],
                     'note': 'a maximum rating, not an operating condition'})
        if words and words[0][0] <= body_left + 8:
            heading = ''
    return rows


def parse_thermal_resistance(page, applies_to):
    """The junction-to-ambient and junction-to-case resistance of each package.

    Page 10-4 carries this table for the MC68EC020 and the DC table for the
    MC68020, and both open with a heading that starts "Characteristic", so
    the search starts from the paragraph title rather than the top of the
    page.
    """
    lines = lines_of(page)
    start = next(i for i, l in enumerate(lines)
                 if text_of(l) == '%s Thermal Resistance (°C/W)' % applies_to)
    header = next(l for l in lines[start:]
                  if text_of(l).startswith('Characteristic'))
    cols = [(t[0] + t[1]) / 2 for t in header if t[2] in ('θJA', 'θJC')]
    assert len(cols) == 2, text_of(header)
    rows = []
    for line in lines[lines.index(header) + 1:]:
        values = [t for t in line if t[0] > cols[0] - 24]
        if len(values) != 2:
            if values:
                break
            continue
        name = text_of([t for t in line if t[0] <= cols[0] - 24])
        for col, value in zip(('θJA', 'θJC'), values):
            rows.append({'table': 'thermal-resistance', 'pdf_page': page,
                         'printed_page': folio(page), 'applies_to': applies_to,
                         'row': name, 'column': col, 'value': value[2],
                         'unit': '°C/W', 'note': ''})
    return rows


def parse_matrix(page, table, applies_to, caption, first_word, split_x):
    """One of Tables 10-1 to 10-4: a grid of values under a row of headings.

    Each of the four is shaped differently, so the line that carries the
    column headings is named by its first word and the boundary between the
    row labels and the values is given outright; below that the shape is the
    same in all four. Column headings of several words - "PD Maximum
    (Watts)" - are gathered by the gap between them.
    """
    lines = lines_of(page)
    start = next(i for i, l in enumerate(lines) if caption in text_of(l))
    header = next(l for l in lines[start + 1:] if l and l[0][2] == first_word)
    labels, cols = [], []
    for t in [t for t in header if t[0] > split_x]:
        if labels and t[0] - cols[-1][1] < 24:
            labels[-1] += ' ' + t[2]
            cols[-1] = (cols[-1][0], t[1])
        else:
            labels.append(t[2])
            cols.append((t[0], t[1]))
    centres = [(a + b) / 2 for a, b in cols]

    rows, group = [], ''
    for line in lines[lines.index(header) + 1:]:
        values = [t for t in line if t[0] > split_x]
        name = text_of([t for t in line if t[0] <= split_x])
        text = text_of(line)
        if ('USER' in text and 'MANUAL' in text) or text.startswith(
                ('*', 'Table', 'Values', 'NOTE')):
            break
        if not values:
            if not name:
                continue
            group = name
            continue
        for value in values:
            mid = (value[0] + value[1]) / 2
            j = min(range(len(centres)), key=lambda k: abs(centres[k] - mid))
            rows.append({'table': table, 'pdf_page': page,
                         'printed_page': folio(page), 'applies_to': applies_to,
                         'row': (group + ', ' + name).strip(', ') or group,
                         'column': labels[j], 'value': value[2],
                         'unit': '', 'note': ''})
    return rows


# ----------------------------------------------------------- table notes ----
# A starred note may hang off a speed-grade column rather than off rows.
# Which of the two it is is not written down anywhere in the table, so it is
# recorded here: both tables star the 25 MHz column, and the read and write
# table also stars the specifications the MC68EC020 does not have.
COLUMN_NOTES = {('clock', '*'): 'f25', ('read-write', '**'): 'f25'}

STAR = re.compile(r'^(\*{1,2})(?!\s)(.*)$')
NUMBERED = re.compile(r'^([0-9]{1,2})\.\s+(.*)$')


def parse_notes(table, first, last):
    """The notes printed under a table.

    Two kinds. A starred note hangs off a whole column or off the rows
    carrying that many stars, and is printed as a paragraph; a numbered note
    hangs off the rows that reference it, and the numbered ones are gathered
    under a NOTES: heading. Both wrap, and a wrapped line is recognised by
    being indented past the marker it continues.
    """
    out = []
    for page in range(first, last + 1):
        collecting, indent = None, 0
        for line in lines_of(page):
            text = text_of(line)
            if not text or ('USER' in text and 'MANUAL' in text):
                continue
            if text == 'NOTES:':
                continue
            m = STAR.match(text) or NUMBERED.match(text)
            if m and line[0][0] < 120 and m.group(2).strip()[:1].isalpha():
                marker, body = m.group(1), m.group(2).strip()
                out.append({'table': table, 'marker': marker,
                            'applies_to': COLUMN_NOTES.get((table, marker), ''),
                            'text': body})
                collecting, indent = out[-1], line[0][0]
                continue
            if collecting is not None and line[0][0] > indent - 1 \
                    and not text[0].isupper() or (
                    collecting is not None and line[0][0] > indent + 2):
                collecting['text'] += ' ' + text
            else:
                collecting = None
    return out


# ------------------------------------------------------------- assembly ----
def write(name, cols, rows):
    with open(os.path.join(HERE, name), 'w', newline='') as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        w.writerows(rows)
    values = sum(1 for r in rows for c in cols
                 if c.startswith(('f16', 'f20', 'f25', 'f33')) and r[c])
    print('%-38s %3d rows%s' % (name + ':', len(rows),
                                ', %d limits' % values if values else ''))


def main():
    ac = parse_ac('clock', P_AC_CLOCK, P_AC_CLOCK) \
        + parse_ac('read-write', *P_AC_READ_WRITE)
    # The asterisk in front of a specification number is a footnote marker,
    # not part of the number: it means the MC68EC020 has no such signal.
    for row in ac:
        if row['num'].startswith('*'):
            row['num'] = row['num'][1:]
            row['footnotes'] = ','.join(['*'] + [f for f in
                                                 row['footnotes'].split(',') if f])
    assert len(ac) == 65, len(ac)

    notes = parse_notes('clock', P_AC_CLOCK, P_AC_CLOCK) \
        + parse_notes('read-write', 283, 284)
    assert len(notes) == 14, len(notes)

    dc = parse_maximum() \
        + parse_dc('dc', 'MC68020', 278, 'MC68020 DC Electrical Characteristics') \
        + parse_dc('dc', 'MC68EC020', 279,
                   'MC68EC020 DC Electrical Characteristics')

    thermal = parse_thermal_resistance(276, 'MC68020') \
        + parse_thermal_resistance(278, 'MC68EC020') \
        + parse_matrix(277, 'table-10-1', 'MC68020', 'Table 10-1.', 'θJA', 280) \
        + parse_matrix(277, 'table-10-2', 'MC68020/EC020', 'Table 10-2.',
                       'Rated', 260) \
        + parse_matrix(277, 'table-10-3', 'MC68020', 'Table 10-3.',
                       'Natural', 280) \
        + parse_matrix(278, 'table-10-4', 'MC68EC020', 'Table 10-4.', 'θJA', 200)

    write('ac-electrical-specifications.csv', AC_COLS, ac)
    write('ac-table-notes.csv', NOTE_COLS, notes)
    write('dc-electrical-specifications.csv', DC_COLS, dc)
    write('thermal-characteristics.csv', THERMAL_COLS, thermal)


if __name__ == '__main__':
    main()
