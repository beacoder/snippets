"""Database facilities.

Sqlite used to store movies.
"""

#History#
#1 [DONE] (2017-05-26) Add DB operation.
#2 [DONE] (2017-06-06) Add column id in table movies.
#3 [DONE] (2017-06-13) Use SQLAlchemy as ORM, instead of using raw sql.
#4 [DONE] (2017-06-15) Fix encoding error when save movie to db

# public symbols
__all__ = ["Movie", "connect_db", "close_db", "find_movie",
           "save_movie", "dump_movies"]

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float


Base       = declarative_base()
Session    = sessionmaker()


class Movie(Base):
    __tablename__ = 'movies'

    id       = Column(Integer, primary_key=True)
    name     = Column(String(50))
    year     = Column(String(50))
    rate     = Column(Float)
    address  = Column(String(50))

    def __repr__(self):
        return "<Moive(name='%s', year='%s', rate='%s', address='%s')>" % (
            self.name, self.year, self.rate, self.address)
    pass


def connect_db():
    global Session
    engine = create_engine('sqlite:///movies.db')
    Base.metadata.create_all(engine)
    Session.configure(bind = engine)
    pass


def close_db():
    session = Session()
    session.close()
    pass


def find_movie(movie):
    return Session().query(Movie.id).filter(Movie.id == movie.id).first()


def save_movie(movie):
    session = Session()
    session.add(movie)
    session.commit()
    pass


def dump_movies():
    session = Session()
    for movie in session.query(Movie).order_by(Movie.id):
        print(movie.__repr__())
    pass
