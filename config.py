#!/usr/bin/python

from ConfigParser import ConfigParser


class ConfigFile:
    """
    Class for writing and received values from the config file
    """

    def __init__(self):
        self.configFileName = ".config"
        self.config = ConfigParser()
        self.config.read(self.configFileName)

    def _add_section(self, name):
        if not self.config.has_section(name):
            self.config.add_section(name)

    def add_parameter(self, section, name, value):
        self._add_section(section)
        self.config.set(section, name, value)
        self.save()

    def get_parameter(self, section, name):
        if not self.config.has_option(section, name):
            return None
        return self.config.get(section, name)

    def remove_parameter(self, section, name):
        if self.config.has_option(section, name):
            self.config.remove_option(section, name);
            self.save()

    def save(self):
        config = open(self.configFileName, 'w')
        with config as f:
            self.config.write(f)
        config.close()
