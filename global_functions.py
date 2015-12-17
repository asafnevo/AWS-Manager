#!/usr/bin/python

import subprocess
import settings
import distutils.spawn


def read_file_to_array(path_to_file):
    """
    read a file into an array
    :param str path_to_file: full path to array
    :return:
    """
    try:
        file_content = open(path_to_file);

    except IOError:
        return False

    content_array = file_content.readlines();
    file_content.close();
    return content_array;


def is_pip_installed():
    """
    Check if the pip is installed
    :return True if installed, False otherwise
    """
    return is_command_exists("pip")


def install_pip():
    """
    install pip
    :return:
    """
    install = raw_input("%s needs to have pip install in order to run. Do you wish to install it now? (y/n)" %
                        settings.script_name)
    if install is "y":
        subprocess.call("sudo python %s" % settings.pip_installation, shell=True)
    elif install is "n":
        print "Cannot run without Pip installed"
        exit()
    else:
        print "Cannot run without Pip installed"
        install_pip()
    init_and_run()


def uninstall_pip():
    """
    uninstall pip
    :return:
    """
    print "This will uninstall both boto3 moudle and pip."
    uninstall_boto3()
    install = raw_input("%s needs to have pip install in order to run. Are you sure you wish to uninstall it? (y/n)" %
                        settings.script_name)
    if install is "y":
        subprocess.call("sudo pip uninstall pip", shell=True)
    init_and_run()


def is_boto3_installed():
    """
    Check if the boto3 is installed
    :return True if installed, False otherwise
    """
    return is_module_exists("boto3")


def install_boto3():
    """
    install boto3
    :return:
    """
    install = raw_input("%s needs to have boto3 installed in order to run. Do you wish to install it now? (y/n)" %
                        settings.script_name)
    if install is "y":
        subprocess.call("sudo pip install boto3", shell=True)
    elif install is "n":
        print "Cannot run without boto3 installed"
        exit()
    else:
        print "Cannot run without boto3 installed"
        install_boto3()
    init_and_run()


def uninstall_boto3():
    """
    uninstall boto3
    :return:
    """
    install = raw_input("%s needs to have boto3 install in order to run. Are you sure you wish to uninstall it? (y/n)" %
                        settings.script_name)
    if install is "y":
        subprocess.call("sudo pip uninstall boto3", shell=True)
    else:
        init_and_run()


def is_command_exists(name):
    """
    Check if a command exists
    :param str name: the name of the comman
    :return: True if the command exists, False otherwise
    """
    return distutils.spawn.find_executable(name) is not None


def is_module_exists(name):
    """
    Check if a moudle exists
    :param str name: the name of the moudle
    :return:
    """
    try:
        __import__(name)
    except ImportError:
        return False
    else:
        return True


def init_and_run():
    install_dependencies()

    import menus
    from aws_credentials import AwsCredentials

    if not AwsCredentials.is_valid_credentials_set():
        menus.show_credential_setup_menu()
    else:
        menus.show_main_menu()

def install_dependencies():
    if not is_pip_installed():
        install_pip()
    if not is_boto3_installed():
        install_boto3()
