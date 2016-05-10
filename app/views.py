#!venv/bin/python
# -*- coding: UTF-8 -*-


__author__ = 'jesse'

from app import toolapp, m_login_manager, oid, db, db_session
from .models import User
from flask import url_for, g, redirect, session, render_template, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from openid.extensions import pape
from app.database import init_db


@toolapp.route('/')
@toolapp.route('/index/', methods=['GET', 'POST'])
# @login_required
def index():
    print "="*20
    with toolapp.test_request_context():
        print url_for("index")
    # user = g.user
    # posts = [
    #     {
    #         'author': {'nickname': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'nickname': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    # return render_template('index.html', title='Home', user=user, posts=posts)
    return render_template('index.html')


@toolapp.route('/login/', methods=['POST', 'GET'])
@oid.loginhandler
def login():
    # if g.user is not None and g.user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     session['remeber_me'] = form.remember_me.data
    #     print '-------try_login openid data'
    #     return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    #
    # return render_template('login.html',
    #                        title='Sign in',
    #                        form=form,
    #                        providers=toolapp.config['OPENID_PROVIDERS'])
    """Does the login via OpenID.  Has to call into `oid.try_login`
    to start the OpenID machinery.
    """
    # # if we are already logged in, go back to were we came from
    if g.user is not None:
        return redirect(oid.get_next_url())

    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            pape_req = pape.Request([])
            return oid.try_login(openid, ask_for=['email', 'nickname'],
                                         ask_for_optional=['fullname'],
                                         extensions=[pape_req])

    return render_template('login.html', next=oid.get_next_url(), error=oid.fetch_error())


@oid.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
    necessary to figure out if this is the users's first login or not.
    This function has to redirect otherwise the user will be presented
    with a terrible URL which we certainly don't want.
    """
    print '***************'
    session['openid'] = resp.identity_url
    if 'pape' in resp.extensions:
        pape_resp = resp.extensions['pape']
        session['auth_time'] = pape_resp.auth_time
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile',
                            next=oid.get_next_url(),
                            name=resp.fullname or resp.nickname,
                            email=resp.email))


@toolapp.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """If this is the user's first login, the create_or_login function
    will redirect here so that the user can set up his profile.
    """
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # test_word = ""
        # avatar_url = request.form['avatar_url']

        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            # init_db()
            db_session.add(User(name, email, session['openid']))
            db_session.commit()
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url())


@toolapp.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    """Updates a profile"""
    if g.user is None:
        abort(401)
    form = dict(name=g.user.name, email=g.user.email)
    if request.method == 'POST':
        if 'delete' in request.form:
            db_session.delete(g.user)
            db_session.commit()
            session['openid'] = None
            flash(u'Profile deleted')
            return redirect(url_for('index'))
        form['name'] = request.form['name']
        form['email'] = request.form['email']
        # form['test_word'] = ""
        if not form['name']:
            flash(u'Error: you have to provide a name')
        elif '@' not in form['email']:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            g.user.name = form['name']
            g.user.email = form['email']
            # g.user.test_word = form['test_word']
            db_session.commit()
            return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', form=form)


@toolapp.route('/logout')
def logout():
    # logout_user()
    # return redirect(url_for('index'))
    session.pop('openid', None)
    flash(u'You have been signed out')
    # return redirect(oid.get_next_url())
    return redirect(url_for('index'))


@toolapp.before_request
def before_request():
    g.user = None
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()


@toolapp.after_request
def after_request(response):
    db_session.remove()
    return response

#
# @m_login_manager.user_loader
# def load_user(uid):
#     return User.query.get(int(uid))


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

# @oid.after_login
# def after_login(resp):
#     # print '============after login11111111111'
#     # if resp.email is None or resp.email == "":
#     #     flash('Invalid login. Please try again.')
#     #     return redirect(url_for('login'))
#     # user = User.query.filter_by(email=resp.email).first()
#     # if user is None:
#     #     nickname = resp.nickname
#     #     if nickname is None or nickname == "":
#     #         nickname = resp.email.split('@')[0]
#     #     user = User(nickname=nickname, email=resp.email)
#     #     db.session.add(user)
#     #     db.session.commit()
#     # remember_me = False
#     # if 'remember_me' in session:
#     #     remember_me = session['remember_me']
#     #     session.pop('remember_me', None)
#     # login_user(user, remember=remember_me)
#     # print '============after login'
#     # return redirect(request.args.get('next') or url_for('index'))
#     """This is called when login with OpenID succeeded and it's not
#     necessary to figure out if this is the users's first login or not.
#     This function has to redirect otherwise the user will be presented
#     with a terrible URL which we certainly don't want.
#     """
#     session['openid'] = resp.identity_url
#     print '********after login------'
#     if 'pape' in resp.extensions:
#         pape_resp = resp.extensions['pape']
#         session['auth_time'] = pape_resp.auth_time
#     user = User.query.filter_by(openid=resp.identity_url).first()
#     if user is not None:
#         flash(u'Successfully signed in')
#         g.user = user
#         return redirect(oid.get_next_url())
#     return redirect(url_for('create_profile',
#                             next=oid.get_next_url(),
#                             name=resp.fullname or resp.nickname,
#                             email=resp.email))


#
# @toolapp.route("/user/<nickname>/")
# @login_required
# def user(nickname):
#     query_user = User.query.filter_by(nickname=nickname).first()
#     if query_user is None:
#         flash("User: " + nickname + ' Not Found')
#         return redirect(url_for('index'))
#
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}]
#     return render_template('user.html', user=user, posts=posts)








