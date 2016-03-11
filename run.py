#!/usr/bin/env python3
import sys

from app import app

if len(sys.argv) != 2:
    sys.stdout.write("Usage: run.py myAssetDefinitions.yml\n")
    sys.stderr.write("Invalid amount of arguments. Exiting now!\n")
    sys.exit(1)

app.run(sys.argv[1])
