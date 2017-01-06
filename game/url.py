#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("./")

import game.Handler.IndexHandler as Index
import game.Handler.UserHandler as User
import game.Handler.LinkHandler as Link

url = [
    (r'/', Index.index),
    # account
    (r'/login', User.login),
    (r'/register', User.register),
    (r'/logout', User.logout),

    # link
    (r'/link/add', Link.create),
]
