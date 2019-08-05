import os
from os.path import join as join_path
from glob import glob

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

TITLE = os.environ.get('TITLE', 'Coding Dojo Silesia Code Golf')
TASK_PATH = os.environ.get('TASK_PATH', '/tasks/helloworld')
HOWTO_PATH = join_path(TASK_PATH, 'howto')
OUTPUTS = {
    key: unixnify(join_path(HOWTO_PATH, key))
    for key in glob(join_path(HOWTO_PATH, '*'))
}
TOP_HIDE_SCORES = int(os.environ.get('TOP_HIDE_SCORES', '2'))
MAX_SCORES_ON_MAIN_PAGE = int(os.environ.get('MAX_SCORES_ON_MAIN_PAGE', '15'))
TIMEOUT = int(os.environ.get('TIMEOUT', '2'))
DASHBOARD_TOKEN = os.environ.get('DASHBOARD_TOKEN')
DATETIME_DASHBOARD_FORMAT = '%Y-%m-%d %H:%M:%S'
