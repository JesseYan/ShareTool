#!venv/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'jesse'

from flask.ext.mail import Message
from flask import render_template
from app import mail
from config import ADMINS
from app import toolapp
from threading import Thread
from .decorators import async


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     # mail.send(msg)
#     thr = Thread(target=send_async_email, args=[toolapp, msg])
#     thr.start()


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(toolapp, msg)


def follower_notification(followed, follower):
    print '='*10, 'email', '='*10
    print 'recipients:', followed.email
    send_email(subject="[microblog] %s is now following you!" % follower.nickname,
               sender=ADMINS[0],
               recipients=[followed.email],
               text_body=render_template("follower_email.txt", user=followed, follower=follower),
               html_body=render_template("follower_email.html", user=followed, follower=follower))



