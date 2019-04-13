import os
import logging
from functools import wraps
from datetime import datetime

from difflib import unified_diff
from time import time

from flask import request, Flask, render_template, send_from_directory

from unix_colors import unix_color_to_html
from const import OUTPUTS, SITE_LANGUAGES, TITLE
from exceptions import CallError
from logic import execute_cmd
from db_logic import submit_score, get_heroes
from db import db

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="APP :: %(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask("cc-golf")

GOLF_DATE_FORMAT = "%Y-%m-%d"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB", "not-found")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def render_index(**kwargs):
    return render_template(
        "index.html", title=TITLE, langs=SITE_LANGUAGES, heroes=get_heroes(), **kwargs
    )


def date_restricted(f):
    """Restricting endpoints based on date of event.

    Decorator takes into account two envs START_DATE and END_DATE,
    both in ISO format or in Python's datetime nomenclature module "%Y-%m-%d".

    If envs do not exist there is no restriction.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        def parse_date(str_date):
            try:
                return datetime.strptime(str_date, GOLF_DATE_FORMAT)
            except (TypeError, ValueError):
                return None

        today = datetime.today()
        start_date = parse_date(os.environ.get("START_DATE"))
        end_date = parse_date(os.environ.get("END_DATE"))

        if start_date and start_date > today:
            return render_template(
                "not_today.html",
                reason=f"Golf has not started yet. Please come back on {start_date.strftime(GOLF_DATE_FORMAT)}.",
            )

        if end_date and end_date < today:
            return render_template(
                "not_today.html",
                reason=f"Golf has finished on {end_date.strftime(GOLF_DATE_FORMAT)}.",
            )

        return f(*args, **kwargs)

    return wrapped


@app.route("/stats/<path:path>")
@date_restricted
def stats(path):
    return send_from_directory("stats", path)


@app.route("/", methods=["GET"])
@date_restricted
def show_me_what_you_got():
    return render_index()


@app.route("/howto")
@date_restricted
def readme_dude():
    return render_template("howto.html", title=TITLE, **OUTPUTS)


@app.route("/", methods=["POST"])
@date_restricted
def execute_order_66():
    code = request.form.get("code", "").replace("\r\n", "\n")
    lang = request.form.get("lang", "")
    nick = request.form.get("nick", "").strip()

    if lang is None:
        return "", 400

    if len(nick) not in range(1, 10 + 1):
        return "", 400

    t0 = time()
    try:
        execute_cmd(code, lang)
    except CallError as exp:
        diff_time = time() - t0
        err = exp
        diff = list(
            unified_diff(
                err.wrong.splitlines(True),
                err.correct.splitlines(True),
                fromfile="your output",
                tofile="args: {}".format(exp.args),
            )
        )
        err_lines = err.error.splitlines(True)
        logger.warning(
            "Fail[%r, %s] in %0.2f seconds, args: %r", nick, lang, diff_time, exp.args
        )
        return (
            render_index(
                code=code,
                lang=lang,
                nick=nick,
                is_done=False,
                err=err,
                diff=[unix_color_to_html(line) for line in diff],
                error_output=[unix_color_to_html(line) for line in err_lines],
            ),
            400,
        )

    diff_time = time() - t0
    submit_score(nick, lang, code, diff_time)
    return render_index(code=code, lang=lang, nick=nick, is_done=True)
