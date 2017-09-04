#!/usr/bin/env python
"""This script is used for parsing perf results."""

import re
import argparse
import json
import sys

def usage():
    sample ="""Parse perf output file and generate funciton calling statistics:
e.g: ./perfParser.py -f out.txt -o statistics
  """
    print sample

def doParseLine(line):
    pass



def doParseFile(input_file, output_file):

  with open(input_file) as f:
    for line in f:
        doParse(line)

  # Filter python objects with list comprehensions
  output_dict = [x for x in input_dict if doMatch(x, filters)]

  # Transform python object back into json
  with open(output_json, 'w') as outfile:
      json.dump(output_dict, outfile, indent=2)
  pass


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
