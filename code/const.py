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

OUTPUTS = dict(
    help1=unixnify("howto/help1"),
    help_text1=unixnify("howto/help_text1"),
    help_text2=unixnify("howto/help_text2"),
    help_width1=unixnify("howto/help_width1"),
    help_width2=unixnify("howto/help_width2"),
    help_height1=unixnify("howto/help_height1"),
    help_height2=unixnify("howto/help_height2"),
)

TOP_HIDE_SCORES = int(os.environ.get('TOP_HIDE_SCORES', '2'))
TIMEOUT = int(os.environ.get('TIMEOUT', '2'))
