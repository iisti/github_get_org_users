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

# CSV handling
import csv

# Time stamps to files
from datetime import datetime

# For creating requests to GitHub API
import requests

# For parsing configurations
from modules.conf_parser import ConfParser

# This is not actually used by this program.
def get_user_info(conf: ConfParser = None, username: str = None):
    """Retrieves user information from GitHub API."""
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

def get_org_members(conf: ConfParser = None):
    """Retrieves organisation members from GitHub API."""

    if conf == None or not isinstance(conf, ConfParser):
        logging.error("No conf given.")
        return

    auth=(conf.get_user(),conf.get_access_token()) 
    headers = {'Accept': 'application/vnd.github.v3+json'}
    url = "https://api.github.com/orgs/{}/members?per_page=100".format(conf.get_organisation_name())
    response = requests.get(url, headers=headers, auth=auth)

    return response


def extract_org_member_logins(json_obj: list = None):
    """Extracts login name information from the organisation members JSON retrieved from GitHub API.
    
    Parameters
    ----------
    json_obj : list
        A JSON file of organisation members retrieved from GitHub API.
    Returns
    -------
    dict
        A dict which contains login usernames as keys and None as values.
    """

    if json_obj == None or not isinstance(json_obj, list):
        logging.error("Func: {} no json_obj given.".format(inspect.stack()[0][3]))
        return

    login_dict = dict()

    # Loop through json_obj to extract all login usernames
    for user in json_obj:
        login_dict[user["login"]] = None

    return login_dict

def add_names_from_file(conf: ConfParser = None, json_dict: dict = None):
    """Combines a real name with the GitHub login name. Uses a user created JSON file as an
    information source."""
    
    if conf == None or not isinstance(conf, ConfParser):
        logging.error("Func: {} no conf given.".format(inspect.stack()[0][3]))
        return
    
    if json_dict == None or not isinstance(json_dict, dict):
        logging.error("Func: {} no json_dict given.".format(inspect.stack()[0][3]))
        return
    
    real_names_dict = json_ops.open_json(conf.get_real_names_json())

    # Loop trough the json_dict (which contains login usernames retrieved from GitHub)
    # and insert real names to the dict value.
    for login_name_json in json_dict.keys():
        for login_name_file, real_name in real_names_dict.items():
            if login_name_json == login_name_file:
                json_dict[login_name_json] = real_name

def check_for_unknown_users(conf: ConfParser = None, json_dict: dict = None):
    """Checks if there are any unkown users and creates a dictionary of the unknown users."""

    if conf == None or not isinstance(conf, ConfParser):
        logging.error("Func: {} no conf given.".format(inspect.stack()[0][3]))
        return
    
    if json_dict == None or not isinstance(json_dict, dict):
        logging.error("Func: {} no json_dict given.".format(inspect.stack()[0][3]))
        return
   
    real_names_dict = json_ops.open_json(conf.get_real_names_json())
    
    unknown_users_dict = dict()

    for login_name_json, val in json_dict.items():
        if not login_name_json in real_names_dict:
            logging.warning("No login name {} found!".format(login_name_json))
            unknown_users_dict[login_name_json] = val

    return unknown_users_dict

def write_csv(conf: ConfParser = None, json_dict: dict = None):
    """Writes GitHub login names and real names into CSV file."""

    file_out = conf.get_output_path() + "github_known_users_" + \
            datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
    
    logging.info("Writing CSV: " + file_out)

    with open(file_out, mode='w') as outfile:
        name_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        name_writer.writerow(['GitHub login', 'Name'])

        for user, real_name in json_dict.items():
            name_writer.writerow([user, real_name])

def main():
    arguments = docopt(__doc__, version='GitHub Get Org Users 0.1')
    config = ConfParser()
    config.load_ini_conf(arguments["--config"])

    # Create log file
    log_to_file(config, "main")

    # Print loaded configuration
    logging.info("Loaded configuration:")
    config.print_conf()

    # Retrieve organisation members
    org_json = get_org_members(config).json()

    # Grab names from the retrieved JSON
    login_name_dict = extract_org_member_logins(org_json)
    
    # Replace real names with value None to the real name
    add_names_from_file(config, login_name_dict)
    
    # Check if there are unknown users and create a dict if there are.
    unknown_users_dict = check_for_unknown_users(config, login_name_dict)
    if unknown_users_dict:
        json_ops.write_json_dump(unknown_users_dict, "github_unknown_users", config.get_output_path())

    # Write a JSON file including known organisation members.
    json_ops.write_json_dump(login_name_dict, "github_known_users", config.get_output_path())

    # Write a CSV file
    write_csv(config, login_name_dict)

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
