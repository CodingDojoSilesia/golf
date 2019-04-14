from logging import getLogger

from const import TOP_HIDE_SCORES
from db import db, Hero

logger = getLogger('app')


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


def submit_score(nick, lang, code, seconds=0.0):
    hero = Hero.query.filter_by(nick=nick).first()
    new_score = len(code)
    if hero is None:
        old_score = '-'
        hero = Hero(nick, lang, new_score)
    else:
        old_score = hero.score
        if old_score < new_score:
            logger.warning(
                'Worse Record[%r, %s] in %0.2f seconds, from %s to %s',
                nick, lang, seconds, old_score, new_score,
            )
            return
        hero.score = new_score
        hero.lang = lang

    logger.info(
        'New Record[%r, %s] in %0.2f seconds, from %s to %s',
        nick, lang, seconds, old_score, new_score,
    )

    db.session.add(hero)
    db.session.commit()