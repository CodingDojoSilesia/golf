from flask import request, Flask, render_template, send_from_directory
from subprocess import Popen, PIPE, TimeoutExpired
from itertools import product
from difflib import unified_diff
from random import sample

import os

from unix_colors import unix_color_to_html, unixnify
from cc import do_it
from db import db, Hero

app = Flask('cc-golf')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DB', 'not-found')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

LANGUAGES = {
    'js': ['node', '-'],
    'python': ['python3', '-'],
    'php': ['php5', '--'],
}

SITE_LANGUAGES = [
    ('python', 'Python'),
    ('js', 'Javascript'),
    ('php', 'PHP'),
]


OUTPUTS = dict(
    colors=unixnify("howto/colors"),
    help1=unixnify("howto/help1"),
    help2=unixnify("howto/help2"),
    help3=unixnify("howto/help3"),
    help4=unixnify("howto/help4"),
    help5=unixnify("howto/help5"),
    help6=unixnify("howto/help6"),
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
        scores=[
            (lang, get_scores_by_lang(key))
            for key, lang in SITE_LANGUAGES
        ],
        **kwargs
    )


def get_scores_by_lang(lang):
    scores = list(
        Hero.query
        .filter_by(lang=lang)
        .order_by(Hero.score)
        .limit(5)
        .all()
    )
    return scores + [Hero('-', lang)] * (5 - len(scores))


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
    code = request.form.get('code', '')
    lang = request.form.get('lang', '')
    nick = request.form.get('nick', '')
    cmd = LANGUAGES.get(lang)

    if cmd is None:
        return '', 400

    try:
        execute_cmd(code, cmd)
    except CallError as exp:
        err = exp
        diff = list(unified_diff(
            err.wrong.splitlines(True),
            err.correct.splitlines(True),
            fromfile='your output',
            tofile='args: {}'.format(exp.args),
        ))
        err_lines = err.error.splitlines(True)
        return render_index(
            code=code, lang=lang, nick=nick, is_done=False,
            err=err,
            diff=[unix_color_to_html(line) for line in diff],
            error_output=[unix_color_to_html(line) for line in err_lines],
        )

    submit_score(nick, lang, code)
    return render_index(code=code, lang=lang, nick=nick, is_done=True)


def submit_score(nick, lang, code):
    hero = Hero.query.filter_by(nick=nick, lang=lang).first()
    score = len(code)
    if hero is None:
        hero = Hero(nick, lang, score)
    else:
        hero.score = min(hero.score, score)

    db.session.add(hero)
    db.session.commit()


def execute_cmd(code, cmd):
    ww = sample(range(18, 50, 2), 4)
    hh = sample(range(14, 50, 2), 4)

    for text in ['for you!', 'xxx',  'x' * 50]:
        for width in ww:
            for height in hh:
                assert_call(cmd, code, (text, width, height))


def decode_output(output):
    if not output:
        return ''
    return output.decode('utf-8', errors='replace')


def preexec_fn():
    os.setgid(4242)
    os.setuid(4242)


def assert_call(cmd_args, code, args):
    cmd_args = cmd_args + [str(arg) for arg in args]
    correct = do_it(*args)

    process = None
    try:
        process = Popen(
            args=cmd_args,
            stdin=PIPE, stdout=PIPE, stderr=PIPE,
            env={'PYTHONIOENCODING': 'UTF-8'},
            preexec_fn=preexec_fn,
        )
        output, err_output = process.communicate(code.encode(), timeout=2)
    except TimeoutExpired as exp:
        raise CallError(err='timeout :(', args=args)
    except Exception as exp:
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
