#!venv/bin/python

__author__ = 'jesse'

from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
import os
from config import basedir
from flask_sqlalchemy import SQLAlchemy


toolapp = Flask(__name__)
toolapp.config.from_object("config")

m_login_manager = LoginManager()
m_login_manager.init_app(toolapp)
m_login_manager.login_view = 'login'
oid = OpenID(toolapp, os.path.join(basedir, 'tmp'))

db = SQLAlchemy(toolapp)

from app import views, models
