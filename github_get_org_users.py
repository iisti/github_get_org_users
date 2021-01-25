#!/usr/bin/env python3

"""GitHub Get Org Users

This is a Python program for retrieving GitHub usernames in a certain organisation and combining
with real names.

Usage:
    github_get_org_users.py (-c <FILE> | --config <FILE>)
    github_get_org_users.py (-h | --help)
    github_get_org_users.py --version

Options:
    -h --help   Show this screen.
    --version   Show version.
    -c --config Configuration file.

"""

# -*- coding: utf-8 -*-
# For documentation
from docopt import docopt

# JSON handling
import json

# Time stamps to files
from datetime import datetime

import requests

from modules.conf_parser import ConfParser

def main():
    arguments = docopt(__doc__, version='GitHub Get Org Users 0.1')
    config = ConfParser()
    config.load_ini_conf(arguments["--config"])

    print("Loaded configuration:")
    config.print_conf()

if __name__ == '__main__':
    main()