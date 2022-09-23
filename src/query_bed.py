"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from query import Table
from bed import (parse_line, print_line)


def main():
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--output',  # use an option to specify this
                           metavar='output',  # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    # FIXME: put your code here
    
    table = Table()
    for line in args.bed:
        table.add_line(parse_line(line))
    
    for l in args.query:
        query_line = l.split()
        chrom, interval1, interval2 = query_line[0], query_line[1], query_line[2]
        for cell in table.get_chrom(chrom):
            if int(interval1) > int(cell.chrom_start) and int(interval2) < int(cell.chrom_end):
                print_line(cell, args.output)
            if int(interval1) < int(cell.chrom_end) and int(interval2) > int(cell.chrom_start):
                print_line(cell, args.output)
        
        
if __name__ == '__main__':
    main()
