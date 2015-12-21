#!/usr/bin/python
"""
Module for writing and reading values from the config file
"""
import aws_manager.settings as settings
from ConfigParser import ConfigParser

_config_file_name = settings.config_file_name  # ".config"


"""
The config file name
:type: str
"""

_config = ConfigParser()
"""
The ConfigParser instance
:type: ConfigParser
"""

# read the config file
print _config.read(_config_file_name)


def _add_section(name):
    global _config
    """
    Add a new section to the config file
    :param str name: the name of the section to add
    """
    if not _config.has_section(name):
        _config.add_section(name)


def add_parameter(section, name, value):
    global _config
    """
    Add a new paramter to the config file
    :param str section: the section in the config file for the new parameter
    :param str name: the name of the parameter
    :param str value: the value of the parameter
    """
    _add_section(section)
    _config.set(section, name, value)
    _save()


def get_parameter(section, name):
    global _config
    """
    Get a paramter from the config file

    :param str section: the name of the section in which the parameter would be found
    :param str name:  the name of the parameter
    :return: the parameter or None if it doesn't exists
    :rtype: str
    """
    if not _config.has_option(section, name):
        return None
    return _config.get(section, name)


def remove_parameter(section, name):
    global _config
    """
    Remove a parameter from the config file
    :param str section: The section of the parameter to remove
    :param str name: The name of the paramter to remove
    """
    if _config.has_option(section, name):
        _config.remove_option(section, name);
        _save()


def _save():
    global _config, _config_file_name
    """
    Save the config file to the file
    """
    with open(_config_file_name, 'w') as f:
        _config.write(f)

