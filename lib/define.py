#!/usr/bin/env python
# coding=utf-8

# Account

ACCOUNT_COUNT = 'account:count' # String
ACCOUNT_USERLIST = 'account:userlist' # set
ACCOUNT_EMAIL = 'account:email:{email}' # String
ACCOUNT_LAST_LOGIN = 'account:lastlogin:{uid}' # hash
ACCOUNT_LOGIN = 'account:login:set' # zset key=uid, value=login time
ACCOUNT_AVATARS = 'account:avatars:{uid}'
ACCOUNT_USER = 'account:user:{uid}' # hash
ACCOUNT_LINK = 'account:link:{uid}' #Set

SESSION_USER = 'session:{uid}' # String
# Link
LINK_COUNT = 'link:count' # string
LINK_ALL = 'link:all:set' # set
#LINK_VISIT = 'link:visit:zset' #zset
LINK = 'link:info:{link_id}' # hash
LINK_SORT_BYVISIT = 'link:sort:visit' #zset
LINK_SORT_BYTIME = 'link:sort:time' #zset
LINK_COMMENT = 'link:comment:{lid}' #zset

# comment
COMMENT_COUNT = 'comment:count' # String
COMMENT = 'comment:comment:{cid}' #hash
