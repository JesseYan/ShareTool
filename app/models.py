#!venv/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'jesse'

from app.database import Base
# import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, SmallInteger
# from sqlalchemy.orm import mapper, relationship
from app.database import db_session, metadata
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
from app import engine

from app import db


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(200))
    openid = Column(String(200))
    # test_word = Column(String(200), default="")
    # avatar_url = Column(String(200), default="")

    Base.metadata.create_all(engine)

    def __init__(self, name, email, openid):
        self.name = name
        self.email = email
        self.openid = openid
        # self.test_word = test_word
        # self.avatar_url = avatar_url

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60))
#     email = db.Column(db.String(200))
#     openid = db.Column(db.String(200))
#
#     def __init__(self, name, email, openid):
#         self.name = name
#         self.email = email
#         self.openid = openid


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     openid = db.Column(db.String(200))
#     nickname = db.Column(db.String(64))
#     email = db.Column(db.String(120))
#     # posts = db.relationship('Post', backref='author', lazy='dynamic')
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         try:
#             return unicode(self.id)  # python 2
#         except NameError:
#             return str(self.id)  # python 3
#
#     def __repr__(self):
#         return '<User %r>' % self.nickname

#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post %r>' % self.body












