#!/usr/bin/env python3

from exall import exall, do_exall, print_warning, ignore, print_error
import os
from subprocess import check_call, CalledProcessError
import subprocess

################### unlink example ############################

""" if os.unlink raises a FileNotFoundError then ignore callback will be called
    and the execution of the function will carry on.
"""
@exall(os.unlink, FileNotFoundError, ignore)
def unlink_example():
    print("test")
    os.unlink("this_file_doesnt_exist_exception_is_ignored")
    os.unlink("this_file_doesnt_exist_exception_is_ignored")
    os.unlink("this_file_exists_and_will_be_deleted")

unlink_example()



################### subprocess example ########################

""" It's ok if check_call("toto") fails, we only need to print a warning 
and continue the program.
Here we handle two different exceptions.
"""

with exall(check_call, (CalledProcessError, FileNotFoundError), print_warning):
    check_call("ll")
    print("do something else")
    print("isn't it beautiful ?")

################## mkdir example #############################

""" If one of the mkdir fails then print an error and exit the program """
""" here we setup a global behaviour """
os.mkdir = do_exall(os.mkdir, FileExistsError, print_error)

def do_mkdirs():
    os.mkdir("/tmp")
    os.mkdir("/tmp/ok")

do_mkdirs()


### Setup your own callback and multiple exception handling ####

def on_timeout(exception):
    print("WARNING: socket timeout")
    # ...
    # do some clean up
    # reconnnect..

# os.create_connection("test", 4242)
