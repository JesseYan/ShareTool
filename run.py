#!venv/bin/python

__author__ = 'jesse'


from app import toolapp
from app.database import init_db


init_db()
toolapp.run(debug=True)
