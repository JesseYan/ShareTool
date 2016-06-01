#!venv/bin/python
# -*- coding: UTF-8 -*-


__author__ = 'jesse'

from app import toolapp, m_login_manager, oid, db
from .models import User, Post
from flask import url_for, g, redirect, session, render_template, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, EditForm, PostForm
from openid.extensions import pape
from app.database import init_db
from datetime import datetime
import config


@toolapp.route('/')
@toolapp.route('/index/', methods=['GET', 'POST'])
@toolapp.route('/index/<int:page>/', methods=['GET', 'POST'])
@login_required
def index(page=1):
    print "="*20
    with toolapp.test_request_context():
        print url_for("index")

    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=current_user)

        db.session.add(post)
        db.session.commit()
        flash('your post now is live!')

        return redirect(url_for('index'))

    posts = current_user.followed_posts().paginate(page, config.POSTS_PER_PAGE, False)
    # flash(g.user.followed_posts().all())

    # posts = g.user.followed_posts().all()
    return render_template('index.html', title='Home', form=form, posts=posts)


@toolapp.route('/login/', methods=['POST', 'GET'])
@oid.loginhandler
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


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. email is null, Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@toolapp.route('/follow/<nickname>/')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))


@toolapp.route('/unfollow/<nickname>/')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))


# @toolapp.route('/create-profile', methods=['GET', 'POST'])
# def create_profile():
#     """If this is the user's first login, the create_or_login function
#     will redirect here so that the user can set up his profile.
#     """
#     if g.user is not None or 'openid' not in session:
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         # test_word = ""
#         # avatar_url = User.avatar(128)
#
#         if not name:
#             flash(u'Error: you have to provide a name')
#         elif '@' not in email:
#             flash(u'Error: you have to enter a valid email address')
#         else:
#             flash(u'Profile successfully created')
#             # init_db()
#             db_session.add(User(name, email, session['openid']))
#             db_session.commit()
#             return redirect(oid.get_next_url())
#     return render_template('create_profile.html', next_url=oid.get_next_url())
#
#
# @toolapp.route('/profile', methods=['GET', 'POST'])
# def edit_profile():
#     """Updates a profile"""
#     if g.user is None:
#         abort(401)
#     form = dict(name=g.user.name, email=g.user.email)
#     if request.method == 'POST':
#         if 'delete' in request.form:
#             db_session.delete(g.user)
#             db_session.commit()
#             session['openid'] = None
#             flash(u'Profile deleted')
#             return redirect(url_for('index'))
#         form['name'] = request.form['name']
#         form['email'] = request.form['email']
#         # form['test_word'] = ""
#         if not form['name']:
#             flash(u'Error: you have to provide a name')
#         elif '@' not in form['email']:
#             flash(u'Error: you have to enter a valid email address')
#         else:
#             flash(u'Profile successfully created')
#             g.user.name = form['name']
#             g.user.email = form['email']
#             # g.user.test_word = form['test_word']
#             db_session.commit()
#             return redirect(url_for('edit_profile'))
#     return render_template('edit_profile.html', form=form)


@toolapp.route('/logout')
def logout():
    logout_user()
    flash(u'You have been signed out')
    return redirect(url_for('index'))
    # session.pop('openid', None)
    # flash(u'You have been signed out')
    # # return redirect(oid.get_next_url())
    # return redirect(url_for('index'))


@toolapp.before_request
def before_request():
    g.user = current_user
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()

    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@toolapp.after_request
def after_request(response):
    db.session.remove()
    return response


@m_login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


@toolapp.route("/user/<nickname>/")
@toolapp.route("/user/<nickname>/<int:page>/")
@login_required
def user(nickname, page=1):
    query_user = User.query.filter_by(nickname=nickname).first()
    if query_user is None:
        flash("User: " + nickname + ' Not Found')
        return redirect(url_for('index'))

    # posts = [
    #     {'author': query_user, 'body': 'Test post #1'},
    #     {'author': query_user, 'body': 'Test post #2'}]
    posts = query_user.posts.paginate(page=page, per_page=config.POSTS_PER_PAGE, error_out=False)
    return render_template('user.html', user=query_user, posts=posts)


@toolapp.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit_profile.html', form=form)









