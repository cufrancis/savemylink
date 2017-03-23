#!/usr/bin/env python
# coding=utf-8

from module.DB import db
import time
from module.util import convert
from module.define import *
from module import Account

class Comment(object):

    def __init__(self, cid=0):
        self.cid = cid
        self.db = db

    def __getattr__(self, field):
        attributes = ['author_id', 'content', 'created_at', 'lid',]
        print("Comment.__getattr__.{field}".format(field=field))

        if field in attributes:
            return self._get(field)
        elif field == 'author':
            return self._author()
        elif field == 'reply':
            return self._reply()

    def _author(self):
        return Account(self.author_id)

    def _get(self, field):
        comment = COMMENT.format(cid=self.cid)
        print(comment)
        result = self.db.hget(comment, field)

        return result

    # return sub comment
    def _reply(self):
        comment_reply = COMMENT_REPLY.format(cid=self.cid)
        comments = self.db.smembers(comment_reply)

        result = []
        for cid in comments:
            result.append(Comment(cid))
        print("comments")
        return result

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
