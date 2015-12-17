#!/usr/bin/python

from config import *
import global_functions


class AwsCredentials:
    """
    This class represents credentials of AWS
    """

    _current_credentials = None
    """ :type _current_credentials: AwsCredentials the current loaded credentials """

    @staticmethod
    def save_path_to_config(path):
        """
        Save path to credential file into the config file
        :param str path: to credential file
        """
        path = path.replace("\\", "")
        config = ConfigFile();
        config.add_parameter("aws_credentials", "aws_credential_path", path)

    @staticmethod
    def load_from_config(set_as_current=True):
        """
        create an AwsCredentials instance from a credential file in the config
        :param set_as_current: default True if to set this file as the current instance
        :return AwsCredentials: instance
        """
        aws_credentials_path = AwsCredentials.get_stored_credentials_path()
        if aws_credentials_path is None:
            return None

        credentials = AwsCredentials(aws_credentials_path)

        if set_as_current:
            AwsCredentials._current_credentials = credentials;

        return credentials

    @staticmethod
    def get_current_credentials():
        """
        Get the current loaded AwsCredentials instance
        :rtype: AwsCredentials
        :return AwsCredentials of the current credentials
        """
        return AwsCredentials._current_credentials

    @staticmethod
    def set_current_credentials(credentials):
        """
        Set the current credentials
        :param AwsCredentials credentials: the credentials to set as current
        """
        AwsCredentials._current_credentials = credentials

    @staticmethod
    def get_stored_credentials_path():
        """
        Get the stored credentials path
        :return str: the stored credential path
        """
        config = ConfigFile()
        return config.get_parameter("aws_credentials", "aws_credential_path");

    @staticmethod
    def remove_stored_credential_path():
        config = ConfigFile()
        return config.remove_parameter("aws_credentials", "aws_credential_path");

    @staticmethod
    def is_valid_credentials_set():
        """
        Check if there is a valid credential set
        :return: True if there are credential set, False otherwise
        """
        if AwsCredentials.load_from_config() is None:
            return False
        return True

    def __init__(self, filepath=None):
        """
        Init a new AwsCredentials instance
        :param str filepath: optional full path to file
        """
        if filepath is not None:
            self.load_from_file(filepath)

    def _set_file_path(self, filepath):
        self._filePath = filepath

    def _get_file_path(self):
        return self._filePath

    def _set_username(self, name):
        self._name = name

    def _get_username(self):
        return self._name;

    def _set_key(self, key):
        self._key = key

    def _get_key(self):
        return self._key

    def _set_secret(self, secret):
        self.secret = secret;

    def _get_secret(self):
        return self.secret;

    def load_from_file(self, filepath):
        """
        Creates a credential object from a file
        :param str filepath: the path to credential file
        """
        try:
            self.file_path = filepath.strip();
            self.file_path = filepath.replace("\\", "");
            credentials_file_content = global_functions.read_file_to_array(filepath)
            if not credentials_file_content:
                raise IOError("Error opening credentials file")
            credentials_file_content = credentials_file_content[1].split(",")
            self.username = credentials_file_content[0].replace('"', '')
            self.access_key = credentials_file_content[1]
            self.secret = credentials_file_content[2]
        except IOError, e:
            AwsCredentials.remove_stored_credential_path()
            print e
            exit()

    def save_to_config(self):
        """
        Save the credentials to the config file
        """
        config = ConfigFile()
        config.add_parameter("aws_credentials", "aws_credential_path", self.file_path)

    file_path = property(_get_file_path, _set_file_path)
    username = property(_get_username, _set_username)
    access_key = property(_get_key, _set_key)
    secret = property(_get_secret, _set_secret)
