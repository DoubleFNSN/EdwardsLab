"""
Convert a triple of [name, lat, lon] to a matrix of pairwise distances
"""

import os
import sys
import argparse
import math

__author__ = 'Rob Edwards'



def latlon2distance(lat1, long1, lat2, long2, miles=False):
    """Convert two coordinates to distance.

    This is an approximation since the earth is not spherical, but accuracy is <100m, especially for close points

    This code was taken from http://www.johndcook.com/python_longitude_latitude.html

    Latitude is measured in degrees north of the equator; southern locations have negative latitude.
    Similarly, longitude is measured in degrees east of the Prime Meridian. A location 10deg west of
    the Prime Meridian, for example, could be expressed as either 350deg  east or as -10deg east.

    Arguments: lat1, long1; lat2, long2; miles is a boolean. If you want miles set it to true. Else set it to false

    """

    if lat1 == lat2 and long1 == long2:
        return 0


    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    try:
        arc = math.acos(cos)
    except Exception as err:
        sys.stderr.write("There was an err: {} trying to take the acos of ({})\n".format(err, cos))
        arc=0
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    #
    # To convert to miles multiple arc by 3960
    # To convert to kilometers multiply arc by 6373

    if miles:
        arc *= 3960
    else:
        arc *= 6373

    return arc




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a triple of [name, lat, lon] to a matrix of pairwise distances')
    parser.add_argument('-f', help='input file with [name, lat, lon]', required=True)
    parser.add_argument('-i', help='ignore the first line', action='store_true')
    args = parser.parse_args()

    first = args.i
    loc = {}
    with open(args.f, 'r') as f:
        for l in f:
            if first:
                first = False
                continue
            p = l.strip().split("\t")
            if len(p) < 3:
                sys.stderr.write("Not enough values. Skipped: {}\n".format(l.strip()))
                continue
            try:
                loc[p[0]]=[float(p[1]), float(p[2])]
            except Exception as err:
                sys.stderr.write("Error {} converting {}\n".format(err, l.strip()))

    names = list(loc.keys())
    names.sort()
    sys.stdout.write("\t" + "\t".join(names))
    sys.stdout.write("\n")
    for i in range(len(names)):
        fn = names[i]
        sys.stdout.write(fn)
        for j in range(len(loc)):
            tn = names[j]
            if fn == tn:
                sys.stdout.write("\t0")
                continue
            #sys.stdout.write("{}, {} :: {}, {}".format(loc[fn][0], loc[fn][1], loc[tn][0], loc[tn][1]))
            dist = latlon2distance(loc[fn][0], loc[fn][1], loc[tn][0], loc[tn][1])
            sys.stdout.write("\t{}".format(dist))
            #sys.stdout.write("\n")
        sys.stdout.write("\n")

