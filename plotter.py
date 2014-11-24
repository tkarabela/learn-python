#!/usr/bin/env python

# make Python 2 more like Python 3
from __future__ import print_function, unicode_literals
from io import open

"""
Plotter

Implement a script to plot data from a CSV file.

The script should not prompt the user for options,
but rather take all options as command line arguments, eg.

    ./plotter.py pie my_data.csv my_plot.png 1:2

to make a pie chart from my_data.csv using 1st column as label
and 2nd column as data, saving it as PNG image to file my_plot.png.

Consider implementing these features:

- various types of plots, eg. line plot, pie chart, histogram
- various output formats, eg. PNG, SVG, PDF (decided by output file extension)
- configurable CSV separator (eg. comma, semicolon, whitespace)
- error handling with helpful error messages
  (eg. missing column in CSV, non-numerical values as data, etc.)
- configurable labels for X and Y axis, caption for the whole plot,
  any other matplotlib options that catch your eye
- plot multiple datasets in one plot (multiple columns from one CSV file)
- option to read the CSV file from standard input instead of a file,
  for use with UNIX pipes, eg. to visualize output of the ps(1) command
- write the part of your program which reads colums from CSV file such that it
  can be used independently and write tests to check its correctness (unit tests)
- use the argparse module to handle command line arguments instead of manually
  working with sys.argv, implement --help option to describe how to use the program

References:
http://matplotlib.org/users/pyplot_tutorial.html
http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.savefig
https://docs.python.org/3/library/argparse.html

"""

import sys
import matplotlib.pyplot as plt
# import argparse


def main():
    args = sys.argv[1:]
    print(args)

if __name__ == "__main__":
    main()
