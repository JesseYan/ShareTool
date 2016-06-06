#!venv/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'jesse'

from app.models import Post
from app import db
for post in Post.query.all():
    db.session.delete(post)
    db.session.commit()
