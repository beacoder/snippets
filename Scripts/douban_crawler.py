#!/usr/bin/env python

"""Minimal crawler to crawl high rated movies from movie.douban.com"""

#1 [Done]  crawl movies on douban
#2 [Done]  add delays, don't blacklisted by douban
#3 [Done]  save data into sqlite
#4 [Todo]  fix chinese character encoding problem
#5 [Todo]  push the latest movies to cell phone

import re
import requests
from collections import deque
import time
import sqlite3


# Pattern for matching douban movies
_DOUBAN_MOVIES_PATTERN = re.compile(r'href="(https?://\S+/subject/\d+/)\S*"')

_DOUBAN_MOVIE_SEED     = "https://movie.douban.com"

_CRAWLED_SITES         = set()

_HELP_STRING           ="""Usage:
start()       -> start crawling
dump_movies() -> show movies in DB"""

_db_conn               = None


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


# Follow this rule
#1 always use unicode in application
#2 encode it with 'utf-8' only when writing file/database/socket
#3 decode it with 'utf-8' when reading it back
def encode_with_utf8(in_string):
    "Convert string to utf-8 encoding."
    if isinstance(in_string, str):
        ret_string = u' '.join(in_string).encode('utf-8').strip()
    elif isinstance(in_string, unicode):
        ret_string = in_string.encode('utf-8')
    else:
        print "not a string"
    return ret_string


class _QueueAndStackBase(object):
    """Base class for Queue and Stack."""
    def __init__(self):
        self.items = deque()

    def isEmpty(self):
        return (len(self.items) == 0)

    def __iter__(self):
        return self

    def size(self):
        return len(self.items)


class Queue(_QueueAndStackBase):
    """FIFO Container."""
    def next(self):
        try:
            return self.deque()
        except IndexError:
            raise StopIteration

    def enqueue(self, item):
        self.items.append(item)

    def deque(self):
        return self.items.popleft()


class Stack(_QueueAndStackBase):
    """LIFO Container."""
    def next(self):
        try:
            return self.pop()
        except IndexError:
            raise StopIteration

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]


class DoubanMovie(object):
    """Represent a movie from movie.douban.com"""

    # Pattern for matching rating numble against douban movie
    _DOUBAN_MOVIE_RATE_PATTERN = re.compile(r'<strong class="ll rating_num" property="v:average">(.*)</strong>')

    # Pattern for matching douban movie name
    _DOUBAN_MOVIE_NAME_PATTERN    = re.compile(r'<span property="v:itemreviewed">(.*)</span>')

    # Pattern for matching year of douban movie
    _DOUBAN_MOVIE_YEAR_PATTERN    = re.compile(r'<span class="year">(.*)</span>')

    def __init__(self, text, url):
        self._movie_rate     = ""
        self._movie_name     = ""
        self._movie_year     = ""
        self._error_happened = False
        self._movie_address  = url
        self._parse_movie(text)

    def _parse_movie(self, text):
        try:
            self._movie_rate = (re.findall(DoubanMovie._DOUBAN_MOVIE_RATE_PATTERN, text))[0]
            self._movie_name = (re.findall(DoubanMovie._DOUBAN_MOVIE_NAME_PATTERN, text))[0]
            self._movie_year = (re.findall(DoubanMovie._DOUBAN_MOVIE_YEAR_PATTERN, text))[0]
        except BaseException, e:
            self._error_happened = True
            print e

    def __repr__(self):
        if not self._error_happened:
            return ("Rate of %s%s is %s \n" % (self._movie_name, self._movie_year, self._movie_rate))

    @property
    def movie_item(self):
        "Proper format to be serialized to db."
        return [encode_with_utf8(item) for item in (self._movie_name, self.movie_year, self.movie_rate, self._movie_address)]

    @property
    def movie_rate(self):
        "Get the movie rate."
        return self._movie_rate

    @property
    def movie_name(self):
        "Get the movie name."
        return self._movie_name

    @property
    def movie_year(self):
        "Get the movie year."
        return self._movie_year


# BFS stratege to do web crawling.
# @see http://stackoverflow.com/questions/20579169/dfs-vs-bfs-in-web-crawler-design
def bfs_crawl(seed):
    """Breadth First Crawling."""

    q = Queue()
    q.enqueue(seed)

    while not q.isEmpty():
        time.sleep(1)
        url = q.deque()
        rsp = requests.get(url)
        urls = set(re.findall(_DOUBAN_MOVIES_PATTERN, rsp.text))

        movie = DoubanMovie(rsp.text, url)
        save_movie(movie.movie_item)
        print(movie.__repr__())

        for url in urls:
            q.enqueue(url)
    pass


def prepare_movie_db():
    connect_db()
    if (False == bool(find_table())):
        create_table()


def start():
    bfs_crawl(_DOUBAN_MOVIE_SEED)

if __name__ == '__main__' :
    prepare_movie_db()
    print _HELP_STRING
