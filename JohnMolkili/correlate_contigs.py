import os
import sys

from scipy.stats.stats import pearsonr
import argparse

__author__ = 'Rob Edwards'


def merge_clust(c1, c2, inclust, clustermembers):
    if c2 < c1:
        [c1, c2] = [c2, c1]

    for c in clustermembers[c2]:
        clustermembers[c1].add(c)
        inclust[c] = c1

    clustermembers.pop(c2)
    return inclust, clustermembers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate pairwise pearson correlations between contigs and then cluster them')
    parser.add_argument('-d', help='data table with contigs in rows and occurence in columns', required=True)
    parser.add_argument('-t', help='pearson correlation minimum for clustering (default = 0.9)', default=0.9)
    args = parser.parse_args()

    data = {}
    headers = []
    with open(args.d, 'r') as f:
        for l in f:
            p=l.strip().split("\t")
            if headers == []:
                headers = p
            else:
                data[p[0]] = map(int, p[1:])

    allcontigs  = data.keys()
    allcontigs.sort()
    dist = {x:{} for x in allcontigs}

    cluster = 0
    inclust = {}
    clustermembers = {}

    for i in range(len(allcontigs)):
        cfr = allcontigs[i]
        for j in range(i, len(allcontigs)):
            cto = allcontigs[j]
            if cfr in inclust and cto in inclust and inclust[cfr] == inclust[cto]:
                # no need to calculate!
                continue
            dist[cfr][cto] = dist[cto][cfr] = pearsonr(data[cfr], data[cto])
            if dist[cfr][cto] < args.t:
                if cfr in inclust and cto in inclust:
                    # need to merge these two clusters
                    inclust, clustermembers = merge_clust(inclust[cfr], inclust[cto], inclust, clustermembers)
                elif cfr in inclust:
                    inclust[cto] = inclust[cfr]
                    clustermembers[inclust[cfr]].append(cto)
                elif cto in inclust:
                    inclust[cfr] = inclust[cto]
                    clustermembers[inclust[cto]].append(cfr)
                else:
                    inclust[cfr] = cluster
                    inclust[cto] = cluster
                    clustermembers[cluster] = {cfr, cto}
                    cluster += 1


    for contig in inclust:
        print("{}\t{}".format(contig, inclust[contig]))
