import os
import csv
from .webcolors import name_to_hex

def check_config(path):
    """Checks the config file to see if it is valid"""
    folder_path = os.path.dirname(path)

    f = open(path, 'r', encoding='utf-8')
    reader = csv.reader(f)
    
    table = []
    for row in reader:
        table.append([])
        for cell in row:
            table[-1].append(cell)
    headers = table[0]
    allowed_images = ['.jpg', '.png']
    
    for row in range(1, len(table)):
        settings = {}
        for col in range(len(table[row])):
            settings[headers[col]] = table[row][col]

        if (not 'Song' in settings or 
                settings['Song'].rstrip() == '' or 
                not settings['Song'].endswith('.mp3') or
                not os.path.isfile(os.path.join(folder_path, settings['Song']))):
            return "Config file row " + str(row + 1) + " has an invalid song path"
            
        if (not 'Background' in settings or not 
                os.path.isfile(os.path.join(folder_path, settings['Background'])) or 
                os.path.splitext(settings['Background'])[1] not in allowed_images):

            return "Config file row " + str(row + 1) + " has invalid background path"
        
        if 'Bar Color' in settings:
            try:
                name_to_hex(settings['Bar Color'])
            except ValueError:
                if not settings['Bar Color'].startswith('#'):
                    return "Config file row " + str(row + 1) + ": Bar Color must be valid hexcode (starts with '#')"
                if len(settings['Bar Color'][1::]) > 6 or len(settings['Bar Color'][1::]) % 2 != 0:
                    return "Config file row " + str(row + 1) + ": Bar Color must be valid hexcode ('#' + <= to 6 alphanumerics)"
                if not settings['Bar Color'][1::].isalnum():
                    return "Config file row " + str(row + 1) + ": Bar Color must be valid hexcode (alpha numeric)"
        
        if 'Bar Count' in settings:
            try:
                test = int(settings['Bar Count'])
            except ValueError:
                return "Config file row " + str(row + 1) + ": Bar Count must be an integer"
        
        if 'Bar Style' in settings:
            allowed_styles = ['bottom', 'top', 'top-bottom', 'left', 
                              'right', 'left-right', 
                              'horizontal-center', 'vertical-center']
            if not settings['Bar Style'] in allowed_styles:
                return "Config file row " + str(row + 1) + ": Invalid style.\nValid Styles: bottom, top, top-bottom,\nleft, right, left-right, horizontal-center, vertical-center"
        
        if 'Space Fraction' in settings:
            try:
                test = float(settings['Space Fraction'])
                if test < 0 or test > 1:
                    return "Config file row " + str(row + 1) + ": Space Fraction must be a number between 0 & 1"
            except ValueError:
                return "Config file row " + str(row + 1) + ": Space Fraction must be a number between 0 & 1"
        if 'Height Fraction' in settings:
            try:
                test = float(settings['Height Fraction'])
                if test < 0 or test > 1:
                    return "Config file row " + str(row + 1) + ": Height Fraction must be a number between 0 & 1"
            except ValueError:
                return "Config file row " + str(row + 1) + ": Height Fraction must be a number between 0 & 1"
                
        if 'Fade' in settings:
            try:
                test = bool(int(settings['Fade']))
            except ValueError:
                return "Config file row " + str(row + 1) + ": Fade value must be either 0 or 1"
        
        if 'Opacity' in settings:
            try:
                test = float(settings['Opacity'])
                if test < 0 or test > 1:
                    return "Config file row " + str(row + 1) + ": Opacity must be a number between 0 & 1"
            except ValueError:
                return "Config file row " + str(row + 1) + ": Opacity must be a number between 0 & 1"

    return ''
