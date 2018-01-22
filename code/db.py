from sqlalchemy import Column, Integer, String, UniqueConstraint, Index

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'heroes'
    __table_args__ = (
        UniqueConstraint('nick', 'lang', name='hero_key'),
        Index('hero_nick_key', 'nick'),
        Index('hero_lang_key', 'lang'),
    )

    nick = Column(String)
    lang = Column(String)
    score = Column(Integer)

    def __init__(self, nick, lang, score=0):
        self.nick = nick
        self.lang = lang
        self.score = score
