#!/usr/bin/env python3

import argparse
import sys

from app import app

available_filters = ["Base64Filter", "CleanCssFilter", "CleanSourceMapFilter", "SassFilter", "UglifyJsFilter"]

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("def_file", help="the filename of the definitions file to use")
parser.add_argument("output_dir", help="the directory where to put the resulting files")
parser.add_argument("--working-dir", help="from where to start looking for files")
parser.add_argument("--debug", help="enable debug mode which results in disabled minification and more verbosity",
                    action="store_true", default=False)
parser.add_argument("--verbose", help="enforce more verbosity when processing", action="store_true")
parser.add_argument("--filter", help="when given only process bundles that include this file")
parser.add_argument("--filters-enabled", help="comma separated list of enabled filters",
                    default=",".join(available_filters), type=str)
args = parser.parse_args()

args.filters_enabled = args.filters_enabled.split(",")

if False in list(map(lambda f: f in available_filters, args.filters_enabled)):
    sys.stderr.write("Invalid list of enabled filters supplied using --filters-enabled!")
    sys.exit(1)

if args.verbose:
    app.VERBOSE = True

app.run(def_file=args.def_file, output_dir=args.output_dir, working_dir=args.working_dir, debug=args.debug,
        filter_file=args.filter, filters_enabled=args.filters_enabled)
