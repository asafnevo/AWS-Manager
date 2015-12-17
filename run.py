#!/usr/bin/python


import global_functions
import botocore

try:
    global_functions.init_and_run()
except KeyboardInterrupt:
    print "\nBye Bye!"
    exit()
except botocore.exceptions.ClientError:
    print "You have no permission to perform this action on AWS using these credentials."
    print "Please change your credentials in the Main Menu"
    exit()
