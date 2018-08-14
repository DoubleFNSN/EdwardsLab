"""
Trim a sequence in a fasta file to a user-defined position
"""

import os
import sys
import argparse
from roblib import stream_fasta

def trim_seq(faf, start=0, end=None, seqid=None, verbose=False):
    """

    Trim a sequence from start to end.
    If start is not provided we use the first base.
    If end is not provided we trim to the end.
    If sequence ID is not provided we trim the first sequence, otherwise we'll trim all the sequences

    :param faf: fasta file
    :param start: optional start position
    :param end:  optional end position
    :param seqid: optional sequence ID to trim
    :param verbose: more output
    :return: Nothing
    """

    for sid, seq in stream_fasta(faf):
        seqname = sid.split(" ")[0]
        if seqid and seqname != seqid:
            continue

        print(">{}\n{}".format(sid, seq[start:end]))
        if verbose:
            sys.stderr.write("Trimmed {}. Next stretch is {}\n".format(sid, seq[end:end+20]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Trim a fasta file")
    parser.add_argument('-f', help='fasta file to trim')
    parser.add_argument('-b', help='optional first base', default=0, type=int)
    parser.add_argument('-e', help='optional last base. Note that this is inclusive, so if you are trying to trim to 3409 as the first base of a repeat use 3408 as your coordinate', default=None, type=int)
    parser.add_argument('-c', help='optional contig name. Otherwise we just trim all the contigs', default=None)
    parser.add_argument('-v', help='verbose output', action="store_true")
    args = parser.parse_args()

    trim_seq(args.f, args.b, args.e, args.c, args.v)