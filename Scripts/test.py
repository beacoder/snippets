#!/usr/bin/env python

"Minimal crawler to crawl high rated movies from douban.com"

import re
import requests


# Pattern for matching douban movies
_DOUBAN_MOVIES_PATTERN = re.compile(r'href="(https?://\S+/subject/\d+/)\S*"')

# Pattern for matching rating numble against douban movie
_DOUBAN_RATING_NUMBER_PATTERN = re.compile(
    r'<strong class="ll rating_num" property="v:average">(.*)</strong>')

# Pattern for matching douban movie name
_DOUBAN_MOVIE_NAME_PATTERN = re.compile(r'<span property="v:itemreviewed">(.*)</span>')

# Pattern for matching year of douban movie
_DOUBAN_MOVIE_YEAR_PATTERN = re.compile(r'<span class="year">(.*)</span>')

def str_to_utf8(in_string):
    "Convert string to utf-8 encoding."
    ret_string = u' '.join(in_string).encode('utf-8').strip()
    return ret_string

def remove_duplicates_from_list(seq):
    "Remove duplicate items from a list."
    seq = list(set(seq))
    return seq
    
def get_rating_num(url):
    "Get the rating number of a movie."
    try:
        return float((re.findall(_DOUBAN_RATING_NUMBER_PATTERN,
                                 requests.get(url).text))[0])
    except BaseException, e:
        print e
        return None

    def get_movie_name(url):
    "Get the movie name."
    try:
        return float((re.findall(_DOUBAN_MOVIE_NAME_PATTERN,
                                 requests.get(url).text))[0])
    except BaseException, e:
        print e
        return None

def get_movie_year(url):
    "Get year of a movie."
    
class DoubanMovie(object):
    """Represent a movie from movie.douban.com"""

    def __init__(self,
                 url):
        self.url = url

    @property
    def rating_num(self):
        "Get the rating number of a movie."
        try:
            return float((re.findall(_DOUBAN_RATING_NUMBER_PATTERN,
                                     requests.get(url).text))[0])
        except BaseException, e:
            print e
            return None

    def get_movie_name(url):
        "Get the movie name."
        try:
            return float((re.findall(_DOUBAN_MOVIE_NAME_PATTERN,
                                     requests.get(url).text))[0])
        except BaseException, e:
            print e
            return None


def test():
    """Start crawling."""
    # Crawl douban movie
    rsp  = requests.get("https://movie.douban.com")
    urls = remove_duplicates_from_list(re.findall(_DOUBAN_MOVIES_PATTERN, rsp.text))

    for l in urls:
        r = get_rating_num(l)
        if r is None:
            r = 0.00
        print("Rate of %s is %f \n" % (l, r))

if __name__ == '__main__' :
    test()    
