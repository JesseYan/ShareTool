#!venv/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'jesse'

# from app.database import Base
# import sqlalchemy
# from sqlalchemy import Table, Column, Integer, String, SmallInteger
# from sqlalchemy.orm import mapper, relationship
from app.database import db_session, metadata
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
from app import engine

from app import db


# follower
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(200))
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(120))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    posts = db.relationship('Post',
                            backref='author',
                            lazy='dynamic')

    followed = db.relationship('User',
                               secondary=followers, # 辅助表
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    # about login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    # about follow
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # 关注者的所有文章
    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id))\
            .filter(followers.c.follower_id == self.id)\
            .order_by(Post.timestamp.desc())


# article
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body












