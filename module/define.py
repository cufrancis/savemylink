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

# User (New action)
USER_NICKNAME = 'user:{nickname}' # string key
NICKNAME = 'nickname' # set 存所有nickname， 查重用
EMAIL = 'email' # set 存所有email，查重用



# 用户收藏夹
ACCOUNT_FAVOURITE = 'account:{uid}:favourite' # set，存放用户所拥有的收藏夹的id
FAVOURITE_INFO = 'favourite:{fid}:info' # hash， 存放收藏夹的所有信息，如收藏夹名字(name)，收藏夹创建日期(created_at), 收藏夹作者(author)
FAVOURITE = 'favourite:{fid}' # set, 存放收藏夹所包含的link id
FAVOURITE_COUNT = 'favourite:count' # string 自增favourite id
FAVOURITE_PUBLIC = 'favourite:public' # set, 存放公开的收藏夹id，用户新建收藏夹时默认公开

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
