import os

from unix_colors import unixnify

LANGUAGES = {
    'js': ['/usr/bin/node', '-'],
    'python': ['/usr/bin/python3', '-'],
    'php': ['/usr/bin/php', '--'],
    'ruby': ['/usr/bin/ruby', '-'],
    'bash': ['/bin/bash', '-s', '--'],
}

SITE_LANGUAGES = [
    ('python', 'Python3'),
    ('ruby', 'Ruby'),
    ('bash', 'Bash'),
    ('js', 'Javascript'),
    ('php', 'PHP7'),
]

TITLE = 'Coding Dojo Silesia Code Golf Easter Holiday Edition 2019'
OUTPUTS = dict(
    help_fancy_egg=unixnify("howto/help_fancy_egg"),
    help_basic_egg=unixnify("howto/help_basic_egg"),
    help_egg=unixnify("howto/help_egg"),
    help_maskoff=unixnify("howto/help_maskoff"),
    help_zigzag=unixnify("howto/help_zigzag"),
    help_maze=unixnify("howto/help_maze"),
    help_cross=unixnify("howto/help_cross"),
    help_hstrip=unixnify("howto/help_hstrip"),
    help_vstrip=unixnify("howto/help_vstrip"),
)

TOP_HIDE_SCORES = int(os.environ.get('TOP_HIDE_SCORES', '2'))
TIMEOUT = int(os.environ.get('TIMEOUT', '2'))
