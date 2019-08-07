from os.path import join as join_path
from os import environ


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

TITLE = environ.get('TITLE', 'Coding Dojo Silesia Code Golf')
TASK_PATH = environ.get('TASK_PATH', '/tasks/helloworld')
TASK_MODULE_PATH = join_path(TASK_PATH, 'task.py')
TOP_HIDE_SCORES = int(environ.get('TOP_HIDE_SCORES', '2'))
MAX_SCORES_ON_MAIN_PAGE = int(environ.get('MAX_SCORES_ON_MAIN_PAGE', '15'))
TIMEOUT = int(environ.get('TIMEOUT', '2'))
DASHBOARD_TOKEN = environ.get('DASHBOARD_TOKEN')
DATETIME_DASHBOARD_FORMAT = '%Y-%m-%d %H:%M:%S'
