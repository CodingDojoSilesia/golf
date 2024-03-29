from cgi import escape

import re


def change_match(match):
    raw_colors, content = match.groups()
    colors = (color.strip() for color in raw_colors.split(';'))
    classes = ['color-%s' % color for color in colors if color]
    return '<span class="{}">{}</span>'.format(' '.join(classes), content)


def unix_color_to_html(line):
    line = escape(line)
    line = re.sub('\033\[([\d;]+)m([^\033]+)', change_match, line)
    return line


def unixnify(filename):
    with open(filename, 'rb') as f:
        return [
            unix_color_to_html(line.decode('UTF-8')) 
            for line in f.readlines()
        ]
