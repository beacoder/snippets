#!/usr/bin/env python

"""Minimal crawler to crawl high rated movies from douban.com"""

#1 [Done]  crawl movies on douban
#2 [Done]  add delays, don't blacklisted by douban
#3 [Todo]  save data into sqlite
#4 [Todo]  push the latest movies to cell phone

import re
import requests
from collections import deque
import time


# Pattern for matching douban movies
_DOUBAN_MOVIES_PATTERN = re.compile(r'href="(https?://\S+/subject/\d+/)\S*"')

_DOUBAN_MOVIE_SEED     = "https://movie.douban.com"

_CRAWLED_SITES         = set()

def str_to_utf8(in_string):
    "Convert string to utf-8 encoding."
    ret_string = u' '.join(in_string).encode('utf-8').strip()
    return ret_string

class _Base_For_Queue_And_Stack:
    """Base class for Queue and Stack."""
    def __init__(self):
        self.items = deque()

    def isEmpty(self):
        return (len(self.items) == 0)

    def __iter__(self):
        return self

    def size(self):
        return len(self.items)


class Queue(_Base_For_Queue_And_Stack):
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


class Stack(_Base_For_Queue_And_Stack):
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

    def __init__(self, text):
        self._movie_rate = ""
        self._movie_name = ""
        self._movie_year = ""
        self._parse_movie(text)
        self._error_happened = False

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
        else:
            return "\n"

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


# Normally, BFS will be a good idea for web crawling.
# @see http://stackoverflow.com/questions/20579169/dfs-vs-bfs-in-web-crawler-design
def bfs_crawl(seed):
    """Breadth First Crawling."""

    q = Queue()
    q.enqueue(seed)

    with requests.Session() as s:
        while not q.isEmpty():
            time.sleep(3.0)
            rsp = s.get(q.deque())
            urls = set(re.findall(_DOUBAN_MOVIES_PATTERN, rsp.text))

            movie = DoubanMovie(rsp.text)
            print(movie.__repr__())

            for url in urls:
                q.enqueue(url)
    pass


if __name__ == '__main__' :
    bfs_crawl(_DOUBAN_MOVIE_SEED)
