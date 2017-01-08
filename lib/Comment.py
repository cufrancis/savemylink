#!/usr/bin/env python
# coding=utf-8

from lib.DB import db
import time
from lib.util import convert
from lib.define import *

class Comment(object):

    def __init__(self, link_id=1):
        self.lid = link_id
        self.db = db

    def test(self):
        self.db.r.incr('comment:count')
        self.db.r.zadd("link:comment:1", 1, int(time.time()))
        self.db.r.zadd("link:comment:1", 2, int(time.time()))
        comment = dict(
            fid=0,
            content='This is irst comment',
            author=0,
            time=int(time.time())
        )
        comment2 = dict(
            fid=1,
            content='This is second comment',
            author=0,
            time=int(time.time())
        )
        self.db.r.hmset("comment:comment:1", comment)
        self.db.r.hmset("comment:comment:2", comment2)

    def findAll(self):
        print("ALL")
        tmp = self.db.r.zrange('link:comment:1', 0, -1, True)
        all_c = []
        for k in tmp:
            all_c.append(int(bytes.decode(k)))

        comments = []
        for k in all_c:
            tmp = convert(self.db.r.hgetall('comment:comment:{id}'.format(id=k)))
            #print(tmp)
            if tmp['fid'] != '0':
                tmp['father'] = convert(self.db.r.hgetall('comment:comment:{id}'.format(id=tmp['fid'])))
            comments.append(tmp)

        #print(comments)
        return comments

#        for k in comments:
#            if k['fid'] != '0':


comment = Comment()

#comment.test()
comments = comment.findAll()

print(comments[0])
