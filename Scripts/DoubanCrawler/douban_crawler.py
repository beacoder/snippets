#!/usr/bin/env python

"""Minimal crawler to crawl high rated movies from movie.douban.com"""

#History#
#1 [Done] (2017-05-18) crawl movies on douban
#2 [Done] (2017-05-23) add delays, don't blacklisted by douban
#3 [Done] (2017-05-25) save data into sqlite
#4 [Done] (2017-05-25) fix chinese character encoding problem
#5 [Done] (2017-06-06) only save movies which doesn't exist in DB
#6 [Todo]              push the latest movies to cell phone
#7 [Todo]              add logging to log errors

from utils import *
from db import *

import re
import requests
import time


# Pattern for matching douban movies
_DOUBAN_MOVIES_PATTERN = re.compile(r'href="(https?://\S+/subject/\d+/)\S*"')

_DOUBAN_MOVIE_SEED     = "https://movie.douban.com"

_CRAWLED_SITES         = set()

_HELP_STRING           ="""Usage:
start()       -> start crawling
dump_movies() -> show movies in DB"""


class DoubanMovie(object):
    """Represent a movie from movie.douban.com"""

    # Pattern for matching rating numble against douban movie
    _DOUBAN_MOVIE_RATE_PATTERN = re.compile(r'<strong class="ll rating_num" property="v:average">(.*)</strong>')

    # Pattern for matching douban movie name
    _DOUBAN_MOVIE_NAME_PATTERN    = re.compile(r'<span property="v:itemreviewed">(.*)</span>')

    # Pattern for matching year of douban movie
    _DOUBAN_MOVIE_YEAR_PATTERN    = re.compile(r'<span class="year">(.*)</span>')

    # Pattern for matching id of douban movie
    _DOUBAN_MOVIE_ID_PATTERN      = re.compile(r'/subject/(\d+)/')

    def __init__(self, text, url):
        self._movie_rate     = ""
        self._movie_name     = ""
        self._movie_year     = ""
        self._movie_id       = ""
        self._error_happened = False
        self._movie_address  = url
        self._parse_movie(text)

    def _parse_movie(self, text):
        try:
            self._movie_rate = (re.findall(DoubanMovie._DOUBAN_MOVIE_RATE_PATTERN, text))[0]
            self._movie_name = (re.findall(DoubanMovie._DOUBAN_MOVIE_NAME_PATTERN, text))[0]
            self._movie_year = (re.findall(DoubanMovie._DOUBAN_MOVIE_YEAR_PATTERN, text))[0]
            self._movie_id   = (re.findall(DoubanMovie._DOUBAN_MOVIE_ID_PATTERN, text))[0]
        except BaseException, e:
            self._error_happened = True
            print e

    def __repr__(self):
        if not self._error_happened:
            return ("Rate of %s%s is %s \n" % (self._movie_name, self._movie_year, self._movie_rate))

    @property
    def movie_item(self):
        "Proper format to be serialized to db."
        return [encode_with_utf8(item) for item in
                (self._movie_id, self._movie_name, self.movie_year, self.movie_rate, self._movie_address)]

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

    @property
    def movie_id(self):
        "Get the movie id."
        return self._movie_id


# BFS stratege to do web crawling.
# @see http://stackoverflow.com/questions/20579169/dfs-vs-bfs-in-web-crawler-design
def bfs_crawl(seed):
    """Breadth First Crawling."""

    q = Queue()
    q.enqueue(seed)

    while not q.isEmpty():
        time.sleep(1)
        url = q.deque()

        try:
            rsp = requests.get(url)
        except Exception as e:
            print e
            continue

        urls = set(re.findall(_DOUBAN_MOVIES_PATTERN, rsp.text))
        movie = DoubanMovie(rsp.text, url)

        if not find_movie(movie):
            print(movie.__repr__())
            save_movie(movie.movie_item)

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
