from cgi import escape

import re


def change_match(match):
    a, b = match.groups()
    return f'<span class="color-{a}">{b}</span>'


def unix_color_to_html(line):
    line = escape(line)
    line = line.replace(' ', '&nbsp;')
    line = re.sub('\033\[(\d+)m([^\033]+)', change_match, line)
    return line


def unixnify(filename):
    with open(filename) as f:
        return [unix_color_to_html(line) for line in f.readlines()]
