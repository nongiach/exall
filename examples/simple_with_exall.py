#!/usr/bin/env python3

import exall
import os
from subprocess import check_call, CalledProcessError
import subprocess
import inspect

################### unlink example ############################

@exall.exall(os.unlink, FileNotFoundError, exall.ignore)
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

@exall.exall(check_call, FileNotFoundError, exall.print_warning)
def test_check_call():
    print("check_call here")
    # tata = exall.do_exall(check_call, FileNotFoundError, exall.print_warning)
    # print(inspect.getargspec(tata))
    # print(inspect.getargspec(check_call))
    # check_call.__code__ = tata.__code__
    check_call("ll")
    print("do something else")
    print("isn't it beautiful ?")

test_check_call()

################## mkdir example #############################

""" If one of the mkdir fails then print an error and exit the program """
""" here we setup a global behaviour """
os.mkdir = exall.do_exall(os.mkdir, FileExistsError, exall.print_error)

def mkdir_tata():
    os.mkdir("/tata")

mkdir_tata()
os.mkdir("/tmp/ok")

### Setup your own callback and multiple exception handling ####

def on_timeout(exception):
    print("WARNING: socket timeout")
    # ...
    # do some clean up
    # reconnnect..

# os.create_connection("test", 4242)
