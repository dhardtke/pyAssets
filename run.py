#!/usr/bin/env python3

import argparse

from app import app

parser = argparse.ArgumentParser()
parser.add_argument("def_file", help="the filename of the definitions file to use")
parser.add_argument("output_dir", help="the directory where to put the resulting files")
parser.add_argument("--working-dir", help="from where to start looking for files")
parser.add_argument("--debug", help="enable debug mode which results in disabled minification and more verbosity",
                    action="store_true")
parser.add_argument("--verbose", help="enforce more verbosity when processing", action="store_true")
parser.add_argument("--filter", help="when given only process bundles that include this file")
parser.set_defaults(debug=False)
args = parser.parse_args()

if args.verbose:
    app.VERBOSE = True

app.run(def_file=args.def_file, output_dir=args.output_dir, working_dir=args.working_dir, debug=args.debug,
        filter_file=args.filter)
