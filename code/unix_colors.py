from cgi import escape

import re


def change_match(match):
    a, b = match.groups()
    return '<span class="color-{}">{}</span>'.format(a, b)


def unix_color_to_html(line):
    line = escape(line)
    line = line.replace(' ', '&nbsp;')
    line = re.sub('\033\[(\d+)m([^\033]+)', change_match, line)
    return line


def unixnify(filename):
    with open(filename, 'rb') as f:
        return [unix_color_to_html(line.decode('UTF-8')) for line in f.readlines()]
