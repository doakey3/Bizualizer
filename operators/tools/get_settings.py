import csv
from .webcolors import name_to_hex
from .hexcode_to_color import hexcode_to_color

def get_settings(csv_filepath):
    all_settings = []
    f = open(csv_filepath, 'r', encoding='utf-8')
    reader = csv.reader(f)

    table = []
    for row in reader:
        table.append([])
        for cell in row:
            table[-1].append(cell)

    headers = table[0]

    for i in range(1, len(table)):
        row_settings = {}
        for col in range(len(table[i])):
            row_settings[headers[col]] = table[i][col]

        if not 'Opacity' in row_settings:
            row_settings['Opacity'] = 1.0
        else:
            row_settings['Opacity'] = float(row_settings['Opacity'])

        if not 'Bar Color' in row_settings:
            row_settings['Bar Color'] = '#FFFFFF'
        if not row_settings['Bar Color'].startswith('#'):
            row_settings['Bar Color'] = name_to_hex(row_settings['Bar Color'])
        row_settings['Bar Color'] = hexcode_to_color(row_settings['Bar Color'])
        row_settings['Bar Color'].append(int(row_settings['Opacity'] * 255))
        row_settings['Bar Color'] = tuple(row_settings['Bar Color'])

        if not 'Bar Count' in row_settings:
            row_settings['Bar Count'] = 64
        else:
            row_settings['Bar Count'] = int(row_settings['Bar Count'])

        if not 'Bar Style' in row_settings:
            row_settings['Bar Style'] = 'bottom'

        if not 'Space Fraction' in row_settings:
            row_settings['Space Fraction'] = 0.1
        else:
            row_settings['Space Fraction'] = float(row_settings['Space Fraction'])

        if not 'Height Fraction' in row_settings:
            row_settings['Height Fraction'] = 0.25
        else:
            row_settings['Height Fraction'] = float(row_settings['Height Fraction'])

        if not 'Fade' in row_settings:
            row_settings['Fade'] = 1
        else:
            row_settings['Fade'] = bool(int(row_settings['Fade']))

        all_settings.append(row_settings)

    return all_settings