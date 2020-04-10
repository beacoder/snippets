#!/usr/bin/env python

"""Minimal crawler to crawl high rated movies from movie.douban.com"""

#History#
#1  [DONE] (2017-05-18) crawl movies on douban
#2  [DONE] (2017-05-23) add delays, don't blacklisted by douban
#3  [DONE] (2017-05-25) save data into sqlite
#4  [DONE] (2017-05-25) fix chinese character encoding problem
#5  [DONE] (2017-06-06) only save movies which doesn't exist in DB
#6  [DONE] (2017-06-16) extract breadth_first_search function
#7  [TODO] use eventloop to improve performance
#8  [TODO] separate crawler into two scripts, one for gathering data, the other for querying data
#9  [TODO] push the latest movies to cell phone
#10 [TODO] add logging to log errors


from utils import breadth_first_search
from db import connect_db, find_movie, save_movie, dump_movies
from db import Movie

import re
import requests


# Pattern for matching douban movies
_DOUBAN_MOVIES_PATTERN     = re.compile(r'href="(https?://\S+/subject/\d+/)\S*"')

# Pattern for matching rating numble against douban movie
_DOUBAN_MOVIE_RATE_PATTERN = re.compile(r'<strong class="ll rating_num" property="v:average">(.*)</strong>')

# Pattern for matching douban movie name
_DOUBAN_MOVIE_NAME_PATTERN = re.compile(r'<span property="v:itemreviewed">(.*)</span>')

# Pattern for matching year of douban movie
_DOUBAN_MOVIE_YEAR_PATTERN = re.compile(r'<span class="year">(.*)</span>')

# Pattern for matching id of douban movie
_DOUBAN_MOVIE_ID_PATTERN   = re.compile(r'/subject/(\d+)/')

_DOUBAN_MOVIE_SEED         = "https://movie.douban.com"

_HELP_STRING               ="""Usage:
start()       -> start crawling
dump_movies() -> show movies in DB"""


# @see http://stackoverflow.com/questions/20579169/dfs-vs-bfs-in-web-crawler-design
@breadth_first_search(1)
def crawl(seed):
    """Funciton to crawl.
Given a seed, and return found sites.
    """
    try:
        response = requests.get(seed).text
    except Exception as e:
        return ()

    id=name=year=rate=address = None
    error_happened            = False

    try:
        id      = int((re.findall(_DOUBAN_MOVIE_ID_PATTERN,     response))[0])
        name    = (re.findall(_DOUBAN_MOVIE_NAME_PATTERN,       response))[0]
        year    = (re.findall(_DOUBAN_MOVIE_YEAR_PATTERN,       response))[0]
        rate    = float((re.findall(_DOUBAN_MOVIE_RATE_PATTERN, response))[0])
        address = seed
    except BaseException as e:
        error_happened = True

    if not error_happened:
        movie = Movie(id=id, name=name, year=year, rate=rate, address=address)
        if find_movie(movie) is None:
            print(movie.__repr__())
            save_movie(movie)

    return set(re.findall(_DOUBAN_MOVIES_PATTERN, response))


def start():
    crawl(_DOUBAN_MOVIE_SEED)


if __name__ == '__main__' :
    connect_db()
    print _HELP_STRING
