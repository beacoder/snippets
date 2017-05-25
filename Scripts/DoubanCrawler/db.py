"""Database facilities.

Sqlite used to store movies.
"""

#1 [Todo]   Each DB could have only one connection available

# public symbols
__all__ = ["connect_db", "close_db", "find_table", "create_table",
           "find_movie", "save_movie", "dump_movies"]

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
    _db_conn.execute('''CREATE TABLE movies (name text, year text, rate real, address text)''')
    _db_conn.commit()


# @return: list of movies or a []
def find_movie(movie_name):
    assert(_db_conn is not None)
    c = _db_conn.cursor()
    return c.execute('SELECT * FROM movies WHERE name=?', name).fetchall()


# @param movie: ('movie_name', '2017', '9.2', 'http://wwww...')
def save_movie(movie):
    assert(_db_conn is not None)
    c = _db_conn.cursor()
    c.execute('INSERT INTO movies VALUES (?,?,?,?)', movie)
    _db_conn.commit()


def dump_movies():
    assert(_db_conn is not None)
    c = _db_conn.cursor()
    for row in c.execute('SELECT * FROM movies ORDER BY name'):
       print row[0].decode('utf-8'), row[1], row[2], row[3]
