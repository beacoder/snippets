#!/usr/bin/env python

"Minimal crawler to crawl high rated movies from douban.com"

import re
import requests


# Pattern for matching douban movies
_DOUBAN_MOVIES_PATTERN = re.compile(
    r'href="(https?://\S+/subject/\d+/)\S*"')

def str_to_utf8(in_string):
    "Convert string to utf-8 encoding."
    ret_string = u' '.join(in_string).encode('utf-8').strip()
    return ret_string

def remove_duplicates(seq):
    "Remove duplicate items from a list."
    seq = list(set(seq))
    return seq


class DoubanMovie(object):
    """Represent a movie from movie.douban.com"""

    # Pattern for matching rating numble against douban movie
    _DOUBAN_RATING_NUMBER_PATTERN = re.compile(
        r'<strong class="ll rating_num" property="v:average">(.*)</strong>')

    # Pattern for matching douban movie name
    _DOUBAN_MOVIE_NAME_PATTERN    = re.compile(
        r'<span property="v:itemreviewed">(.*)</span>')

    # Pattern for matching year of douban movie
    _DOUBAN_MOVIE_YEAR_PATTERN    = re.compile(
        r'<span class="year">(.*)</span>')

    def __init__(self, url):
        self._rating_num = ""
        self._movie_name = ""
        self._movie_year = ""
        self._parse_movie(url)

    def _parse_movie(self, url):
        rsp = requests.get(url).text
        try:
            self._rating_num = (re.findall(DoubanMovie._DOUBAN_RATING_NUMBER_PATTERN, rsp))[0]
            self._movie_name = (re.findall(DoubanMovie._DOUBAN_MOVIE_NAME_PATTERN, rsp))[0]
            self._movie_year = (re.findall(DoubanMovie._DOUBAN_MOVIE_YEAR_PATTERN, rsp))[0]
        except BaseException, e:
            print e

    def __repr__(self):
        return ("Rate of %s%s is %s \n" % (self._movie_name, self._movie_year, self._rating_num))

    @property
    def rating_num(self):
        "Get the rating number of a movie."
        return self._rating_num

    @property
    def movie_name(self):
        "Get the movie name."
        return self._movie_name

    @property
    def movie_year(self):
        "Get the movie year."
        return self._movie_year

def crawl():
    """Start crawling."""
    # Crawl douban movie
    rsp  = requests.get("https://movie.douban.com")
    urls = remove_duplicates(re.findall(_DOUBAN_MOVIES_PATTERN, rsp.text))

    for movie_site in urls:
        movie = DoubanMovie(movie_site)
        print(movie.__repr__())

if __name__ == '__main__' :
    crawl()
