from sqlalchemy import Column, Integer, String, Index

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'heroes'
    __table_args__ = (Index('nick', 'lang'),)

    nick = Column(String, primary_key=True)
    lang = Column(String)
    score = Column(Integer)

    def __init__(self, nick, lang, score=0):
        self.nick = nick
        self.lang = lang
        self.score = score
