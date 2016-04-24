#!venv/bin/python
# -*- coding: UTF-8 -*-


__author__ = 'jesse'

from app import toolapp, m_login_manager, oid
# from app.models import User
from flask import url_for, g, redirect, session, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm


@toolapp.route('/')
@toolapp.route('/index/', methods=['GET', 'POST'])
def index():
    print "="*20
    with toolapp.test_request_context():
        print url_for("index")
    return "Hello, World!"


@m_login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# @oid.loginhandler
# @toolapp.route('/login', methods=['POST', 'GET'])
# def login():
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['remeber_me'] = form.remember_me.data
#         return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
#
#     return render_template('login.html',
#                            title='Sign in',
#                            form=form,
#                            providers=toolapp.config['OPENID_PROVIDERS'])

@toolapp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=toolapp.config['OPENID_PROVIDERS'])



