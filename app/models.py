#!venv/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'jesse'

from app.database import Base
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, SmallInteger
from sqlalchemy.orm import mapper, relationship
from app.database import db_session, metadata


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=True)
#     email = Column(String(120), unique=True)
#
#     def __init__(self, name=None, email=None):
#         self.name = name
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % (self.name)

# class User(object):
#     query = db_session.query_property()
#
#     def __init__(self, name=None, email=None):
#         self.name = name
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % (self.name)
#
#
# users = Table('users', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(50), unique=True),
#     Column('email', String(120), unique=True)
# )
# mapper(User, users)

class User(Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    role = Column(SmallInteger)
    posts = relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)












