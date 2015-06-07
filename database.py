__author__ = 'Antah'
import bcrypt
import ochrona
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)

class User(ochrona.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    pw_hash = Column(String(120))
    question = Column(String(120))
    answer = Column(String(120))

    def __init__(self, username, password, question, answer):
        self.username = username
        self.set_password(password)
        self.question = question
        self.set_answer(answer)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.pw_hash = bcrypt.hashpw(password, salt)

    def check_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), self.pw_hash.encode('utf-8')) == self.pw_hash.encode('utf-8')

    def set_answer(self, answer):
        salt = bcrypt.gensalt()
        self.answer = bcrypt.hashpw(answer, salt)

    def check_answer(self, answer):
        return bcrypt.hashpw(answer.encode('utf-8'), self.answer.encode('utf-8')) == self.answer.encode('utf-8')