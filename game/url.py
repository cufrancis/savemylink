#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("./")

import game.Handler.IndexHandler as Index
import game.Handler.UserHandler as User

url = [
    (r'/', Index.index),
    (r'/login', User.login),
    (r'/register', User.register),
    (r'/logout', User.logout),
]
