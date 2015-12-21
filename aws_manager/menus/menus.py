#!/usr/bin/python
"""
Module for showing all the relevant module according to the user choices
"""

import aws
import subprocess;
import settings;
import functions

_instances = None
""":rtype list instances of ec2"""


def show_credential_setup_menu():
    """
    Show the menu for adding credentials files
    """
    subprocess.call("clear")
    print "Let's setup some initial settings:";
    aws_file_path = raw_input("What is the path to your AWS Access Key?\n");
    aws.save_path_to_config(aws_file_path)
    credentials = aws.load_from_config()
    if credentials is None:
        print "User credentials are invalid. Make sure you have the right path and permissions for the file"
        exit();
    show_main_menu()


def show_main_menu():
    """
    Show the script main menu
    """
    credentials = aws.get_current_credentials()
    subprocess.call("clear")
    print "Welcome to", settings.script_name
    print "AWS User Key:", credentials["username"]
    print ""
    print "Please Choose an option from the menu:"
    print "1. EC2 Instances Management"
    print "2. Change AWS credentials settings"
    print "3. Uninstall Pip & Boto3"
    print "4. Exit"
    try:
        main_menu_options(int(raw_input()))()
    except ValueError:
        show_main_menu()


def main_menu_options(i):
    """
    The main menu options process
    :param int i: the index of the option
    :return:
    """
    return {
        1: show_region_menu,
        2: show_credential_setup_menu,
        3: functions.uninstall_pip,
        4: exit
    }.get(i, show_main_menu)


def show_region_menu(is_no_instances=False):
    global _instances
    """
    Show the region menu
    :param boolean is_no_instances: default is False. call this method with True to show that there were no instances in
        the selected region
    """
    subprocess.call("clear")
    if is_no_instances:
        print "Sorry, no instances were found in this region\n"

    print "Please choose the region of the EC2 instance you wish to connect to:";
    print "1. US East (N. Virginia)";
    print "2. US West (Oregon)";
    print "3. US West (N. California)";
    print "4. EU (Ireland)";
    print "5. EU (Frankfurt)";
    print "6. Asia Pacific (Singapore)";
    print "7. Asia Pacific (Sydney)";
    print "8. Asia Pacific (Tokyo)";
    print "9. South America (Sao Paulo)";
    print "10. Back";
    try:
        chosen_region = region_menu_options(int(raw_input()))
        if isinstance(chosen_region, str):
            print "Loading instances..."
            _instances = aws.load_ec2_instances(chosen_region)
            if _instances is None:
                show_region_menu(True)
            else:
                show_environments_menu()
        else:
            chosen_region()
    except ValueError:
        show_region_menu()


def region_menu_options(i):
    """
    region menu options
    :param int i: the index the user chosen
    :return:
    """
    return {
        1: "us-east-1",
        2: "us-west-2",
        3: "us-west-1",
        4: "eu-west-1",
        5: "eu-central-1",
        6: "ap-southeast-1",
        7: "ap-southeast-2",
        8: "ap-northeast-1",
        9: "sa-east-1",
        10: show_main_menu
    }.get(i, show_region_menu)


def show_environments_menu():
    global _instances
    """
    Show the environments menu
    :param list instances: of EC2 instance to filter the environment from
    """
    subprocess.call("clear")
    print "Please choose the environment your instance is located in:"
    environments = aws.get_environments_from_instances(_instances)
    for i, environment in enumerate(environments):
        print "%d. %s" % (i + 1, environment)
    print "%d. Back" % (len(environments) + 1)
    chosen_index = int(raw_input());
    try:
        chosen_environment = environments[chosen_index - 1]
        show_applications_menu(chosen_environment)
    except ValueError:
        show_environments_menu()
    except IndexError:
        if chosen_index == len(environments) + 1:
            show_region_menu()
        else:
            show_environments_menu()


def show_applications_menu(environment):
    global _instances
    """
    Show the application menu
    :param list instances: of EC2 instance to filter the environment from
    :param str environment: the name of the environment the user chosen
    """
    subprocess.call("clear")
    print "Please choose the application your instance is part of:"
    filtered_instance = aws.filter_instances_by_tag(_instances, "Environment", environment)
    applications = aws.get_applications_from_instances(filtered_instance)
    for i, application in enumerate(applications):
        print "%d. %s" % (i + 1, application)
    print "%d. Back" % (len(applications) + 1)
    chosen_index = int(raw_input())
    try:
        chosen_application = applications[chosen_index - 1]
        show_instances_menu(filtered_instance, environment, chosen_application)
    except ValueError:
        show_applications_menu(environment)
    except IndexError:
        if chosen_index == len(applications) + 1:
            show_environments_menu()
        else:
            show_applications_menu(environment)


def show_instances_menu(instances, environment, application):
    global _instances
    """
    Show the instance list
    :param list instances: the list of instances from AWS
    :param str environment: the environment we are showing
    :param str application: the application the user chose
    :return:
    """
    subprocess.call("clear")
    print "Please choose the instance you want to manage:"
    filtered_instances = aws.filter_instances_by_tag(instances, "Application", application)
    for i, instance in enumerate(filtered_instances):
        print "%d. %s" % (i + 1, aws.convert_instance_to_menu_string(instance))
    print "%d. Back" % (len(filtered_instances) + 1)
    chosen_index = int(raw_input())
    try:
        show_instance_manager_menu(filtered_instances, chosen_index - 1, environment, application)
    except ValueError:
        show_instances_menu(_instances, environment, application)
    except IndexError:
        if chosen_index == len(filtered_instances) + 1:
            show_applications_menu(environment)
        else:
            show_instances_menu(_instances, environment, application)


def show_instance_manager_menu(instances, index, environment, application):
    global _instances
    """
    Menu for a specific instance
    :param list instances: the EC2 AWS instances list
    :param int index: the index of the current instance in the list
    :param str environment: the environment the user chose
    :param str application: the application the user chose
    :return:
    """
    subprocess.call("clear")
    instance = instances[index]
    i = 1
    print "Instance: %s" % (aws.get_instance_tag(instance, "Name"))
    print "Please choose what you want to do:"
    print "%d. Connect" % i
    i += 1
    if aws.has_repository(instance):
        print "%d. Pull git branch" % i
        i += 1
    print "%d. Back" % i
    chosen = int(raw_input())
    if chosen == i:
        show_instances_menu(_instances, environment, application)
    elif chosen == 1:
        aws.connect_to_instance(instances, index)
        show_instance_manager_menu(instances, index, environment, application)
    elif chosen == 2:
        branch = raw_input("Please specify branch or press enter for default (development branch)\n")
        if branch == "":
            aws.pull_git_branch(instances, index)
        else:
            aws.pull_git_branch(instances, index, branch)
        raw_input("Press enter to continue")
        show_instance_manager_menu(instances, index, environment, application)
    else:
        show_instance_manager_menu(instances, index, environment, application)
