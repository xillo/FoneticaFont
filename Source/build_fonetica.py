#!/usr/bin/env python3
"""Build Fonetica 1.0.0 from Atkinson Hyperlegible 1.02 OpenType originals.

Fonetica customization and adaptation: Davide Perillo (2026).
Underlying typeface: Braille Institute of America / Applied Design Works (2020).
License: SIL Open Font License 1.1.

Requires: fonttools >=4.0. For WOFF2, also install brotli.
Run: python Source/build_fonetica.py --sources /path/to/atkinson/ --output ./Fonetica
"""
from argparse import ArgumentParser
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FAMILY = 'Fonetica'
AUTHOR = 'Davide Perillo'
VERSION = '1.000'
DATE = '2026-11-21'
DEFAULT_SOURCE = Path('/usr/share/texlive/texmf-dist/fonts/opentype/public/atkinson')
STYLES = {
    'Regular': ('Atkinson-Hyperlegible-Regular-102.otf', False, False),
    'Bold': ('Atkinson-Hyperlegible-Bold-102.otf', True, False),
    'Italic': ('Atkinson-Hyperlegible-Italic-102.otf', False, True),
    'BoldItalic': ('Atkinson-Hyperlegible-BoldItalic-102.otf', True, True),
}


def bounds(glyphset, name):
    pen = BoundsPen(glyphset)
    glyphset[name].draw(pen)
    return pen.bounds


def change_accent_glyph(font, composite_name, base, accent, size_kind, italic):
    glyphset = font.getGlyphSet()
    original_advance, _ = font['hmtx'][base]
    x0, _, x1, _ = bounds(glyphset, base)
    a0, ay0, a1, _ = bounds(glyphset, accent)
    center = (x0 + x1) / 2

    if size_kind == 'small':
        body_scale, acute_scale_x, acute_scale_y = 0.675, 0.77, 0.75
        accent_bottom = 425
        advance = round(original_advance * 0.82)
    else:
        body_scale, acute_scale_x, acute_scale_y = 1.265, 1.15, 1.14
        accent_bottom = 692
        advance = round(original_advance * 1.205)

    x_shift = advance / 2 - center * body_scale
    mark_center = advance / 2 + (18 if italic else 0)
    accent_x = mark_center - (a0 + a1) / 2 * acute_scale_x
    accent_y = accent_bottom - ay0 * acute_scale_y

    pen = T2CharStringPen(advance, glyphset)
    glyphset[base].draw(TransformPen(pen, (body_scale, 0, 0, body_scale, x_shift, 0)))
    glyphset[accent].draw(TransformPen(pen, (acute_scale_x, 0, 0, acute_scale_y, accent_x, accent_y)))
    top = font['CFF '].cff.topDictIndex[0]
    top.CharStrings[composite_name] = pen.getCharString(
        private=top.Private, globalSubrs=font['CFF '].cff.GlobalSubrs)
    font['hmtx'][composite_name] = (advance, round(x_shift + x0 * body_scale))


