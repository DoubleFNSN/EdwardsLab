#!/usr/bin/env python

"""
Renumber a fasta file, starting with either number 1 or a number provided on the command line.
At the end, we output the last number written.

Note that this uses the roblib library that is available from this github repository.
"""

import os
import sys
import argparse
from roblib import read_fasta

__author__ = 'Rob Edwards'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-f', help='input file', required=True)
    parser.add_argument('-o', help='output file', required=True)
    parser.add_argument('-n', help='number to start from. Default: 1', type=int, default=1)
    parser.add_argument('-x', help='maximum number of sequences to write out', type=int)
    args = parser.parse_args()


    counter = args.n - 1
    fa = read_fasta(args.f)
    with open(args.o, 'w') as out:
        for id in fa:
            counter += 1
            out.write(">{}\n{}\n".format(counter, fa[id]))
            if args.x and (counter - (args.n-2)) > args.x:
                break

    print("The last ID written to the file {} was {}".format(args.o, counter))

