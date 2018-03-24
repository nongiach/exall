#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @chaign_c

from contextlib import ContextDecorator
import functools
import inspect
import builtins

# ==========================================================
# Exception manager based on decorator/context/callback.
# Using this will separate code logic from error handling, 
# the goal would be to reduce code duplication and ease development.
# ==========================================================

def do_exall(fn, exceptions, callback):
    """ Call *callback* when *exception* is raised by the function *fn* """
    if not isinstance(exceptions, tuple):
        exceptions = (exceptions,)
    def new_function(*args, **kwargs):
        # TODO: can you delete this first line ? .. if context is shared between try and finally ..
        ret_value = None
        try:
            return fn(*args, **kwargs)
        except exceptions as e:
            callback(e)
    new_function.__wrapped__ = fn
    return new_function

def the_real_module(module):
    if module == "posix":
        return "os"
    return module

class exall(ContextDecorator):
    """
        A context and decorator for do_exall.
        Call *callback* when *exception* is raised by the function *fn*
    """
    def __init__(self, fn, exception, callback):
        super().__init__()
        self.fn = fn
        self.decorator = do_exall(self.fn, exception, callback)
        self.locals = inspect.currentframe().f_back.f_locals

    def __enter__(self):
        # print("Exall.enter {s.fn.__module__}.{s.fn.__name__}".format(s=self))
        self.fn_module = __import__(the_real_module(self.fn.__module__))
        setattr(self.fn_module,  self.fn.__name__, self.decorator)
        if self.fn.__name__ in self.locals and self.locals[self.fn.__name__] is self.fn:
            self.locals[self.fn.__name__] = self.decorator
        elif hasattr(builtins, self.fn.__name__) and getattr(builtins, self.fn.__name__) is self.fn:
            setattr(builtins, self.fn.__name__, self.decorator)

    def __exit__(self, *exc):
        setattr(self.fn_module,  self.fn.__name__, self.fn)
        if self.fn.__name__ in self.locals and self.locals[self.fn.__name__] is self.decorator:
            self.locals[self.fn.__name__] = self.fn
        elif hasattr(builtins, self.fn.__name__) and getattr(builtins, self.fn.__name__) is self.decorator:
            setattr(builtins, self.fn.__name__, self.fn)
        # print("Exall.exit {s.fn.__module__}.{s.fn.__name__}".format(s=self))

# =========================================================
# Callbacks: several basic way of handling exception
# =========================================================

import traceback
from pprint import pprint
import os

def print_traceback(exception):
    print(exception)
    pprint(traceback.extract_stack()[:-2])

class Color:
    orange = "\x1B[33m"
    red = "\x1B[31m"
    normal = "\x1B[0m"
def print_warning(exception):
    location = traceback.extract_stack()[-3]
    print("{c.orange}WARNING{c.normal}: {l.filename}:{l.lineno} {l.line} => {c.orange}{exception}{c.normal} ".format(
        exception=exception, l=location, c=Color))

def ignore(exception):
    pass

def print_error(exception):
    # pprint(traceback.extract_stack()[:-2])
    locations = traceback.extract_stack()[:-2]
    for i, location in enumerate(locations):
        print("{c.red}{i}=>{c.normal} {l.filename}:{l.lineno} {l.line}".format(
            exception=exception, l=location, i=i * " ", c=Color))
    print("{c.red}ERROR{c.normal}: {exception}".format(exception=exception, c=Color))
    os._exit(1)