def update_metadata(font, style, bold, italic):
    subfamily = 'Bold Italic' if bold and italic else ('Bold' if bold else ('Italic' if italic else 'Regular'))
    postscript_style = 'BoldItalic' if bold and italic else ('Bold' if bold else ('Italic' if italic else 'Regular'))
    fullname = f'{FAMILY} {subfamily}'
    ps_name = f'Fonetica-{postscript_style}'
    values = {
        0: ('Copyright 2020 Braille Institute of America, Inc. '
            'Fonetica modifications copyright 2026 Davide Perillo. '
            'Licensed under SIL Open Font License 1.1.'),
        1: FAMILY,
        2: subfamily,
        3: f'Fonetica;{VERSION};{postscript_style};2026;DavidePerillo',
        4: fullname,
        5: f'Version {VERSION}; {DATE}',
        6: ps_name,
        7: 'Fonetica - a modified, independently named font derived from Atkinson Hyperlegible.',
        8: 'Davide Perillo (Fonetica modifications); original: Braille Institute / Applied Design Works',
        9: AUTHOR,
        10: ('Fonetica is an Italian diction-oriented variation designed by Davide Perillo '
             'using the Atkinson Hyperlegible base design. Grave-accented è/ò are compact; '
             'acute-accented é/ó are enlarged. The original typeface was designed '
             'for Braille Institute of America. No endorsement is implied.'),
        11: 'https://github.com/googlefonts/atkinson-hyperlegible',
        12: 'https://github.com/googlefonts/atkinson-hyperlegible',
        13: 'SIL Open Font License, Version 1.1. See the distributed OFL.txt.',
        14: 'https://openfontlicense.org/open-font-license-official-text/',
        16: FAMILY,
        17: subfamily,
        18: fullname,
    }
    table = font['name']
    for name_id, text in values.items():
        table.removeNames(nameID=name_id)
        table.setName(text, name_id, 3, 1, 0x409)
        table.setName(text, name_id, 1, 0, 0)

    top = font['CFF '].cff.topDictIndex[0]
    top.FamilyName = FAMILY
    top.FullName = fullname
    top.FontName = ps_name
    top.version = VERSION
    top.Copyright = ('Copyright 2020 Braille Institute of America, Inc. '
                     'Modifications copyright 2026 Davide Perillo.')
    top.Notice = 'SIL Open Font License 1.1. Fonetica is based on Atkinson Hyperlegible.'
    font['head'].fontRevision = 1.0
    if 'DSIG' in font:
        del font['DSIG']  # Original digital signature would not cover changed data.


def build_face(source_file, otf_output, woff2_output, style, bold, italic):
    font = TTFont(source_file)
    cmap = font.getBestCmap()
    for char, kind, base, accent in (
        ('è', 'small', 'e', 'grave'),
        ('ò', 'small', 'o', 'grave'),
        ('é', 'large', 'e', 'acute'),
        ('ó', 'large', 'o', 'acute'),
    ):
        if ord(char) not in cmap:
            raise ValueError(f'Missing glyph for {char}: {source_file}')
        change_accent_glyph(font, cmap[ord(char)], base, accent, kind, italic)
    update_metadata(font, style, bold, italic)
    font.recalcBBoxes = True
    font.recalcTimestamp = False
    otf_output.parent.mkdir(parents=True, exist_ok=True)
    font.flavor = None
    font.save(otf_output)

    if woff2_output is not None:
        woff2_output.parent.mkdir(parents=True, exist_ok=True)
        font.flavor = 'woff2'
        font.save(woff2_output)

    for output in [otf_output, woff2_output]:
        if output is None:
            continue
        verify = TTFont(output)
        assert verify['name'].getDebugName(1) == FAMILY
        assert verify['name'].getDebugName(9) == AUTHOR
        assert verify['name'].getDebugName(6) == f'Fonetica-{style}'
        assert all(ord(char) in verify.getBestCmap() for char in 'èòéó')
        print(f'Created: {output} ({output.stat().st_size} bytes)')


def main():
    parser = ArgumentParser(description='Build Fonetica by Davide Perillo')
    parser.add_argument('--sources', type=Path, default=DEFAULT_SOURCE,
                        help='Directory with original Atkinson Hyperlegible v1.02 OTF fonts')
    parser.add_argument('--output', type=Path, default=Path('Fonetica'))
    parser.add_argument('--no-woff2', action='store_true')
    args = parser.parse_args()
    for style, (file, bold, italic) in STYLES.items():
        build_face(
            args.sources / file,
            args.output / 'Fonts' / 'OTF' / f'Fonetica-{style}.otf',
            None if args.no_woff2 else args.output / 'Fonts' / 'WOFF2' / f'Fonetica-{style}.woff2',
            style, bold, italic)


if __name__ == '__main__':
    main()
