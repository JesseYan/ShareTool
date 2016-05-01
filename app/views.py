#!venv/bin/python
# -*- coding: UTF-8 -*-


__author__ = 'jesse'

from app import toolapp, m_login_manager, oid, db
from .models import User
from flask import url_for, g, redirect, session, render_template, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm


@toolapp.route('/')
@toolapp.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    print "="*20
    with toolapp.test_request_context():
        print url_for("index")
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@oid.loginhandler
@toolapp.route('/login/', methods=['POST', 'GET'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remeber_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    return render_template('login.html',
                           title='Sign in',
                           form=form,
                           providers=toolapp.config['OPENID_PROVIDERS'])


@toolapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@toolapp.before_request
def before_request():
    g.user = current_user


@m_login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# @toolapp.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#         return redirect('/index')
#     return render_template('login.html',
#                            title='Sign In',
#                            form=form,
#                            providers=toolapp.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))





