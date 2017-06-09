"""Database facilities.

Sqlite used to store movies.
"""

#History#
#1 [Done] (2017-05-26) Add DB operation.
#2 [Done] (2017-06-06) Add column id in table movies.
#3 [TODO]              Use SQLAlchemy as ORM, instead of using raw sql.

# public symbols
__all__ = ["connect_db", "close_db", "find_table", "create_table",
           "find_movie", "save_movie", "dump_movies"]

from utils import *
import sqlite3


_db_conn = None


class MovieDBError(Exception):
    """Error happend when accessing movie database."""
    pass


def connect_db(db = 'movies.db'):
    global _db_conn
    assert(_db_conn is None)
    _db_conn = sqlite3.connect(db)
    _db_conn.text_factory = str


def close_db():
    global _db_conn
    assert(_db_conn is not None)
    _db_conn.close()
    _db_conn = None


def find_table(table = ('movies',)):
    assert(_db_conn is not None)
    c   = _db_conn.cursor()
    return (c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", table).fetchall())


def create_table():
    assert(False == bool(find_table()))
    _db_conn.execute('''CREATE TABLE movies (id integer, name text, year text, rate real, address text)''')
    _db_conn.commit()


# @return: list of movies or a []
def find_movie(movie):
    assert(_db_conn is not None)
    c = _db_conn.cursor()
    return (c.execute('SELECT id FROM movies WHERE id=?', (movie.movie_id, )).fetchall())


# @param movie: ('movie_name', '2017', '9.2', 'http://wwww...')
def save_movie(movie):
    assert(_db_conn is not None)
    c = _db_conn.cursor()
    c.execute('INSERT INTO movies VALUES (?,?,?,?,?)', movie)
    _db_conn.commit()


def dump_movies():
    assert(_db_conn is not None)
    c = _db_conn.cursor()
    for row in c.execute('SELECT * FROM movies ORDER BY name'):
       print row[0], decode_with_utf8(row[1]), row[2], row[3], row[4]
