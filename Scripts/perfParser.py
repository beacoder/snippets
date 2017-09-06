#!/usr/bin/env python
"""This script is used for parsing perf results."""

from collections import defaultdict
import re
import argparse
import json
import sys
import pdb

# nested_dict = lambda: defaultdict(nested_dict)
# nd = nested_dict()
# nd["a","b","c"] = 'local'
# assert nd["a"]["b"]["c"] == 'local'

def nested_dict():
    """return a nested_dict."""

    children    = defaultdict(nested_dict)
    children[0] = 0
    return children


class ParserTree(object):
    """Used to store parsed perf data."""

    def __init__(self):
        """used nested_dict as a tree."""

        self._data_ = nested_dict()
        pass


    def insert(self, keys, value):
        """insert tree data.
e.g: ParseTree.insert([1,2,3], 1) => ParseTree[1][2][3] = 1."""

        ptr = self._data_
        for key in keys.split(";"):
            ptr    =  ptr[key]
            ptr[0] += value
        pass

    @breadth_first_search(1)
    def __repr__(self):
        """show the tree data."""
        # use queue strucuture to iterate.
        pass

    pass


def usage():
    """usage information"""

    sample ="""Parse perf output file and generate funciton calling statistics:
e.g: ./perfParser.py -f out.txt -o statistics
    """
    print sample


def doParseLine(line, tree):
    (keys, value) = line.rsplit(" ", 1)
    print keys
    print value

    tree.insert(keys, int(value))
    pass


def doParseFile(input_file, output_file):
    tree = ParserTree()
    with open(input_file) as f:
        for line in f:
            doParse(line, tree)
    pass


  # Filter python objects with list comprehensions
  # output_dict = [x for x in input_dict if doMatch(x, filters)]

  # Transform python object back into json
  # with open(output_json, 'w') as outfile:
  #     json.dump(output_dict, outfile, indent=2)
  # pass


def createParser():
    p = argparse.ArgumentParser()
    p.add_argument("-f")
    p.add_argument("-o")

    return p.parse_args()


def main():
    args = createParser()

    if args.f and args.o:
        doParseFile(args.f, args.o)
    else:
        usage()

    sys.exit(0)


if __name__ == "__main__":
    main()
