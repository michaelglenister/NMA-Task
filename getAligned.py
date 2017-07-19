#!/usr/bin/env python
# Creates a PDB for a multiple protomer structure, containing co-ords of an aligned PDB structure
import os
import sys
import argparse
from datetime import datetime

import math


def main(args):
    output = args.pdbSca[:args.pdbSca.index('.')]  # "3VBSFull3_SCA_Aligned"
    f = open(args.pdbAligned, 'r')
    lines = f.readlines()
    f.close()

    f = open(args.pdbSca, 'r')
    cg_lines = f.readlines()
    f.close()
    index_of_ter = 210

    coarse_grained = []
    for atom in cg_lines[0:index_of_ter]:
        if atom.startswith("ATOM"):
            info = atom.split()
            first = info[0].strip()
            res = info[3]
            atom_type = info[2]
            chain = info[4]
            res_num = info[5]
            for line in lines:
                if line.startswith("ATOM"):
                    info2 = line.split()
                    res2 = info2[3]
                    atom_type2 = info2[2]
                    chain2 = info2[4]
                    res_num2 = info2[5]
                    if res == res2 and atom_type == atom_type2 and chain == chain2 and res_num == res_num2:
                        coarse_grained.append(line)

    print len(coarse_grained)

    w = open(output + "_SCA.pdb", 'w')
    w.writelines(coarse_grained)
    w.write("END")
    w.close()


silent = False
stream = sys.stdout


def log(message):
    global silent
    global stream

    if not silent:
        print >> stream, message


if __name__ == "__main__":
    # parse cmd arguments
    parser = argparse.ArgumentParser()

    # standard arguments for logging
    parser.add_argument("--silent", help="Turn off logging",
                        action='store_true', default=False)
    parser.add_argument(
        "--log-file", help="Output log file (default: standard output)", default=None)

    # custom arguments
    # '3VBSFull_Aligned.pdb'
    parser.add_argument("--pdbAligned", help="")
    parser.add_argument("--pdbSca", help="")  # '3VBSFull3_SCA.pdb'

    args = parser.parse_args()

    # Check if args supplied by user
    if len(sys.argv) > 1:
        # set up logging
        silent = args.silent

        if args.log_file:
            stream = open(args.log_file, 'w')

        start = datetime.now()
        log("Started at: %s" % str(start))

        # run script
        main(args)

        end = datetime.now()
        time_taken = format_seconds((end - start).seconds)

        log("Completed at: %s" % str(end))
        log("- Total time: %s" % str(time_taken))

        # close logging stream
        stream.close()
    else:
        print "No arguments provided. Use -h to view help"