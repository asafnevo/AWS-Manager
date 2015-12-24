#!/usr/bin/python

import os

script_name = "AWS Manager"

config_file_name = os.path.join(os.path.expanduser('~'), ".aws_manager_config")

default_git_branch = "development"

pip_installation = "'%s/%s/scripts/get-pip.py'" % (os.path.dirname(os.path.realpath(__file__)), "..")
