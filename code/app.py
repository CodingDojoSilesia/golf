import os
import logging

from difflib import unified_diff
from time import time

from flask import request, Flask, render_template, send_from_directory

from unix_colors import unix_color_to_html
from const import OUTPUTS, SITE_LANGUAGES
from exceptions import CallError
from logic import execute_cmd
from db_logic import submit_score, get_heroes
from db import db

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt='APP :: %(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask('cc-golf')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DB', 'not-found')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def render_index(**kwargs):
    return render_template(
        'index.html',
        langs=SITE_LANGUAGES,
        heroes=get_heroes(),
        **kwargs
    )


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
    nick = request.form.get('nick', '').strip()

    if lang is None:
        return '', 400

    if len(nick) not in range(1, 10 + 1):
        return '', 400

    t0 = time()
    try:
        execute_cmd(code, lang)
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
