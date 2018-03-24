#!/usr/bin/env python3

import os
from subprocess import check_call, CalledProcessError
import contextlib
import sys

################### unlink example ############################

""" if os.unlink raises a FileNotFoundError then ignore callback will be called
    and the execution of the function will carry on.
"""
def unlink_example():
    """ We want all unlink to be executed even if the first one fails"""
    with contextlib.suppress(FileNotFoundError):
        os.unlink("this_file_doesnt_exist_exception_is_ignored")
    with contextlib.suppress(FileNotFoundError):
        os.unlink("this_file_doesnt_exist_exception_is_ignored")
    with contextlib.suppress(FileNotFoundError):
        os.unlink("this_file_exists_and_will_be_deleted")

unlink_example()

################### subprocess example ########################

""" It's ok if check_call("toto") fails, we only need to print a warning 
and continue the program.
Here we handle two different exceptions.
"""
try:
    check_call("toto")
except (CalledProcessError, FileNotFoundError):
    print("WARNING: execution of toto failed")
print("do something else")
print("There must be a better way")

################## mkdir example #############################

""" If one of the mkdir fails then print an error and exit the program """
try:
    os.mkdir("/tata")
    os.mkdir("/tmp/ok")
except FileExistsError:
    print("ERROR: mkdir failed")
    sys.exit(1)

### Setup your own callback and multiple exception handling ####

def on_timeout(exception):
    print("WARNING: socket timeout")
    # ...
    # do some clean up
    # reconnnect..

