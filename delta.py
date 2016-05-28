#!/usr/bin/python
from elasticsearch import Elasticsearch
from config import *
from optparse import OptionParser
from cursor import Cursor
from processor import Processor
from queries import Query
import json

def main():
    parser = OptionParser()
    parser.add_option("-l", "--list",
                      action="store_true", dest="show_list",
                      help="list all available data sets")
    parser.add_option("-p", "--process",
                      action="store",
                      dest="process_file",
                      metavar="FILE data_source", 
                      nargs=2,
                      help="process file into data base")
    parser.add_option("-o", "--diff-overlap",
                      action="store", 
                      nargs=2,
                      dest="diff_overlap",
                      metavar="[HASH 1] [HASH 2]", 
                      help="find the overlap of 2 data sets")
    parser.add_option("-m", "--diff-minus",
                      action="store", 
                      nargs=2,
                      dest="diff_minus",
                      metavar="[HASH 1] [HASH 2]", 
                      help="find the data in data set 1 but excluded from data set 2")
    parser.add_option("-c", "--diff-combine",
                      action="store", 
                      nargs=2,
                      dest="diff_combine",
                      metavar="[HASH 1] [HASH 2]", 
                      help="find the combined data set from data set 1 and data set 2")

    (opts, args) = parser.parse_args()

    if opts.show_list:
        lookup = Cursor(es, "all_data")
        lookup.list()
    # process file
    elif opts.process_file:
        p = Processor(es, opts.process_file[0], opts.process_file[1])
        p.process()
    # show data in set 1 and set 2
    elif opts.diff_overlap:
        # translate key value into data source and version
        lookup = Cursor(es, "all_data")
        (source_1, version_1) = lookup.search_by_key(opts.diff_overlap[0])
        (source_2, version_2) = lookup.search_by_key(opts.diff_overlap[1])
        # search database
        q = Query(es)
        res = q.search_match_field_value_a_and_b(source_1, version_1, source_2, version_2)
        print json.dumps(res, indent=2)
    # show data in set 1 but not in set 2
    elif opts.diff_minus:
        # translate key value into data source and version
        lookup = Cursor(es, "all_data")
        (source_1, version_1) = lookup.search_by_key(opts.diff_minus[0])
        (source_2, version_2) = lookup.search_by_key(opts.diff_minus[1])
        # search database
        q = Query(es)
        res = q.search_match_field_value_a_not_b(source_1, version_1, source_2, version_2)
        print json.dumps(res, indent=2)
    # show data in set 1 or in set 2
    elif opts.diff_combine:
        # translate key value into data source and version
        lookup = Cursor(es, "all_data")
        (source_1, version_1) = lookup.search_by_key(opts.diff_combine[0])
        (source_2, version_2) = lookup.search_by_key(opts.diff_combine[1])
        # search database
        q = Query(es)
        res = q.search_match_field_value_a_or_b(source_1, version_1, source_2, version_2)
        print json.dumps(res, indent=2)
    else:
        # ignore other options
        parser.print_help()


if __name__ == "__main__":
    main()



