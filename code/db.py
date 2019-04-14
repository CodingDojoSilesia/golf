from sqlalchemy import (
    Column, Integer, String, DateTime, Float,
    Boolean, PrimaryKeyConstraint, Index,
)
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def make_time_column():
    return Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class Hero(db.Model):
    __tablename__ = 'heroes'
    __table_args__ = (
        PrimaryKeyConstraint('nick', 'lang', name='hero_key'),
        Index('hero_nick_key', 'nick'),
        Index('hero_lang_key', 'lang'),
    )

    nick = Column(String, nullable=False)
    lang = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    time = make_time_column()

    def __init__(self, nick, lang, score=0):
        self.nick = nick
        self.lang = lang
        self.score = score


class ScoreLog(db.Model):
    __tablename__ = 'score_logs'
    __table_args__ = (
        Index('score_logs_nick_key', 'nick'),
        Index('score_logs_lang_key', 'lang'),
    )

    pk = Column(Integer, primary_key=True)
    nick = Column(String, nullable=False)
    lang = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    execution_time = Column(Float, nullable=False)
    fail = Column(Boolean, nullable=False)
    time = make_time_column()

    def __init__(self, nick, lang, fail, execution_time, score):
        self.nick = nick
        self.lang = lang
        self.score = score
        self.fail = fail
        self.execution_time = execution_time
