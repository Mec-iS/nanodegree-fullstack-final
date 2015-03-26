__author__ = 'lorenzo'

from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


def create_sqlite_file(eng):
    """Create and sql lite file"""
    Base.metadata.create_all(eng)


def start_session(eng):
    """This method starts an SQLAlchemy session"""
    Base.metadata.bind = eng
    DBSession = sessionmaker(bind=eng)
    session = DBSession()
    return session

'''Configuration'''
engine = create_engine(
    r'sqlite:///C:\Github\restaurantmenu.db'
)
'''End Configuration'''