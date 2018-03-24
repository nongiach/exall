#!/usr/bin/env python3

import exall

### Home made test unit functions
passed_test = 0
nbr_test = 0

def shouldnt_raise(fn):
    global nbr_test, passed_test
    nbr_test += 1
    try:
        fn()
        passed_test += 1
    except Exception as e:
        print("{fn.__name__} Failed: {e}".format(fn=fn, e=e))

def should_raise(fn, exception):
    global nbr_test, passed_test
    nbr_test += 1
    try:
        fn()
        print("{fn.__name__} Failed".format(fn=fn))
    except exception:
        passed_test += 1

### catch exception from an nested module calling the source function
### TODO
### catch exception with src=a_decorated_fonction
### TODO
### catch exception with src=local_fonction

def raise_file_not_found_error():
    raise FileNotFoundError

@exall.exall(raise_file_not_found_error, FileNotFoundError, exall.ignore)
def test_local_function():
    raise_file_not_found_error()

should_raise(raise_file_not_found_error, FileNotFoundError)
shouldnt_raise(test_local_function)

# ### catch exception with src=builtins (os/posix and local builtins)
# ### 

import os

@exall.exall(os.unlink, FileNotFoundError, exall.ignore)
def exall_os_unlink():
    os.unlink("this_file_doesn't exist")

def os_unlink():
    os.unlink("this_file_doesn't exist")

should_raise(os_unlink, FileNotFoundError)
shouldnt_raise(exall_os_unlink)

@exall.exall(open, FileNotFoundError, exall.ignore)
def exall_local_open():
    open("this_file_doesn't exist")

def local_open():
    open("this_file_doesn't exist")

should_raise(local_open, FileNotFoundError)
shouldnt_raise(exall_local_open)

# ### catch exception with src=the_current_function/context (when no src is specified)
# ### TODO
# ### catch exception on instancied object (exemple socket)
# ### 

import socket

def socket_connect():
    s = socket.create_connection(("google.com", 80))
    s.settimeout(0.001)
    s.recv(4096)

@exall.exall(socket.socket.recv, socket.timeout, exall.ignore)
def exall_socket_connect():
    socket_connect()

should_raise(socket_connect, socket.timeout)
shouldnt_raise(exall_socket_connect)

# ### catch exception with to nested exall
# ### 
# ### catch exception with src= partial fonction ?
# ### 
# ### catch exception with src=import as
# ### 
# ### catch exception with src= from taat import tata as tutu
# ################### unlink example ############################
#
# @exall.exall(os.unlink, FileNotFoundError, exall.ignore)
# def unlink_example():
#     print("test")
#     os.unlink("this_file_doesnt_exist_exception_is_ignored")
#     os.unlink("this_file_doesnt_exist_exception_is_ignored")
#     os.unlink("this_file_exists_and_will_be_deleted")
#
# unlink_example()
#
#
#
# ################### subprocess example ########################
#
# """ It's ok if check_call("toto") fails, we only need to print a warning 
# and continue the program.
# Here we handle two different exceptions.
# """
#
# @exall.exall(check_call, FileNotFoundError, exall.print_warning)
# def test_check_call():
#     print("check_call here")
#     # tata = exall.do_exall(check_call, FileNotFoundError, exall.print_warning)
#     # print(inspect.getargspec(tata))
#     # print(inspect.getargspec(check_call))
#     # check_call.__code__ = tata.__code__
#     check_call("ll")
#     print("do something else")
#     print("isn't it beautiful ?")
#
# test_check_call()
#
# ################## mkdir example #############################
#
# """ If one of the mkdir fails then print an error and exit the program """
# """ here we setup a global behaviour """
# os.mkdir = exall.do_exall(os.mkdir, FileExistsError, exall.print_error)
#
# os.mkdir("/tata")
# os.mkdir("/tmp/ok")
#
# ### Setup your own callback and multiple exception handling ####
#
# def on_timeout(exception):
#     print("WARNING: socket timeout")
#     # ...
#     # do some clean up
#     # reconnnect..
#
# # os.create_connection("test", 4242)

############## UNIT TEST results #################################

print(f"{passed_test} / {nbr_test} tests passed")
