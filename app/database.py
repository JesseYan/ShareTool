#!venv/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'jesse'

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import toolapp

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import app.models
    Base.metadata.create_all(bind=engine)


@toolapp.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()




