#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("./")

import app.Handler.IndexHandler as Index
import app.Handler.UserHandler as User
import app.Handler.LinkHandler as Link
import app.Handler.CommentHandler as Comment

url = [
    (r'/', Index.index),
    # account
    (r'/login', User.login),
    (r'/register', User.register),
    (r'/logout', User.logout),
    (r'/user/(\d+)', User.index),

    # link
    (r'/link/(\d+)', Link.index),
    (r'/link/add', Link.create),
    (r'/link/delete/{lid}', Link.delete),

    # comment
    (r'/comment/(\d+)/reply', Comment.reply),

]
