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
# ### TODO

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

############## UNIT TEST results #################################

print(f"{passed_test} / {nbr_test} tests passed")
