#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import exall

import os
import subprocess

@exall.exall(subprocess.check_call, subprocess.CalledProcessError, exall.ignore)
def tata():
    subprocess.check_call("ll", shell=True)

tata()

@exall.exall(os.unlink, FileNotFoundError, exall.print_warning)
def test():
    print("test")
    os.unlink("this_file_doesnt_exist_exception_is_ignored")
    os.unlink("this_file_doesnt_exist_exception_is_ignored")
    os.unlink("this_file_exists_and_will_be_deleted")

test()

# Setup a global behavior
os.mkdir = exall.do_exall(os.mkdir, FileExistsError, exall.print_error)

