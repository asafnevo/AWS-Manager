#!/usr/bin/python
"""
Module for running AWS related functions
"""

import aws_credentials
import boto3
import collections
import aws_manager.config_file as config_file
from subprocess import PIPE, Popen
import subprocess


def get_default_region():
    return "eu-central-1"


def load_ec2_instances(region):
    """
    Load the EC2 instances a region
    :param region:
    :rtype: list
    :return: a list of the instances in a region or None if there are no instances
    """
    ec2 = _get_resource("ec2", region)
    ec2_instances = ec2.instances.all()
    counter = collections.Counter(ec2_instances)
    ec2_size = sum(counter.itervalues())
    if ec2_size == 0:
        return None
    return ec2_instances


def get_environments_from_instances(instances):
    """
    Get all the environments available from instances lists
    :param list instances: the list of instance
    :rtype: list
    :return: a list of the environments
    """
    environments = []
    for instance in instances:
        tags = instance.tags
        for tag in tags:
            key = tag.get("Key")
            if key == "Environment":
                environment = tag.get("Value").strip()
                if environment not in environments:
                    environments.append(environment)
    return environments


def get_applications_from_instances(instances):
    """
    Get all the application available from instances lists
    :param list instances: the list of instance
    :rtype: list
    :return: a list of the applications
    """
    applications = []
    for instance in instances:
        tags = instance.tags
        for tag in tags:
            key = tag.get("Key")
            if key == "Application":
                application = tag.get("Value").strip()
                if application not in applications:
                    applications.append(application)
    return applications


def get_nat_from_instances(instances):
    """
    Get a NAT instance from the list of instances
    :param instances: the list of instances
    :return: the NAT instance from that list
    """
    for instance in instances:
        name = get_instance_tag(instance, "Name")
        if name == "NAT":
            return instance
    return None


def convert_instance_to_menu_string(instance):
    """
    Convernt an instance object into menu string
    :param instance: the instance to prepare the string for
    :rtype: str
    :return: the string of the instance
    """
    additional_list = []
    string = ""
    name = get_instance_tag(instance, "Name")
    if instance.private_ip_address is not None and instance.private_ip_address != "":
        additional_list.append("Private Ip: %s" % instance.private_ip_address)
    if instance.public_ip_address is not None and instance.public_ip_address != "":
        additional_list.append("Public Ip: %s" % instance.public_ip_address)
    public_domain = get_instance_tag(instance, "Public Domain")
    if public_domain is not None and public_domain != "":
        public_domain = "Public Domain: %s" % public_domain
        additional_list.append(public_domain)
    for additional in additional_list:
        if not string:
            string = "(%s" % additional
        else:
            string = "%s, %s" % (string, additional)
    if len(additional_list) == 0:
        return name
    else:
        string = "%s)" % string
        string = "%s %s" % (name, string)
        return string


def get_instance_tag(instance, key):
    """
    Get instance tag
    :param boto3.ec2 instance: the instance to get the name for
    :param str key the key of the tag
    :rtype: str
    :return: the name of the instance or None if no name was defined
    """
    tags = instance.tags
    for tag in tags:
        if tag.get("Key") == key:
            return tag.get("Value")
    return None


def filter_instances_by_tag(instances, key, value):
    """
    filter a list of instances according to a tag value
    :param list instances: the list of instances to filter
    :param str key: the key to filter the instance according to
    :param str value: the value of the key
    :rtype: list
    :return: a filtered list of instances
    """
    filtered_instance = []
    for instance in instances:
        tags = instance.tags
        for tag in tags:
            if tag.get("Key") == key and tag.get("Value") == value:
                filtered_instance.append(instance)
    return filtered_instance


def connect_to_instance(instances, index, command=None):
    """
    Connect to an ec2 instance.
    This will connect directly to the ec2 or use the NAT instance as needed
    It will launch an ssh session to the instance
    :param instances: the list of instance from which you want to connect to the instance
    :param index:  the index of the instance you want to connect to
    """
    instance = instances[index]
    nat_instance = get_nat_from_instances(instances)
    if nat_instance is None:
        start_ssh_session(instance, "ubuntu", instance.key_name, command)
    elif instance == nat_instance:
        start_ssh_session(instance, "ec2-user", instance.key_name, command)
    else:
        start_nat_ssh_session(instance, "ubuntu", nat_instance, "ec2-user", instance.key_name, command)


