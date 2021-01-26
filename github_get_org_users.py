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

# For logging
# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# https://www.loggly.com/ultimate-guide/python-logging-basics/
import logging
import logging.handlers
import os
# Retrieve the name of current function
import inspect

# JSON handling
import json
import modules.json_ops as json_ops

# Time stamps to files
from datetime import datetime

# For creating requests to GitHub API
import requests

# For parsing configurations
from modules.conf_parser import ConfParser

def get_org_members(conf: ConfParser = None):
    
    if conf == None or not isinstance(conf, ConfParser):
        logging.error("No conf given.")
        return

    auth=(conf.get_user(),conf.get_access_token()) 
    headers = {'Accept': 'application/vnd.github.v3+json'}
    url = "https://api.github.com/orgs/{}/members".format(conf.get_organisation_name())
    response = requests.get(url, headers=headers, auth=auth)

    return response

def get_user_info(conf: ConfParser = None, username: str = None):

    if conf == None or not isinstance(conf, ConfParser):
        logging.error("Func: {} no conf given.".format(inspect.stack()[0][3]))
        return
    
    if username == None or not isinstance(username, str):
        logging.error("Func: {} no username given.".format(inspect.stack()[0][3]))
        return

    auth=(conf.get_user(),conf.get_access_token()) 
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    url = "https://api.github.com/users/" + username
    response = requests.get(url, headers=headers)

    return response

def extract_org_member_logins(json_obj: list = None):

    if json_obj == None or not isinstance(json_obj, list):
        logging.error("Func: {} no json_obj given.".format(inspect.stack()[0][3]))
        return

    login_list = list()

    # Loop through json_obj to extract all login usernames
    for user in json_obj:
        print(user)
        login_list.append(user["login"])

    return login_list

def combine_github_name_and_login(conf: ConfParser = None, login_names: list = None):
    
    if conf == None or not isinstance(conf, ConfParser):
        logging.error("Func: {} no conf given.".format(inspect.stack()[0][3]))
        return
    
    if json_obj == None or not isinstance(json_obj, list):
        logging.error("Func: {} no login_names given.".format(inspect.stack()[0][3]))
        return


    
def main():
    arguments = docopt(__doc__, version='GitHub Get Org Users 0.1')
    config = ConfParser()
    config.load_ini_conf(arguments["--config"])

    # Create log file
    log_to_file(config, "main")

    logging.info("Loaded configuration:")
    config.print_conf()

    org_json= get_org_members(config).json()

    login_name_list = extract_org_member_logins(org_json)
    print(login_name_list)
    

    print(get_user_info(config, "juho-bt").json()["name"])

# Example:
# https://realpython.com/python-logging/
def log_to_file(config: ConfParser = None, log_id: str = None):
    log_path = config.get_log_path()
    log_name = log_path + log_id + "_" + \
            datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"

    # Probably some import initializes the logging already,
    # but logging needs to be initialized this way to get the
    # output to certain file.
    # https://stackoverflow.com/a/46098711
    logging.root.handlers = []
    logging.basicConfig(level=config.get_logging_level(), \
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_name),
                logging.StreamHandler()
            ]
    )

if __name__ == '__main__':
    main()
