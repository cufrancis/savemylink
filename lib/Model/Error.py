#!/usr/bin/env python
# coding=utf-8

class Error(Exception):
    """
    Base class for exception in this module.
    """
    pass

class LoginError(Error):
    def __init__(self, value):
        self.value = value
