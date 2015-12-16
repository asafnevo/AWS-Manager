#!/usr/bin/python


import global_functions

try:
    global_functions.init_and_run()
except KeyboardInterrupt:
    print "\nBye Bye!"
    exit()