def start_ssh_session(instance, user, key_name, command=None):
    """
    Starts an ssh session to an instance
    :param instance: the instance to start the session to
    :param nat: optional nat instance to connect through
    """
    key_pair_path = load_key_pair(key_name)
    ssh_command = "ssh -i '%s' %s@%s" % (
        key_pair_path, user, instance.public_ip_address)
    if command is not None:
        ssh_command = '%s "%s"' % (ssh_command, command)
        print "Connecting to %s instance and running command" % get_instance_tag(instance, "Name")
    else:
        print "Connecting to %s instance" % get_instance_tag(instance, "Name")
    key_error = "Permission denied (publickey)"
    call = Popen(ssh_command, shell=True, stderr=PIPE)
    stdout, stderr = call.communicate()
    if key_error in stderr:
        config_file.remove_parameter("key_pairs", key_name)
        raw_input("Error loading key, please make sure the key and user are correct. Click enter to continue")


def start_nat_ssh_session(instance, instance_user, nat_instance, nat_user, key_name, command=None):
    """
    Starts an ssh session to an instance through NAT instance
    :param instance: the instance to connect to
    :param instance_user:  the instance user to connect with
    :param nat_instance: the nat instance to connect to
    :param nat_user: the nat user to connect with
    :param key_name: the key_pair name
    """
    key_pair_path = load_key_pair(key_name)
    ssh_command = "ssh -A -t -i '%s' %s@%s" % (key_pair_path, nat_user, nat_instance.public_ip_address)
    tunnel_command = "ssh %s@%s" % (instance_user, instance.private_ip_address)
    if command is not None:
        ssh_command = "%s '%s \"%s\"'" % (ssh_command, tunnel_command, command)
        print "Connecting to %s instance and running command" % get_instance_tag(instance, "Name")
    else:
        ssh_command = "%s %s" % (ssh_command, tunnel_command)
        print "Connecting to %s instance" % get_instance_tag(instance, "Name")
    key_error = "Permission denied (publickey)"
    call = Popen(ssh_command, shell=True, stderr=PIPE)
    stdout, stderr = call.communicate()
    if key_error in stderr:
        config_file.remove_parameter("key_pairs", key_name)
        raw_input("Error loading key, please make sure the key and user are correct. Click enter to continue")


def pull_git_branch(instances, index, branch="development"):
    """
    Pull a git branch of an instance
    :param insntaces: the instance to pull the branch for
    :param index: the index of the instance
    :param branch: the name of the branch to pull, development is default
    """
    instance = instances[index]
    username = config_file.get_parameter("git", "username")
    password = config_file.get_parameter("git", "password")
    if username is None:
        username = raw_input("Please enter username to use with your git account\n")
        config_file.add_parameter("git", "username", username)
    if password is None:
        password = raw_input("Please enter password to use with your git account\n")
        config_file.add_parameter("git", "password", password)
    user_pass = "%s:%s" % (username, password)
    remote_repository = get_instance_tag(instance, "Remote Repository")
    remote_repository = "https://%s@%s" % (user_pass, remote_repository)
    local_repository = get_instance_tag(instance, "Local Repository")
    git_command_1 = "sudo git --git-dir=%s/.git --work-tree=%s/ checkout -b %s" % (
        local_repository, local_repository, branch)
    git_command_2 = "sudo git --git-dir=%s/.git --work-tree=%s/ checkout %s" % (
        local_repository, local_repository, branch)
    git_command_3 = "sudo git --git-dir=%s/.git --work-tree=%s/ pull --no-edit %s %s" % (
        local_repository, local_repository, remote_repository, branch)

    command = "%s; %s; %s" % (git_command_1, git_command_2, git_command_3)
    connect_to_instance(instances, index, command)


def has_repository(instance):
    """
    Check if an instance has repository defined and get receive pull requests
    :param instance: the instance to check
    :return: True if there is a repository for the instance, false otherwise
    :rtype: boolean
    """
    if get_instance_tag(instance, "Remote Repository") is not None and get_instance_tag(instance,
                                                                                        "Local Repository") is not None:
        return True
    return False


def load_key_pair(key_name):
    """
    Check if a key pair name is exists in the config file
    :param string key_name: the name of the key pair
    :param bool reset: flag to determine if to reset the config key before loading
    :return: path to key pair
    :rtype str
    """
    key_pair_path = config_file.get_parameter("key_pairs", key_name)
    if key_pair_path is None:
        print "Please define path for Key-Pair named %s" % key_name
        key_pair_path = raw_input().replace("\\", "").strip()
        config_file.add_parameter("key_pairs", key_name, key_pair_path)
    subprocess.call("ssh-add '%s'" % key_pair_path, shell=True)
    return key_pair_path


def _get_resource(name, region=None):
    """
    Get the resource for a name
    :param str name: the name of the resource
    :param str region: optional region
    :return:
    """
    credentials = aws_credentials.get_current_credentials()
    boto3.setup_default_session(aws_access_key_id=credentials["key"],
                                aws_secret_access_key=credentials["secret"],
                                region_name=region)

    return boto3.resource(name);
