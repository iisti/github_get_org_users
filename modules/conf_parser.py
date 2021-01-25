#!/usr/bin/env python3

# For removing whitespaces
import re
# For parsing configuration file
from configparser import ConfigParser


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
