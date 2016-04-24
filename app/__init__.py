#!venv/bin/python

__author__ = 'jesse'

from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
import os
from config import BASE_DIR

toolapp = Flask(__name__)
toolapp.config.from_object("config")

m_login_manager = LoginManager()
m_login_manager.init_app(toolapp)
oid = OpenID(toolapp, os.path.join(BASE_DIR, 'tmp'))

from app import views
