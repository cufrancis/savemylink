#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("./")

import app.Handler.IndexHandler as Index
import app.Handler.UserHandler as User
import app.Handler.LinkHandler as Link
import app.Handler.CommentHandler as Comment
import app.Handler.AdminHandler as Admin
import app.Handler.FavouriteHandler as Favourite

url = [
    (r'/', Index.index),
    # account
    (r'/login', User.login),
    (r'/register', User.register),
    (r'/logout', User.logout),
    (r'/user/(\d+)', User.index),
    (r'/user/(\d+)/favourite', User.favourite),

    (r'/user/favourite/add/(\d+)', User.add_favourite),

    # favourite
    (r'/favourite', Favourite.all),
    (r'/favourite/create', Favourite.create),
    (r'/favourite/(\d+)', Favourite.index),
    (r'/favourite/(\d+)/addlink/(\d+)', Favourite.addlink),

    # link
    (r'/link/(\d+)', Link.index),
    (r'/link/add', Link.create),
    (r'/link/delete/(\d+)', Link.delete),
    (r'/link/(\d+)/vote_up', Link.vote_up),
    (r'/link/(\d+)/vote_down', Link.vote_down),

    # comment
    (r'/comment/(\d+)/reply', Comment.reply),

    # admin
    (r'/admin', Admin.index),
    (r'/admin/link', Admin.link),

    # ajax check
    (r'/user/check/nickname', User.check_nickname),
    (r'/user/check/email', User.check_email),

    (r'/link/check/url', Link.check_url),

    (r'/ajax/get/title', Link.get_title),
    (r'/ajax/link/vote_up', Link.vote_up),
    (r'/ajax/link/vote_down', Link.vote_down),

    # 获取链接信息的api
    (r'/api/link',Link.api_link),

    # admin.link
    #(r'/admin/link/(\d+)', Link.index)
]
