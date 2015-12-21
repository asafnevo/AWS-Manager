#!/usr/bin/python

import os

script_name = "AWS Manager"

config_file_name = '.config'

pip_installation = "'%s/%s/scripts/get-pip.py'" % (os.path.dirname(os.path.realpath(__file__)), "..")
