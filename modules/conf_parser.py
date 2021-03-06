#!/usr/bin/env python3

# For removing whitespaces
import re
# For parsing configuration file
from configparser import ConfigParser

# logging
# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# https://www.loggly.com/ultimate-guide/python-logging-basics/
import logging

class ConfParser:
    """A class for parsing configuration files."""

    def __init__(self):
        self.config = ConfigParser()

    def load_ini_conf(self, conf_file):
        """Loads a configuration file.

        Parameters
        ----------
        config_file : str
            A configuration file in the OS with path.
        """

        self.config.read(conf_file)

    def get_logging_level(self):
        """Returns the log level which should be used for logging.
        logging.LEVEL's type is int."""

        log_level = self.config['Data']['log_level']
        if log_level.lower() == "debug":
            return logging.DEBUG
        elif log_level.lower() == "info":
            return logging.INFO
        elif log_level.lower() == "warning":
            return logging.WARNING
        elif log_level.lower() == "error":
            return logging.ERROR
        elif log_level.lower() == "critical":
            return logging.CRITICAL

    def get_log_path(self):
        """Return log path
        
        Returns
        -------
        str
            log output path.
        """

        return self.config['Data']['log_path']
    
    def get_output_path(self):
        """Return output path.
        
        Returns
        -------
        str
            log output path.
        """

        return self.config['Data']['output_path']
   
    def get_real_names_json(self):
        """Returns path to JSON file which contains real names of GitHub users."""
        
        return self.config['Data']['real_names_json']

    def get_user(self):
        """Returns user defined in configuration file."""
        
        return self.config['Data']['user']

    def get_access_token(self):
        """Returns token in configuration file."""
        
        return self.config['Data']['access_token']
    
    def get_org_url(self):
        """Returns the URL for retrieving organisation information."""

        tmp_str = self.config['Data']['org_url'].replace("MY_ORGANISATION",
                self.get_organisation_name())

        return tmp_str
    
    def get_users_url(self):
        """Returns the URL for retrieving users information."""

        return self.config['Data']['users_url']

    def get_organisation_name(self):
        """Returns organisation name defined in configuration file."""

        return self.config['Data']['organisation_name']
    
    def print_conf(self):
        """Prints all data that was parsed from configuration file."""

        for each_section in self.config.sections():
            for (key, val) in self.config.items(each_section):
                if key == "access_token":
                    print(key, "=", "<CENSORED>")
                else:
                    print(key, "=", val)
