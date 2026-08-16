#!/usr/bin/env python3
"""Write the Section 10 electrical specifications out as CSV.

Every number below was read off a 300 dpi rendering of the page, not off the
PDF's text layer.  The text layer of this scan is good enough to *check* a
transcription - check-spec-csv.py does exactly that - but not to make one:
it drops columns, turns em dashes into nothing, and merges cells.

Nothing here is corrected.  Where the source is wrong (and it is, in nine
places) the printed value is what lands in the CSV and the `note` column
says what is wrong with it; README.md collects them all.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# The six speed grades of the MC68000/MC68008/MC68010 tables.  The fourth is
# headed "16.67 MHz 12F" - the 12F is a separately binned part, which is why
# it can be faster than the plain 16 MHz column on some specifications.
# The MC68EC000 tables have five grades and no 12F; their 16.67 MHz column
# lands in f16_67 and their f16 columns stay empty.
GRADES6 = ['f8', 'f10', 'f12_5', 'f16_67', 'f16', 'f20']
GRADES5 = ['f8', 'f10', 'f12_5', 'f16_67', 'f20']
GRADES2 = ['f8', 'f10']

AC_COLS = (['table', 'pdf_page', 'printed_page', 'num', 'footnotes',
            'characteristic', 'condition', 'unit'] +
           ['%s_%s' % (g, s) for g in GRADES6 for s in ('min', 'max')] +
           ['note'])

# ---------------------------------------------------------------------------
# 10.8  AC ELECTRICAL SPECIFICATIONS - CLOCK TIMING          (printed 10-8)
CLOCK_COND = ('VCC = 5.0 VDC +/- 5%; GND = 0 VDC; TA = TL to TH; '
              'applies to all processors except the MC68EC000')
CLOCK = [
    ('',     '',  'Frequency of Operation', 'MHz',
     ('4.0', '8.0'), ('4.0', '10.0'), ('4.0', '12.5'),
     ('8.0', '16.7'), ('8.0', '16.7'), ('8.0', '20.0'), ''),
    ('1',    '',  'Cycle Time', 'ns',
     ('125', '250'), ('100', '250'), ('80', '250'),
     ('60', '125'), ('60', '125'), ('50', '125'), ''),
    ('2, 3', '',  'Clock Pulse Width (Measured from 1.5 V to 1.5 V for 12F)', 'ns',
     ('55', '125'), ('45', '125'), ('35', '125'),
     ('27', '62.5'), ('27', '62.5'), ('21', '62.5'),
     'printed as two identical lines, one for specification 2 and one for 3'),
    ('4, 5', '',  'Clock Rise and Fall Times', 'ns',
     ('', '10'), ('', '10'), ('', '5'), ('', '5'), ('', '5'), ('', '4'),
     'printed as two identical lines, one for specification 4 and one for 5'),
]

# 10.9  MC68008 AC ELECTRICAL SPECIFICATIONS - CLOCK TIMING  (printed 10-9)
CLOCK08_COND = 'VCC = 5.0 VDC +/- 5%; GND = 0 VDC; TA = TL to TH; MC68008 only'
CLOCK08 = [
    ('',     '', 'Frequency of Operation', 'MHz', ('2.0', '8.0'), ('2.0', '10.0'), ''),
    ('1',    '', 'Cycle Time', 'ns', ('125', '500'), ('100', '500'), ''),
    ('2, 3', '', 'Clock Pulse Width', 'ns', ('55', '250'), ('45', '250'), ''),
    ('4, 5', '', 'Clock Rise and Fall Times', 'ns', ('', '10'), ('', '10'), ''),
]

# 10.10  AC ELECTRICAL SPECIFICATIONS - READ AND WRITE CYCLES
# (printed 10-10 .. 10-12; the header prints "+/- 5+" for "+/- 5%")
RW_COND = ('VCC = 5.0 VDC +/- 5%; GND = 0 V; TA = TL to TH; '
           'applies to all processors except the MC68EC000')
RW = [
    (161, '10-10', '6',   '',      'Clock Low to Address Valid', 'ns',
     ('', '62'), ('', '50'), ('', '50'), ('', '50'), ('', '30'), ('', '25'),
     'the 16 MHz minimum cell is blank rather than dashed'),
    (161, '10-10', '6A',  '',      'Clock High to FC Valid', 'ns',
     ('', '62'), ('', '50'), ('', '45'), ('', '45'), ('0', '30'), ('0', '25'), ''),
    (161, '10-10', '7',   '',      'Clock High to Address, Data Bus High Impedance (Maximum)', 'ns',
     ('', '80'), ('', '70'), ('', '60'), ('', '50'), ('', '50'), ('', '42'),
     'the 16 MHz minimum cell is blank rather than dashed'),
    (161, '10-10', '8',   '',      'Clock High to Address, FC Invalid (Minimum)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (161, '10-10', '9',   '1',     'Clock High to AS, DS Asserted', 'ns',
     ('3', '60'), ('3', '50'), ('3', '40'), ('3', '40'), ('3', '30'), ('3', '25'), ''),
    (161, '10-10', '11',  '2',     'Address Valid to AS, DS Asserted (Read)/AS Asserted (Write)', 'ns',
     ('30', ''), ('20', ''), ('15', ''), ('15', ''), ('15', ''), ('10', ''), ''),
    (161, '10-10', '11A', '2',     'FC Valid to AS, DS Asserted (Read)/AS Asserted (Write)', 'ns',
     ('90', ''), ('70', ''), ('60', ''), ('30', ''), ('45', ''), ('40', ''),
     'printed with two stray closing parentheses: "FC Valid to AS), DS Asserted (Read)/AS) Asserted (Write)"'),
    (161, '10-10', '12',  '1',     'Clock Low to AS, DS Negated', 'ns',
     ('', '62'), ('', '50'), ('', '40'), ('', '40'), ('3', '30'), ('3', '25'), ''),
    (161, '10-10', '13',  '2',     'AS, DS Negated to Address, FC Invalid', 'ns',
     ('40', ''), ('30', ''), ('20', ''), ('10', ''), ('15', ''), ('10', ''), ''),
    (161, '10-10', '14',  '2',     'AS (and DS Read) Width Asserted', 'ns',
     ('270', ''), ('195', ''), ('160', ''), ('120', ''), ('120', ''), ('100', ''),
     'printed "ASand DS Read) Width Asserted"; 10.14 prints the same specification as "AS (and DS Read) Width Asserted"'),
    (161, '10-10', '14A', '',      'DS Width Asserted (Write)', 'ns',
     ('140', ''), ('95', ''), ('80', ''), ('60', ''), ('60', ''), ('50', ''),
     'the first four maximum cells are blank rather than dashed'),
    (161, '10-10', '15',  '2',     'AS, DS Width Negated', 'ns',
     ('150', ''), ('105', ''), ('65', ''), ('60', ''), ('60', ''), ('50', ''), ''),
    (161, '10-10', '16',  '',      'Clock High to Control Bus High Impedance', 'ns',
     ('', '80'), ('', '70'), ('', '60'), ('', '50'), ('', '50'), ('', '42'), ''),
    (161, '10-10', '17',  '2',     'AS, DS Negated to R/W Invalid', 'ns',
     ('40', ''), ('30', ''), ('20', ''), ('10', ''), ('15', ''), ('10', ''), ''),
    (161, '10-10', '18',  '1',     'Clock High to R/W High (Read)', 'ns',
     ('0', '55'), ('0', '45'), ('0', '40'), ('0', '40'), ('0', '30'), ('0', '25'), ''),
    (161, '10-10', '20',  '1',     'Clock High to R/W Low (Write)', 'ns',
     ('0', '55'), ('0', '45'), ('0', '40'), ('0', '40'), ('0', '30'), ('0', '25'), ''),
    (161, '10-10', '20A', '2, 6',  'AS Asserted to R/W Valid (Write)', 'ns',
     ('', '10'), ('', '10'), ('', '10'), ('', '10'), ('', '10'), ('', '10'), ''),
    (161, '10-10', '21',  '2',     'Address Valid to R/W Low (Write)', 'ns',
     ('20', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (161, '10-10', '21A', '2',     'FC Valid to R/W Low (Write)', 'ns',
     ('60', ''), ('50', ''), ('30', ''), ('20', ''), ('30', ''), ('25', ''), ''),
    (161, '10-10', '22',  '2',     'R/W Low to DS Asserted (Write)', 'ns',
     ('80', ''), ('50', ''), ('30', ''), ('20', ''), ('30', ''), ('25', ''), ''),
    (161, '10-10', '23',  '',      'Clock Low to Data-Out Valid (Write)', 'ns',
     ('', '62'), ('', '50'), ('', '50'), ('', '550'), ('', '30'), ('', '25'),
     'SOURCE ERROR: the 16.67 MHz maximum prints as 550; 10.11 gives 50 for the same specification and grade'),
    (161, '10-10', '25',  '2, 10', 'AS, DS Negated to Data-Out Invalid (Write)', 'ns',
     ('40', ''), ('30', ''), ('20', ''), ('15', ''), ('15', ''), ('10', ''),
     'the 8 MHz cell prints "40" with the footnote marker 10 broken across two lines; '
     'note 10 reads "245 ns for the MC68008", which fits specification 28, not this one'),
    (162, '10-11', '26',  '2',     'Data-Out Valid to DS Asserted (Write)', 'ns',
     ('40', ''), ('30', ''), ('20', ''), ('15', ''), ('15', ''), ('10', ''), ''),
    (162, '10-11', '27',  '5',     'Data-In Valid to Clock Low (Setup Time on Read)', 'ns',
     ('10', ''), ('10', ''), ('10', ''), ('7', ''), ('5', ''), ('5', ''), ''),
    (162, '10-11', '27A', '5',     'Late BERR Asserted to Clock Low (Setup Time)', 'ns',
     ('45', ''), ('45', ''), ('45', ''), ('', ''), ('', ''), ('', ''),
     'not specified above 12.5 MHz'),
    (162, '10-11', '28',  '2, 11', 'AS, DS Negated to DTACK Negated (Asynchronous Hold)', 'ns',
     ('0', '240'), ('0', '190'), ('0', '150'), ('0', '110'), ('0', '110'), ('0', '95'),
     'the 8 MHz maximum prints "240" with the footnote marker 11 broken across two lines; '
     'note 11 reads "50 ns for the MC68008", which fits specification 25, not this one'),
    (162, '10-11', '28A', '',      'AS, DS Negated to Data-In High Impedance', 'ns',
     ('', '187'), ('', '150'), ('', '120'), ('', '110'), ('', '110'), ('', '95'), ''),
    (162, '10-11', '29',  '',      'AS, DS Negated to Data-In Invalid (Hold Time on Read)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (162, '10-11', '29A', '',      'AS, DS Negated to Data-In High Impedance', 'ns',
     ('', '187'), ('', '150'), ('', '120'), ('', '90'), ('', '90'), ('', '75'),
     'same characteristic text as 28A but different limits above 12.5 MHz'),
    (162, '10-11', '30',  '',      'AS, DS Negated to BERR Negated', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (162, '10-11', '31',  '2, 5',  'DTACK Asserted to Data-In Valid (Setup Time)', 'ns',
     ('', '90'), ('', '65'), ('', '50'), ('', '40'), ('', '50'), ('', '42'), ''),
    (162, '10-11', '32',  '',      'HALT and RESET Input Transition Time', 'ns',
     ('0', '200'), ('0', '200'), ('0', '200'), ('0', '150'), ('', '150'), ('0', '150'),
     'the 16 MHz minimum is dashed where every other grade gives 0'),
    (162, '10-11', '33',  '',      'Clock High to BG Asserted', 'ns',
     ('', '62'), ('', '50'), ('', '40'), ('', '40'), ('0', '30'), ('0', '25'), ''),
    (162, '10-11', '34',  '',      'Clock High to BG Negated', 'ns',
     ('', '62'), ('', '50'), ('', '40'), ('', '40'), ('0', '30'), ('0', '25'), ''),
    (162, '10-11', '35',  '',      'BR Asserted to BG Asserted', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'),
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    (162, '10-11', '36',  '7',     'BR Negated to BG Negated', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'),
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    (162, '10-11', '37',  '',      'BGACK Asserted to BG Negated', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'),
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    (162, '10-11', '37A', '8',     'BGACK Asserted to BR Negated', 'ns/Clks',
     ('20', '1.5'), ('20', '1.5'), ('20', '1.5'), ('10', '1.5'), ('10', '1.5'), ('10', '1.5'),
     'the minima are ns and the maxima Clks; 10.12 heads the unit column "Clks/ns", this table "ns"'),
    (162, '10-11', '38',  '',      'BG Asserted to Control, Address, Data Bus High Impedance (AS Negated)', 'ns',
     ('', '80'), ('', '70'), ('', '60'), ('', '50'), ('', '50'), ('', '42'), ''),
    (162, '10-11', '39',  '',      'BG Width Negated', 'clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    (162, '10-11', '40',  '',      'Clock Low to VMA Asserted', 'ns',
     ('', '70'), ('', '70'), ('', '70'), ('', '50'), ('', '50'), ('', '40'), ''),
    (162, '10-11', '41',  '12',    'Clock Low to E Transition', 'ns',
     ('', '55'), ('', '45'), ('', '35'), ('', '35'), ('', '35'), ('', '30'),
     'the 8 MHz maximum carries footnote 12, "50 ns for the MC68008"'),
    (162, '10-11', '42',  '',      'E Output Rise and Fall Time', 'ns',
     ('', '15'), ('', '15'), ('', '15'), ('', '15'), ('', '15'), ('', '12'), ''),
    (162, '10-11', '43',  '',      'VMA Asserted to E High', 'ns',
     ('200', ''), ('150', ''), ('90', ''), ('80', ''), ('80', ''), ('60', ''), ''),
    (162, '10-11', '44',  '',      'AS, DS Negated to VPA Negated', 'ns',
     ('0', '120'), ('0', '90'), ('0', '70'), ('0', '50'), ('0', '50'), ('0', '42'), ''),
    (162, '10-11', '45',  '',      'E Low to Control, Address Bus Invalid (Address Hold Time)', 'ns',
     ('30', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''), ''),
    (162, '10-11', '46',  '',      'BGACK Width Low', 'ns',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''),
     'SOURCE ERROR: the unit prints as ns; 10.12 gives the same limits in Clks, which is what 1.5 must be'),
    (163, '10-12', '47',  '5',     'Asynchronous Input Setup Time', 'ns',
     ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('5', ''), ('5', ''),
     'SOURCE INCONSISTENCY: 10.11 gives 10 ns at 16 MHz and 10.12 gives 5 ns at 16.67 MHz'),
    (163, '10-12', '48',  '2, 3',  'BERR Asserted to DTACK Asserted', 'ns',
     ('20', ''), ('20', ''), ('20', ''), ('10', ''), ('10', ''), ('10', ''), ''),
    (163, '10-12', '48*', '2, 3, 5', 'DTACK Asserted to BERR Asserted (MC68010 Only)', 'ns',
     ('', '80'), ('', '55'), ('', '35'), ('', ''), ('', ''), ('', ''),
     'SOURCE ERROR: printed as a second row numbered 48; 48* is this transcription\'s label for it'),
    (163, '10-12', '49',  '9',     'AS, DS Negated to E Low', 'ns',
     ('-70', '70'), ('-55', '55'), ('-45', '45'), ('-35', '35'), ('-35', '35'), ('-30', '30'), ''),
    (163, '10-12', '50',  '',      'E Width High', 'ns',
     ('450', ''), ('350', ''), ('280', ''), ('220', ''), ('220', ''), ('190', ''), ''),
    (163, '10-12', '51',  '',      'E Width Low', 'ns',
     ('700', ''), ('550', ''), ('440', ''), ('340', ''), ('340', ''), ('290', ''), ''),
    (163, '10-12', '53',  '',      'Data-Out Hold from Clock High', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (163, '10-12', '54',  '',      'E Low to Data-Out Invalid', 'ns',
     ('30', ''), ('20', ''), ('15', ''), ('10', ''), ('10', ''), ('5', ''), ''),
    (163, '10-12', '55',  '',      'R/W Asserted to Data Bus Impedance Change', 'ns',
     ('30', ''), ('20', ''), ('10', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (163, '10-12', '56',  '4',     'HALT/RESET Pulse Width', 'clks',
     ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''),
     'printed "HALT (RESETPulse Width" - a lost parenthesis and a lost space'),
    (163, '10-12', '57',  '',      'BGACK Negated to AS, DS, R/W Driven', 'clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    (163, '10-12', '57A', '',      'BGACK Negated to FC, VMA Driven', 'clks',
     ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''), ''),
    (163, '10-12', '58',  '7',     'BR Negated to AS, DS, R/W Driven', 'clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    (163, '10-12', '58A', '7',     'BR Negated to FC, AS Driven', 'clks',
     ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''),
     'SOURCE INCONSISTENCY: 10.12 gives the same specification as "BR Negated to FC, VMA Driven"'),
]

# 10.11  AC ELECTRICAL SPECIFICATIONS - MC68000 TO M6800 PERIPHERAL (10-15)
M6800_COND = ('VCC = 5.0 Vdc +/- 5%; GND = 0 Vdc; TA = TL to TH; '
              'applies to all processors except the MC68EC000')
M6800 = [
    ('12',  '1', 'Clock Low to AS, DS Negated', 'ns',
     ('', '62'), ('', '50'), ('', '40'), ('', '40'), ('3', '30'), ('3', '25'), ''),
    ('18',  '1', 'Clock High to R/W High (Read)', 'ns',
     ('0', '55'), ('0', '45'), ('0', '40'), ('0', '40'), ('0', '30'), ('0', '25'), ''),
    ('20',  '1', 'Clock High to R/W Low (Write)', 'ns',
     ('0', '55'), ('0', '45'), ('0', '40'), ('0', '40'), ('0', '30'), ('0', '25'), ''),
    ('23',  '',  'Clock Low to Data-Out Valid (Write)', 'ns',
     ('', '62'), ('', '50'), ('', '50'), ('', '50'), ('', '30'), ('', '25'),
     'the 16.67 MHz maximum reads 50 here and 550 in 10.10'),
    ('27',  '',  'Data-In Valid to Clock Low (Setup Time on Read)', 'ns',
     ('10', ''), ('10', ''), ('10', ''), ('7', ''), ('5', ''), ('5', ''), ''),
    ('29',  '',  'AS, DS Negated to Data-In Invalid (Hold Time on Read)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    ('40',  '',  'Clock Low to VMA Asserted', 'ns',
     ('', '70'), ('', '70'), ('', '70'), ('', '50'), ('', '50'), ('', '40'), ''),
    ('41',  '',  'Clock Low to E Transition', 'ns',
     ('', '55'), ('', '45'), ('', '35'), ('', '35'), ('', '35'), ('', '30'), ''),
    ('42',  '',  'E Output Rise and Fall Time', 'ns',
     ('', '15'), ('', '15'), ('', '15'), ('', '15'), ('', '15'), ('', '12'), ''),
    ('43',  '',  'VMA Asserted to E High', 'ns',
     ('200', ''), ('150', ''), ('90', ''), ('80', ''), ('80', ''), ('60', ''), ''),
    ('44',  '',  'AS, DS Negated to VPA Negated', 'ns',
     ('0', '120'), ('0', '90'), ('0', '70'), ('0', '50'), ('0', '50'), ('0', '42'), ''),
    ('45',  '',  'E Low to Control, Address Bus Invalid (Address Hold Time)', 'ns',
     ('30', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''), ''),
    ('47',  '',  'Asynchronous Input Setup Time', 'ns',
     ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('5', ''),
     'SOURCE INCONSISTENCY: 10.10 gives 5 ns at 16 MHz, 10.12 gives 5 ns from 16.67 MHz up'),
    ('49',  '2', 'AS, DS Negated to E Low', 'ns',
     ('-70', '70'), ('-55', '55'), ('-45', '45'), ('-35', '35'), ('-35', '35'), ('-30', '30'), ''),
    ('50',  '',  'E Width High', 'ns',
     ('450', ''), ('350', ''), ('280', ''), ('220', ''), ('220', ''), ('190', ''), ''),
    ('51',  '',  'E Width Low', 'ns',
     ('700', ''), ('550', ''), ('440', ''), ('340', ''), ('340', ''), ('290', ''), ''),
    ('54',  '',  'E Low to Data-Out Invalid', 'ns',
     ('30', ''), ('20', ''), ('15', ''), ('10', ''), ('10', ''), ('5', ''), ''),
]

# 10.12  AC ELECTRICAL SPECIFICATIONS - BUS ARBITRATION       (printed 10-17)
ARB_COND = ('VCC = 5.0 VDC +/- 5%; GND = 0 VDC; TA = TL to TH; '
            'applies to all processors except the MC68EC000')
ARB = [
    ('7',   '',  'Clock High to Address, Data Bus High Impedance (Maximum)', 'ns',
     ('', '80'), ('', '70'), ('', '60'), ('', '50'), ('', '50'), ('', '42'), ''),
    ('16',  '',  'Clock High to Control Bus High Impedance', 'ns',
     ('', '80'), ('', '70'), ('', '60'), ('', '50'), ('', '50'), ('', '42'), ''),
    ('33',  '',  'Clock High to BG Asserted', 'ns',
     ('', '62'), ('', '50'), ('', '40'), ('0', '40'), ('0', '30'), ('0', '25'),
     'the 16.67 MHz minimum is 0 here and dashed in 10.10'),
    ('34',  '',  'Clock High to BG Negated', 'ns',
     ('', '62'), ('', '50'), ('', '40'), ('0', '40'), ('0', '30'), ('0', '25'),
     'the 16.67 MHz minimum is 0 here and dashed in 10.10'),
    ('35',  '',  'BR Asserted to BG Asserted', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'),
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    ('36',  '1', 'BR Negated to BG Negated', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'),
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    ('37',  '',  'BGACK Asserted to BG Negated', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'),
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    ('37A', '2', 'BGACK Asserted to BR Negated', 'Clks/ns',
     ('20', '1.5'), ('20', '1.5'), ('20', '1.5'), ('10', '1.5'), ('10', '1.5'), ('10', '1.5'),
     'the minima are ns and the maxima Clks, so the printed unit reads Clks/ns'),
    ('38',  '',  'BG Asserted to Control, Address, Data Bus High Impedance (AS Negated)', 'ns',
     ('', '80'), ('', '70'), ('', '60'), ('', '50'), ('', '50'), ('', '42'),
     'the first three minimum cells are blank rather than dashed'),
    ('39',  '',  'BG Width Negated', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    ('46',  '',  'BGACK Width Low', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''),
     '10.10 gives the same limits with the unit printed as ns'),
    ('47',  '',  'Asynchronous Input Setup Time', 'ns',
     ('10', ''), ('10', ''), ('10', ''), ('5', ''), ('5', ''), ('5', ''),
     'SOURCE INCONSISTENCY: 10.10 gives 10 ns at 16.67 MHz and 10.11 gives 10 ns at 16 MHz'),
    ('57',  '',  'BGACK Negated to AS, DS, R/W Driven', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    ('57A', '',  'BGACK Negated to FC, VMA Driven', 'Clks',
     ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''), ''),
    ('58',  '1', 'BR Negated to AS, DS, R/W Driven', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    ('58A', '1', 'BR Negated to FC, VMA Driven', 'Clks',
     ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''),
     '10.10 gives the same specification as "BR Negated to FC, AS Driven"'),
]

# 10.14  MC68EC000 AC ELECTRICAL SPECIFICATIONS - READ AND WRITE CYCLES
# (printed 10-24 .. 10-25; the header prints "+/- 5;PC" for "+/- 5%")
EC_RW_COND = 'VCC = 5.0 VDC +/- 5%; GND = 0 VDC; TA = TL to TH; MC68EC000 only'
EC_RW = [
    (175, '10-24', '6',   '',       'Clock Low to Address Valid', 'ns',
     ('', '35'), ('', '35'), ('', '35'), ('', '30'), ('', '25'), ''),
    (175, '10-24', '6A',  '',       'Clock High to FC Valid', 'ns',
     ('', '35'), ('', '35'), ('', '35'), ('', '30'), ('0', '25'), ''),
    (175, '10-24', '7',   '',       'Clock High to Address, Data Bus High Impedance (Maximum)', 'ns',
     ('', '55'), ('', '55'), ('', '55'), ('', '50'), ('', '42'), ''),
    (175, '10-24', '8',   '',       'Clock High to Address, FC Invalid (Minimum)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (175, '10-24', '9',   '1',      'Clock High to AS, DS Asserted', 'ns',
     ('3', '35'), ('3', '35'), ('3', '35'), ('3', '30'), ('3', '25'), ''),
    (175, '10-24', '11',  '2',      'Address Valid to AS, DS Asserted (Read)/AS Asserted (Write)', 'ns',
     ('30', ''), ('20', ''), ('15', ''), ('15', ''), ('10', ''), ''),
    (175, '10-24', '11A', '2',      'FC Valid to AS, DS Asserted (Read)/AS Asserted (Write)', 'ns',
     ('45', ''), ('45', ''), ('45', ''), ('45', ''), ('40', ''), ''),
    (175, '10-24', '12',  '1',      'Clock Low to AS, DS Negated', 'ns',
     ('3', '35'), ('3', '35'), ('3', '35'), ('3', '30'), ('3', '25'), ''),
    (175, '10-24', '13',  '2',      'AS, DS Negated to Address, FC Invalid', 'ns',
     ('15', ''), ('15', ''), ('15', ''), ('15', ''), ('10', ''), ''),
    (175, '10-24', '14',  '2',      'AS (and DS Read) Width Asserted', 'ns',
     ('270', ''), ('195', ''), ('160', ''), ('120', ''), ('100', ''), ''),
    (175, '10-24', '14A', '2',      'DS Width Asserted (Write)', 'ns',
     ('140', ''), ('95', ''), ('80', ''), ('60', ''), ('50', ''), ''),
    (175, '10-24', '15',  '2',      'AS, DS Width Negated', 'ns',
     ('150', ''), ('105', ''), ('65', ''), ('60', ''), ('50', ''), ''),
    (175, '10-24', '16',  '',       'Clock High to Control Bus High Impedance', 'ns',
     ('', '55'), ('', '55'), ('', '55'), ('', '50'), ('', '42'), ''),
    (175, '10-24', '17',  '2',      'AS, DS Negated to R/W Invalid', 'ns',
     ('15', ''), ('15', ''), ('15', ''), ('15', ''), ('10', ''), ''),
    (175, '10-24', '18',  '1',      'Clock High to R/W High (Read)', 'ns',
     ('0', '35'), ('0', '35'), ('0', '35'), ('0', '30'), ('0', '25'), ''),
    (175, '10-24', '20',  '1',      'Clock High to R/W Low (Write)', 'ns',
     ('0', '35'), ('0', '35'), ('0', '35'), ('0', '30'), ('0', '25'), ''),
    (175, '10-24', '20A', '2, 6',   'AS Asserted to R/W Low (Write)', 'ns',
     ('', '10'), ('', '10'), ('', '10'), ('', '10'), ('', '10'),
     '10.10 gives the same specification as "AS Asserted to R/W Valid (Write)"'),
    (175, '10-24', '21',  '2',      'Address Valid to R/W Low (Write)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (175, '10-24', '21A', '2',      'FC Valid to R/W Low (Write)', 'ns',
     ('60', ''), ('50', ''), ('30', ''), ('30', ''), ('25', ''), ''),
    (175, '10-24', '22',  '2',      'R/W Low to DS Asserted (Write)', 'ns',
     ('80', ''), ('50', ''), ('30', ''), ('30', ''), ('25', ''), ''),
    (175, '10-24', '23',  '',       'Clock Low to Data-Out Valid (Write)', 'ns',
     ('', '35'), ('', '35'), ('', '35'), ('', '30'), ('', '25'), ''),
    (175, '10-24', '25',  '2',      'AS, DS Negated to Data-Out Invalid (Write)', 'ns',
     ('40', ''), ('30', ''), ('20', ''), ('15', ''), ('10', ''), ''),
    (175, '10-24', '26',  '2',      'Data-Out Valid to DS Asserted (Write)', 'ns',
     ('40', ''), ('30', ''), ('20', ''), ('15', ''), ('10', ''), ''),
    (175, '10-24', '27',  '5',      'Data-In Valid to Clock Low (Setup Time on Read)', 'ns',
     ('5', ''), ('5', ''), ('5', ''), ('5', ''), ('5', ''), ''),
    (175, '10-24', '28',  '2',      'AS, DS Negated to DTACK Negated (Asynchronous Hold)', 'ns',
     ('0', '110'), ('0', '110'), ('0', '110'), ('0', '110'), ('0', '95'), ''),
    (175, '10-24', '28A', '',       'Clock High to DTACK Negated', 'ns',
     ('0', '110'), ('0', '110'), ('0', '110'), ('0', '110'), ('0', '95'),
     '10.10 numbers a different characteristic 28A, "AS, DS Negated to Data-In High Impedance"'),
    (176, '10-25', '29',  '',       'AS, DS Negated to Data-In Invalid (Hold Time on Read)', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (176, '10-25', '29A', '',       'AS, DS Negated to Data-In High Impedance', 'ns',
     ('', '187'), ('', '150'), ('', '120'), ('', '90'), ('', '75'), ''),
    (176, '10-25', '30',  '',       'AS, DS Negated to BERR Negated', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (176, '10-25', '31',  '2, 5',   'DTACK Asserted to Data-In Valid (Setup Time)', 'ns',
     ('', '90'), ('', '65'), ('', '50'), ('', '50'), ('', '42'), ''),
    (176, '10-25', '32',  '',       'HALT and RESET Input Transition Time', 'ns',
     ('0', '150'), ('0', '150'), ('0', '150'), ('0', '150'), ('0', '150'), ''),
    (176, '10-25', '33',  '',       'Clock High to BG Asserted', 'ns',
     ('', '35'), ('', '35'), ('', '35'), ('0', '30'), ('0', '25'), ''),
    (176, '10-25', '34',  '',       'Clock High to BG Negated', 'ns',
     ('', '35'), ('', '35'), ('', '35'), ('0', '30'), ('0', '25'), ''),
    (176, '10-25', '35',  '',       'BR Asserted to BG Asserted', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    (176, '10-25', '36',  '7',      'BR Negated to BG Negated', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    (176, '10-25', '38',  '',       'BG Asserted to Control, Address, Data Bus High Impedance (AS Negated)', 'ns',
     ('', '55'), ('', '55'), ('', '55'), ('', '50'), ('', '42'), ''),
    (176, '10-25', '39',  '',       'BG Width Negated', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''),
     'the first four maximum cells are blank rather than dashed'),
    (176, '10-25', '44',  '',       'AS, DS Negated to VPA Negated', 'ns',
     ('0', '55'), ('0', '55'), ('0', '55'), ('0', '50'), ('0', '42'),
     'VPA is an MC68000 signal; the MC68EC000 has AVEC in its place'),
    (176, '10-25', '47',  '5',      'Asynchronous Input Setup Time', 'ns',
     ('5', ''), ('5', ''), ('5', ''), ('5', ''), ('5', ''), ''),
    (176, '10-25', '48',  '2, 3',   'BERR Asserted to DTACK Asserted', 'ns',
     ('20', ''), ('20', ''), ('20', ''), ('10', ''), ('10', ''), ''),
    (176, '10-25', '53',  '',       'Data-Out Hold from Clock High', 'ns',
     ('0', ''), ('0', ''), ('0', ''), ('0', ''), ('0', ''), ''),
    (176, '10-25', '55',  '',       'R/W Asserted to Data Bus Impedance Change', 'ns',
     ('30', ''), ('20', ''), ('10', ''), ('0', ''), ('0', ''), ''),
    (176, '10-25', '56',  '4',      'HALT/RESET Pulse Width', 'Clks',
     ('10', ''), ('10', ''), ('10', ''), ('10', ''), ('10', ''), ''),
    (176, '10-25', '58',  '7',      'BR Negated to AS, DS, R/W Driven', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    (176, '10-25', '58A', '7',      'BR Negated to FC, VMA Driven', 'Clks',
     ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''), ''),
]

# 10.15  MC68EC000 AC ELECTRICAL SPECIFICATIONS - BUS ARBITRATION  (10-28)
EC_ARB_COND = ('VCC = 5.0 VDC +/- 5%; GND = 0 VDC; TA = TL to TH; MC68EC000 only')
EC_ARB = [
    ('7',   '',  'Clock High to Address, Data Bus High Impedance (Maximum)', 'ns',
     ('', '55'), ('', '55'), ('', '55'), ('', '50'), ('', '42'), ''),
    ('16',  '',  'Clock High to Control Bus High Impedance', 'ns',
     ('', '55'), ('', '55'), ('', '55'), ('', '50'), ('', '42'), ''),
    ('33',  '',  'Clock High to BG Asserted', 'ns',
     ('', '35'), ('', '35'), ('', '35'), ('0', '30'), ('0', '25'), ''),
    ('34',  '',  'Clock High to BG Negated', 'ns',
     ('', '35'), ('', '35'), ('', '35'), ('0', '30'), ('0', '25'), ''),
    ('35',  '',  'BR Asserted to BG Asserted', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ''),
    ('36',  '7', 'BR Negated to BG Negated', 'Clks',
     ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'), ('1.5', '3.5'),
     'SOURCE ERROR: the marker is 7 but this table defines only notes 1 and 2'),
    ('38',  '',  'BG Asserted to Control, Address, Data Bus High Impedance (AS Negated)', 'ns',
     ('', '55'), ('', '55'), ('', '55'), ('', '50'), ('', '42'), ''),
    ('39',  '',  'BG Width Negated', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    ('47',  '',  'Asynchronous Input Setup Time', 'ns',
     ('5', ''), ('5', ''), ('5', ''), ('5', ''), ('5', ''), ''),
    ('58',  '1', 'BR Negated to AS, DS, R/W Driven', 'Clks',
     ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ('1.5', ''), ''),
    ('58A', '1', 'BR Negated to FC Driven', 'Clks',
     ('1', ''), ('1', ''), ('1', ''), ('1', ''), ('1', ''),
     '10.14 gives the same specification as "BR Negated to FC, VMA Driven"'),
]


def ac_row(table, page, printed, num, foot, char, cond, unit, pairs, grades, note):
    r = {'table': table, 'pdf_page': page, 'printed_page': printed, 'num': num,
         'footnotes': foot, 'characteristic': char, 'condition': cond,
         'unit': unit, 'note': note}
    for g in GRADES6:
        r['%s_min' % g] = r['%s_max' % g] = ''
    for g, (lo, hi) in zip(grades, pairs):
        r['%s_min' % g], r['%s_max' % g] = lo, hi
    return r


def build_ac():
    rows = []
    for num, foot, char, unit, *rest in CLOCK:
        rows.append(ac_row('clock', 159, '10-8', num, foot, char, CLOCK_COND,
                           unit, rest[:-1], GRADES6, rest[-1]))
    for num, foot, char, unit, *rest in CLOCK08:
        rows.append(ac_row('clock-mc68008', 160, '10-9', num, foot, char,
                           CLOCK08_COND, unit, rest[:-1], GRADES2, rest[-1]))
    for page, printed, num, foot, char, unit, *rest in RW:
        rows.append(ac_row('read-write', page, printed, num, foot, char,
                           RW_COND, unit, rest[:-1], GRADES6, rest[-1]))
    for num, foot, char, unit, *rest in M6800:
        rows.append(ac_row('m6800-peripheral', 166, '10-15', num, foot, char,
                           M6800_COND, unit, rest[:-1], GRADES6, rest[-1]))
    for num, foot, char, unit, *rest in ARB:
        rows.append(ac_row('bus-arbitration', 168, '10-17', num, foot, char,
                           ARB_COND, unit, rest[:-1], GRADES6, rest[-1]))
    for page, printed, num, foot, char, unit, *rest in EC_RW:
        rows.append(ac_row('mc68ec000-read-write', page, printed, num, foot,
                           char, EC_RW_COND, unit, rest[:-1], GRADES5, rest[-1]))
    for num, foot, char, unit, *rest in EC_ARB:
        rows.append(ac_row('mc68ec000-bus-arbitration', 179, '10-28', num, foot,
                           char, EC_ARB_COND, unit, rest[:-1], GRADES5, rest[-1]))
    return rows


# ---------------------------------------------------------------------------
# The DC, maximum-rating, thermal and power-dissipation tables.  These have
# nothing like the AC tables' six-grade shape, so they get their own file
# with a plain min/max/typ layout.
DC_COLS = ['table', 'pdf_page', 'printed_page', 'characteristic', 'applies_to',
           'symbol', 'min', 'max', 'unit', 'note']

DC = [
    # 10.1  MAXIMUM RATINGS                                    (printed 10-1)
    ('maximum-ratings', 152, '10-1', 'Supply Voltage', '', 'VCC', '-0.3', '7.0', 'V', ''),
    ('maximum-ratings', 152, '10-1', 'Input Voltage', '', 'Vin', '-0.3', '7.0', 'V', ''),
    ('maximum-ratings', 152, '10-1', 'Maximum Operating Temperature Range', '',
     'TA', 'TL', 'TH', 'degC', 'the range is given as TL to TH and then broken out below'),
    ('maximum-ratings', 152, '10-1', 'Maximum Operating Temperature Range', 'standard',
     'TA', '0', '70', 'degC', ''),
    ('maximum-ratings', 152, '10-1', 'Maximum Operating Temperature Range',
     'Commerical Extended "C" Grade', 'TA', '-40', '85', 'degC',
     'the source spells it "Commerical"'),
    ('maximum-ratings', 152, '10-1', 'Maximum Operating Temperature Range',
     'Commerical Extended "I" Grade', 'TA', '0', '85', 'degC',
     'the source spells it "Commerical"'),
    ('maximum-ratings', 152, '10-1', 'Storage Temperature', '', 'Tstg', '-55', '150', 'degC', ''),

    # 10.2  THERMAL CHARACTERISTICS                            (printed 10-1)
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Ceramic, Type L/LC', 'ThetaJA', '', '30', 'degC/W', ''),
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Ceramic, Type R/RC', 'ThetaJA', '', '33', 'degC/W', ''),
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Plastic, Type P', 'ThetaJA', '', '30', 'degC/W', ''),
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Plastic, Type FN', 'ThetaJA', '', '45', 'degC/W',
     'estimated; Table 10-2 gives 40 for the same package'),
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Ceramic, Type L/LC', 'ThetaJC', '', '15', 'degC/W', 'estimated'),
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Ceramic, Type R/RC', 'ThetaJC', '', '15', 'degC/W', ''),
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Plastic, Type P', 'ThetaJC', '', '15', 'degC/W', 'estimated'),
    ('thermal', 152, '10-1', 'Thermal Resistance', 'Plastic, Type FN', 'ThetaJC', '', '25', 'degC/W', 'estimated'),

    # 10.6  MC68000/68008/68010 DC ELECTRICAL CHARACTERISTICS  (printed 10-7)
    ('dc-mc68000-68008-68010', 158, '10-7', 'Input High Voltage', '', 'VIH', '2.0', 'VCC', 'V', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Input Low Voltage', '', 'VIL', 'GND-0.3', '0.8', 'V', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Input Leakage Current @ 5.25 V',
     'BERR, BGACK, BR, DTACK, CLK, IPL0-IPL2, VPA', 'IIN', '', '2.5', 'uA', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Input Leakage Current @ 5.25 V',
     'MODE, HALT, RESET', 'IIN', '', '20', 'uA', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Three-State (Off State) Input Current @ 2.4 V/0.4 V',
     'AS, A1-A23, D0-D15, FC0-FC2, LDS, R/W, UDS, VMA', 'ITSI', '', '20', 'uA', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Output High Voltage (IOH = -400 uA)',
     'E', 'VOH', 'VCC-0.75', '', 'V', 'footnote: with an external pullup resistor of 1.1 Ohm'),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Output High Voltage (IOH = -400 uA)',
     'AS, A1-A23, BG, D0-D15, FC0-FC2, LDS, R/W, UDS, VMA', 'VOH', '2.4', '2.4', 'V',
     'SOURCE ERROR: 2.4 is printed in both the minimum and the maximum column; '
     '10.7 gives this line as a minimum only'),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Output Low Voltage (IOL = 1.6 mA)', 'HALT', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Output Low Voltage (IOL = 3.2 mA)',
     'A1-A23, BG, FC0-FC2', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Output Low Voltage (IOL = 5.0 mA)', 'RESET', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Output Low Voltage (IOL = 5.3 mA)',
     'E, AS, D0-D15, LDS, R/W, UDS, VMA', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Power Dissipation (see POWER CONSIDERATIONS)',
     '', 'PD', '', '', 'W', 'during normal operation instantaneous VCC current may be as high as 1.5 A'),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Capacitance (Vin = 0 V, TA = 25 degC, Frequency = 1 MHz)',
     '', 'Cin', '', '20.0', 'pF', 'periodically sampled rather than 100% tested'),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Load Capacitance', 'HALT', 'CL', '', '70', 'pF', ''),
    ('dc-mc68000-68008-68010', 158, '10-7', 'Load Capacitance', 'All Others', 'CL', '', '130', 'pF', ''),

    # 10.7  DC ELECTRICAL CHARACTERISTICS                      (printed 10-8)
    ('dc-common', 159, '10-8', 'Input High Voltage', '', 'VIH', '2.0', 'VCC', 'V', ''),
    ('dc-common', 159, '10-8', 'Input Low Voltage', '', 'VIL', 'GND-0.3', '0.8', 'V', ''),
    ('dc-common', 159, '10-8', 'Input Leakage Current @ 5.25 V',
     'BERR, BGACK, BR, DTACK, CLK, IPL0-IPL2, VPA', 'IIN', '', '2.5', 'uA', ''),
    ('dc-common', 159, '10-8', 'Input Leakage Current @ 5.25 V',
     'MODE, HALT, RESET', 'IIN', '', '20', 'uA', ''),
    ('dc-common', 159, '10-8', 'Three-State (Off State) Input Current @ 2.4 V/0.4 V',
     'AS, A0-A23, D0-D15, FC0-FC2, LDS, R/W, UDS, VMA', 'ITSI', '', '20', 'uA', ''),
    ('dc-common', 159, '10-8', 'Output High Voltage',
     'E, AS, A0-A23, BG, D0-D15, FC0-FC2, LDS, R/W, UDS, VMA', 'VOH', 'VCC-0.75', '', 'V', ''),
    ('dc-common', 159, '10-8', 'Output Low Voltage (IOL = 1.6 mA)', 'HALT', 'VOL', '', '0.5', 'V', ''),
    ('dc-common', 159, '10-8', 'Output Low Voltage (IOL = 3.2 mA)',
     'A0-A23, BG, FC0-FC2', 'VOL', '', '0.5', 'V', ''),
    ('dc-common', 159, '10-8', 'Output Low Voltage (IOL = 5.0 mA)', 'RESET', 'VOL', '', '0.5', 'V', ''),
    ('dc-common', 159, '10-8', 'Output Low Voltage (IOL = 5.3 mA)',
     'E, AS, D0-D15, LDS, R/W, UDS, VMA', 'VOL', '', '0.5', 'V', ''),
    ('dc-common', 159, '10-8', 'Current Dissipation', 'f = 8 MHz', 'ID', '', '25', 'mA', 'with no loading'),
    ('dc-common', 159, '10-8', 'Current Dissipation', 'f = 10 MHz', 'ID', '', '30', 'mA', 'with no loading'),
    ('dc-common', 159, '10-8', 'Current Dissipation', 'f = 12.5 MHz', 'ID', '', '35', 'mA', 'with no loading'),
    ('dc-common', 159, '10-8', 'Current Dissipation', 'f = 16.67 MHz', 'ID', '', '50', 'mA', 'with no loading'),
    ('dc-common', 159, '10-8', 'Current Dissipation', 'f = 20 MHz', 'ID', '', '70', 'mA', 'with no loading'),
    ('dc-common', 159, '10-8', 'Power Dissipation', 'f = 8 MHz', 'PD', '', '0.13', 'W', ''),
    ('dc-common', 159, '10-8', 'Power Dissipation', 'f = 10 MHz', 'PD', '', '0.16', 'W', ''),
    ('dc-common', 159, '10-8', 'Power Dissipation', 'f = 12.5 MHz', 'PD', '', '0.19', 'W', ''),
    ('dc-common', 159, '10-8', 'Power Dissipation', 'f = 16.67 MHz', 'PD', '', '0.26', 'W', ''),
    ('dc-common', 159, '10-8', 'Power Dissipation', 'f = 20 MHz', 'PD', '', '0.38', 'W', ''),
    ('dc-common', 159, '10-8', 'Capacitance (Vin = 0 V, TA = 25 degC, Frequency = 1 MHz)',
     '', 'Cin', '', '20.0', 'pF', 'periodically sampled rather than 100% tested'),
    ('dc-common', 159, '10-8', 'Load Capacitance', 'HALT', 'CL', '', '70', 'pF', ''),
    ('dc-common', 159, '10-8', 'Load Capacitance', 'All Others', 'CL', '', '130', 'pF', ''),

    # 10.13  MC68EC000 DC ELECTRICAL SPECIFICATIONS            (printed 10-23)
    ('dc-mc68ec000', 174, '10-23', 'Input High Voltage', '', 'VIH', '2.0', 'VCC', 'V', ''),
    ('dc-mc68ec000', 174, '10-23', 'Input Low Voltage', '', 'VIL', 'GND-0.3', '0.8', 'V', ''),
    ('dc-mc68ec000', 174, '10-23', 'Input Leakage Current @ 5.25 V',
     'BERR, BR, DTACK, CLK, IPL2-IPL0, AVEC', 'Iin', '', '2.5', 'uA', ''),
    ('dc-mc68ec000', 174, '10-23', 'Input Leakage Current @ 5.25 V',
     'MODE, HALT, RESET', 'Iin', '', '20', 'uA', ''),
    ('dc-mc68ec000', 174, '10-23', 'Three-State (Off State) Input Current @ 2.4 V/0.4 V',
     'AS, A23-A0, D15-D0, FC2-FC0, LDS, R/W, UDS', 'ITSI', '', '20', 'uA', ''),
    ('dc-mc68ec000', 174, '10-23', 'Output High Voltage (IOH = -400 uA)',
     'AS, A23-A0, BG, D15-D0, FC2-FC0, LDS, R/W, UDS', 'VOH', 'VCC-0.75', '', 'V', ''),
    ('dc-mc68ec000', 174, '10-23', 'Output Low Voltage (IOL = 1.6 mA)', 'HALT', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68ec000', 174, '10-23', 'Output Low Voltage (IOL = 3.2 mA)',
     'A23-A0, BG, FC2-FC0', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68ec000', 174, '10-23', 'Output Low Voltage (IOL = 5.0 mA)', 'RESET', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68ec000', 174, '10-23', 'Output Low Voltage (IOL = 5.3 mA)',
     'AS, D15-D0, LDS, R/W, UDS', 'VOL', '', '0.5', 'V', ''),
    ('dc-mc68ec000', 174, '10-23', 'Current Dissipation', 'f = 8 MHz', 'ID', '', '25', 'mA', 'with no loading'),
    ('dc-mc68ec000', 174, '10-23', 'Current Dissipation', 'f = 10 MHz', 'ID', '', '30', 'mA', 'with no loading'),
    ('dc-mc68ec000', 174, '10-23', 'Current Dissipation', 'f = 12.5 MHz', 'ID', '', '35', 'mA', 'with no loading'),
    ('dc-mc68ec000', 174, '10-23', 'Current Dissipation', 'f = 16.67 MHz', 'ID', '', '50', 'mA', 'with no loading'),
    ('dc-mc68ec000', 174, '10-23', 'Current Dissipation', 'f = 20 MHz', 'ID', '', '70', 'mA', 'with no loading'),
    ('dc-mc68ec000', 174, '10-23', 'Power Dissipation', 'f = 8 MHz', 'PD', '', '0.13', 'W', ''),
    ('dc-mc68ec000', 174, '10-23', 'Power Dissipation', 'f = 10 MHz', 'PD', '', '0.16', 'W', ''),
    ('dc-mc68ec000', 174, '10-23', 'Power Dissipation', 'f = 12.5 MHz', 'PD', '', '0.19', 'W', ''),
    ('dc-mc68ec000', 174, '10-23', 'Power Dissipation', 'f = 16.67 MHz', 'PD', '', '0.26', 'W', ''),
    ('dc-mc68ec000', 174, '10-23', 'Power Dissipation', 'f = 20 MHz', 'PD', '', '0.38', 'W', ''),
    ('dc-mc68ec000', 174, '10-23', 'Capacitance (Vin = 0 V, TA = 25 degC, Frequency = 1 MHz)',
     '', 'Cin', '', '20.0', 'pF', 'periodically sampled rather than 100% tested'),
    ('dc-mc68ec000', 174, '10-23', 'Load Capacitance', 'HALT', 'CL', '', '70', 'pF', ''),
    ('dc-mc68ec000', 174, '10-23', 'Load Capacitance', 'All Others', 'CL', '', '130', 'pF', ''),
]

# Tables 10-1 and 10-2, power dissipation and junction temperature.  10-1 is
# headed "(ThetaJC = ThetaJA)" and tabulates ThetaJC; 10-2 is headed
# "(ThetaJC != ThetaJC)" - the source's own typo for ThetaJA - and tabulates
# ThetaJA.
PD_COLS = ['table', 'pdf_page', 'printed_page', 'package', 'ta_range',
           'theta_symbol', 'theta_c_per_w', 'pd_w_at_ta_min', 'tj_c_at_ta_min',
           'pd_w_at_ta_max', 'tj_c_at_ta_max', 'note']
PD = [
    ('10-1', 155, '10-4', 'L/LC', '0 to 70',   'ThetaJC', '15', '1.5', '23',  '1.2', '88',  ''),
    ('10-1', 155, '10-4', 'L/LC', '-40 to 85', 'ThetaJC', '15', '1.7', '-14', '1.2', '103', ''),
    ('10-1', 155, '10-4', 'L/LC', '0 to 85',   'ThetaJC', '15', '1.5', '23',  '1.2', '103', ''),
    ('10-1', 155, '10-4', 'P',    '0 to 70',   'ThetaJC', '15', '1.5', '23',  '1.2', '88',  ''),
    ('10-1', 155, '10-4', 'R/RC', '0 to 70',   'ThetaJC', '15', '1.5', '23',  '1.2', '88',  ''),
    ('10-1', 155, '10-4', 'R/RC', '-40 to 85', 'ThetaJC', '15', '1.7', '-14', '1.2', '103', ''),
    ('10-1', 155, '10-4', 'R/RC', '0 to 85',   'ThetaJC', '15', '1.5', '23',  '1.2', '103', ''),
    ('10-1', 155, '10-4', 'FN',   '0 to 70',   'ThetaJC', '25', '1.5', '38',  '1.2', '101', ''),
    ('10-2', 155, '10-4', 'L/LC', '0 to 70',   'ThetaJA', '30', '1.5', '23',  '1.2', '88',  ''),
    ('10-2', 155, '10-4', 'L/LC', '-40 to 85', 'ThetaJA', '30', '1.7', '-14', '1.2', '103', ''),
    ('10-2', 155, '10-4', 'L/LC', '0 to 85',   'ThetaJA', '30', '1.5', '23',  '1.2', '103', ''),
    ('10-2', 155, '10-4', 'P',    '0 to 70',   'ThetaJA', '30', '1.5', '23',  '1.2', '88',  ''),
    ('10-2', 155, '10-4', 'R/RC', '0 to 70',   'ThetaJA', '33', '1.5', '23',  '1.2', '88',  ''),
    ('10-2', 155, '10-4', 'R/RC', '-40 to 85', 'ThetaJA', '33', '1.7', '-14', '1.2', '103', ''),
    ('10-2', 155, '10-4', 'R/RC', '0 to 85',   'ThetaJA', '33', '1.5', '23',  '1.2', '103', ''),
    ('10-2', 155, '10-4', 'FN',   '0 to 70',   'ThetaJA', '40', '1.5', '38',  '1.2', '101',
     'section 10.2 gives 45 for the FN package'),
]


def write(name, cols, rows, dicts=False):
    path = os.path.join(HERE, name)
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols] if dicts else list(r))
    print('%-40s %3d rows' % (name, len(rows)))
    return rows


def main():
    ac = build_ac()
    write('ac-electrical-specifications.csv', AC_COLS, ac, dicts=True)
    write('dc-electrical-specifications.csv', DC_COLS, DC)
    write('power-dissipation.csv', PD_COLS, PD)
    n = sum(1 for r in ac for g in GRADES6 for s in ('min', 'max')
            if r['%s_%s' % (g, s)])
    print('%d AC limits transcribed across %d specification rows' % (n, len(ac)))


if __name__ == '__main__':
    main()
