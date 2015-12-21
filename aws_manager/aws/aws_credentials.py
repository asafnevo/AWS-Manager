#!/usr/bin/python
"""
Module to work with aws credentials
"""

import aws_manager.config_file as config_file
import aws_manager.functions as functions

_username = None
""":type str Aws user name"""

_aws_access_key = None
""":type str Aws access key """

_aws_access_key_secret = None
""":type str Aws access key secret"""

_file_path = None
""":type str file path """


def save_path_to_config(path):
    """
    Save path to credential file into the config file
    :param str path: to credential file
    """
    path = path.replace("\\", "")
    config_file.add_parameter("aws_credentials", "aws_credential_path", path)


def load_from_config():
    """
    create an AwsCredentials instance from a credential file in the config
    :return AwsCredentials: instance
    """
    aws_credentials_path = get_stored_credentials_path()
    if aws_credentials_path is None:
        return None

    credentials = get_current_credentials(aws_credentials_path)

    return credentials


def get_current_credentials(file_path=None):
    global _aws_access_key, _aws_access_key_secret, _username
    """
    Get the current loaded aws credentials
    :param str file_path: optional path to load the credentials from
    :rtype: dict
    :return dict with "key" and "secret" keys
    """
    if file_path is not None:
        load_from_file(file_path)
    credentials = {"key": _aws_access_key, "secret": _aws_access_key_secret, "username": _username}
    return credentials


def set_current_credentials(key, secret):
    global _aws_access_key, _aws_access_key_secret
    """
    Set the current credentials
    :param str key: the aws access key
    :param str secret: the aws access key secret
    """
    _aws_access_key = key
    _aws_access_key_secret = secret


def get_stored_credentials_path():
    """
    Get the stored credentials path
    :return str: the stored credential path
    """
    return config_file.get_parameter("aws_credentials", "aws_credential_path");


def remove_stored_credential_path():
    """
    Remove stored credential path
    """
    return config_file.remove_parameter("aws_credentials", "aws_credential_path");


def is_valid_credentials_set():
    """
    Check if there is a valid credential set
    :return: True if there are credential set, False otherwise
    """
    if load_from_config() is None:
        return False
    return True


def set_file_path(file_path):
    global _file_path
    """
    Set the file path
    :param str file_path: the file path
    :return:
    """
    _file_path = file_path


def get_file_path():
    global _file_path
    """
    Get the file path
    :return: the file path for the credentials
    :rtype str
    """
    return _file_path


def set_username(username):
    global _username
    """
    Set the user name
    :param str username: set the user name
    """
    _username = username


def get_username():
    global _username
    """
    get the username
    :return: the user name
    :rtype str
    """
    return _username


def set_key(key):
    global _aws_access_key
    """
    Set the Aws access key
    :param str key: the Aws access key
    """
    _aws_access_key = key


def get_key():
    global _aws_access_key
    """
    Get the AWS access key
    :return: the AWS access Key
    :rtype: str
    """
    return _aws_access_key


def set_secret(secret):
    global _aws_access_key_secret
    """
    Set the AWS secret
    :param str secret: the aws secret
    """
    _aws_access_key_secret = secret;


def get_secret():
    global _aws_access_key_secret
    """
    Get the aws secret
    :return: the aws secret
    :rtype str: the aws secret
    """
    return _aws_access_key_secret


def load_from_file(file_path):
    global _file_path, _username, _aws_access_key, _aws_access_key_secret
    """
    Creates a credential object from a file
    :param str file_path: the path to credential file
    """
    try:
        _file_path = file_path.strip()
        _file_path = _file_path.replace("\\", "")
        credentials_file_content = functions.read_file_to_array(_file_path)
        if not credentials_file_content:
            raise IOError("Error opening credentials file")
        credentials_file_content = credentials_file_content[1].split(",")
        _username = credentials_file_content[0].replace('"', '')
        _aws_access_key = credentials_file_content[1]
        _aws_access_key_secret = credentials_file_content[2]
    except IOError, e:
        remove_stored_credential_path()
        print e
        exit()


def save_to_config():
    global _file_path
    """
    Save the credentials to the config file
    """
    config_file.add_parameter("aws_credentials", "aws_credential_path", _file_path)
