#!venv/bin/python

__author__ = 'jesse'

from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
import os
from config import basedir
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_mail import Mail
from momentjs import momentjs


toolapp = Flask(__name__)
toolapp.config.from_object("config")

m_login_manager = LoginManager()
m_login_manager.init_app(toolapp)
m_login_manager.login_view = 'login'
oid = OpenID(toolapp, os.path.join(basedir, 'tmp'))

db = SQLAlchemy(toolapp)

engine = create_engine(toolapp.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

mail = Mail(toolapp)

# set jinja-momentjs = my momentjs
toolapp.jinja_env.globals['momentjs'] = momentjs

from app import views, models
