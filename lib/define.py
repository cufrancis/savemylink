#!/usr/bin/env python
# coding=utf-8

# Account

ACCOUNT_COUNT = 'account:count' # String
ACCOUNT_USERLIST = 'account:userlist' # set
ACCOUNT_EMAIL = 'account:email:{email}' # String
ACCOUNT_LAST_LOGIN = 'account:{uid}:lastlogin' # hash
ACCOUNT_LOGIN = 'account:login:set' # zset key=uid, value=login time
ACCOUNT_AVATARS = 'account:{uid}:avatars'
ACCOUNT_USER = 'account:{uid}' # hash
ACCOUNT_LINK = 'account:{uid}:link' #Set

SESSION_USER = 'session:{uid}' # String

# Link
LINK_COUNT = 'link:count' # string
LINK_ALL = 'link:all:set' # set
#LINK_VISIT = 'link:visit:zset' #zset
LINK = 'link:{lid}' # hash
LINK_SORT_BYVISIT = 'link:sort:visit' #zset
LINK_SORT_BYTIME = 'link:sort:time' #zset

LINK_COMMENT = 'link:{lid}:comments' #zset
LINK_COMMENT_COUNT = 'link:{lid}:comments:set' # set, all comment id

# comment
COMMENT_COUNT = 'comment:count' # String
COMMENT = 'comment:{cid}' #hash
COMMENT_REPLY = 'comment:{cid}:reply' # list


# admin
ADMIN = 'admin' # set
