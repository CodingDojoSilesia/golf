from flask import request, Flask, render_template, send_from_directory
from subprocess import Popen, PIPE, TimeoutExpired
from itertools import product
from difflib import unified_diff
from random import sample
from itertools import product
from time import time

import os
import logging

from unix_colors import unix_color_to_html, unixnify
from cc import do_it
from db import db, Hero

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

app = Flask('cc-golf')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DB', 'not-found')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

TOP_HIDE_SCORES = int(os.environ.get('TOP_HIDE_SCORES', '2'))
TIMEOUT = int(os.environ.get('TIMEOUT', '2'))


def make_arguments():
    ww = sample(range(18, 100, 2), 4)
    hh = sample(range(14, 100, 2), 4)
    texts = [
        'for you!', 'xxx',  'x' * 30, 'y' * 30,
        'coding-dojo-silesia' * 5, '---___---',
        '(╯°□°╯) ┻━┻', '┻━┻ \(`Д´)/ ┻━┻',
        'for firemark!', 'aaa',  ' ' * 30, '...' * 10,
    ]
    tt = sample(texts, 4)

    return product(tt, ww, hh)


CHECK_FUNC = do_it

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


class CallError(Exception):

    def __init__(self, *, wrong='', correct='', err='', args=None):
        self.wrong = wrong
        self.correct = correct
        self.error = err
        self.args = args or []


def render_index(**kwargs):
    return render_template(
        'index.html',
        langs=SITE_LANGUAGES,
        heroes=get_heroes(),
        **kwargs
    )


def get_heroes():
    scores = list(
        Hero.query
        .order_by(Hero.score)
        .limit(15)
        .all()
    )
    for hero in scores[0:TOP_HIDE_SCORES]:
        hero.score = '???'
    return scores + [Hero('-', '-')] * (15 - len(scores))


@app.route('/stats/<path:path>')
def stats(path):
    return send_from_directory('stats', path)


@app.route('/', methods=['GET'])
def show_me_what_you_got():
    return render_index()


@app.route('/howto')
def readme_dude():
    return render_template('howto.html', **OUTPUTS)


@app.route('/', methods=['POST'])
def execute_order_66():
    code = request.form.get('code', '').replace('\r\n', '\n')
    lang = request.form.get('lang', '')
    nick = request.form.get('nick', '')
    cmd = LANGUAGES.get(lang)

    if cmd is None:
        return '', 400

    t0 = time()
    try:
        execute_cmd(code, cmd)
    except CallError as exp:
        diff_time = time() - t0
        err = exp
        diff = list(unified_diff(
            err.wrong.splitlines(True),
            err.correct.splitlines(True),
            fromfile='your output',
            tofile='args: {}'.format(exp.args),
        ))
        err_lines = err.error.splitlines(True)
        logger.warning('Fail[%r, %s] in %0.2f seconds, args: %r', nick, lang, diff_time, exp.args)
        return render_index(
            code=code, lang=lang, nick=nick, is_done=False,
            err=err,
            diff=[unix_color_to_html(line) for line in diff],
            error_output=[unix_color_to_html(line) for line in err_lines],
        ), 400

    diff_time = time() - t0
    submit_score(nick, lang, code, diff_time)
    return render_index(code=code, lang=lang, nick=nick, is_done=True)


def submit_score(nick, lang, code, seconds=0.0):
    hero = Hero.query.filter_by(nick=nick, lang=lang).first()
    score = len(code)
    if hero is None:
        old_score = '-'
        hero = Hero(nick, lang, score)
    else:
        old_score = hero.score
        hero.score = min(old_score, score)

    logger.info(
        'New Record[%r, %s] in %0.2f seconds, from %s to %s',
        nick, lang, seconds, old_score, score,
    )

    db.session.add(hero)
    db.session.commit()


def execute_cmd(code, cmd):
    args_list = make_arguments()
    for args in args_list:
        assert_call(cmd, code, args)


def decode_output(output):
    if not output:
        return ''
    return output.decode('utf-8', errors='replace')


def assert_call(cmd_args, code, args):
    cmd_args = cmd_args + [str(arg) for arg in args]
    cmd_args = [
        'nsjail',
        '-Mo',
        '--user', '4242',
        '--group', '4242',
        '--chroot', '/',
        '--cgroup_cpu_ms_per_sec', '100',
        '--cgroup_pids_max', '64',
        '--cgroup_mem_max', '67108864',
        '--rlimit_as=max',
        '--disable_clone_newcgroup',
        '--disable_proc',
        '--iface_no_lo',
        '-Q',
        '--',
    ] + cmd_args
    correct = CHECK_FUNC(*args)

    process = None
    try:
        process = Popen(
            args=cmd_args,
            stdin=PIPE, stdout=PIPE, stderr=PIPE,
            env={'PYTHONIOENCODING': 'UTF-8'},
        )
        output, err_output = process.communicate(code.encode('utf-8'), timeout=TIMEOUT)
    except TimeoutExpired as exp:
        raise CallError(err='timeout :(', args=args)
    except Exception as exp:
        logger.exception('!!!')
        raise CallError(err='something is wrong: %s' % exp, args=args)
    finally:
        if process is not None:
            process.kill()

    output = decode_output(output)
    err_output = decode_output(err_output)

    if process.returncode != 0 or output != correct:
        raise CallError(
            wrong=output,
            correct=correct,
            err=err_output,
            args=args,
        )
