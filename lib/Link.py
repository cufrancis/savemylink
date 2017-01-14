#!/usr/bin/env python
# coding=utf-8

from lib.DB import db
from lib.define import *
import time
import datetime
from lib.util import convert
from lib.Comment import Comment
from lib.Account import Account

class Link(object):
    db = db

    def __init__(self, link_id=0, db=db):
        self.link_id = link_id
        self.db = db

    @classmethod
    def create(self, link):
        pass

    @classmethod
    def delete(self, link_id=0):
        pass

    @classmethod
    def save(self):
        pass


    def _sort_by_time(self):
        lst = self.db.r.zrevrange(LINK_SORT_BYTIME, 0, -1)
        tmp = []
        for key in lst:
            tmp.append(bytes.decode(key))
        lst = tmp

        return lst

    @classmethod
    def getAll(cls):

        lst = cls._sort_by_time(cls)
        result = []

        for key in lst:
            tmps = convert(cls.db.r.hgetall(LINK.format(link_id=key)))
            #tmps = convert(tmps)
            tmps['visit'] = int(cls.db.r.zscore(LINK_SORT_BYVISIT.format(link_id=key), key))
            print(tmps)
            tmps['id'] = key

            #tmps['created_at'] = datetime.datetime.fromtimestamp(int(tmps['created_at'])).strftime("%Y-%m-%d %H:%M:%S")
            #tmps['author_name'] = cls.db.r.hget(ACCOUNT_USER.format(uid=tmps['author']), 'email')
            tmps['comments'] = cls.getComments(cls, lid=tmps['id'])
            result.append(tmps)

        return result

    # return all comments
    def getComments(self, lid = 0):
        if lid == 0:
            lid = self.link_id
        com = Comment(lid)
        return com.findAll()

    def getAuthor(self):
        print(Account())
        return Account(self.author_id)
#        return "getAuthor"

    @classmethod
    def test(cls):
        return cls.db

    @classmethod
    def add(cls, info):

        link_id= cls.db.r.incr(LINK_COUNT)

        info.setdefault('url', None)
        info.setdefault('created_at', None)
        info.setdefault('title', None)
        info.setdefault('author', None)
        info.setdefault('updated_at', None)

        cls.db.r.hmset(LINK.format(link_id=link_id), info)
        cls.db.r.sadd(LINK_ALL, link_id)
        cls.db.r.zadd(LINK_SORT_BYTIME.format(link_id=link_id), link_id, int(time.time()))
        cls.db.r.zadd(LINK_SORT_BYVISIT.format(link_id=link_id),link_id, 0)
        cls.db.r.sadd(ACCOUNT_LINK.format(uid=info['author']), link_id)

#        print(link_id)
        return link_id


    def __getattr__(self, field):
        attribute = ['icon', 'url', 'title', 'created_at', 'updated_at']

        action = ['comments']

        if field in attribute:
            return self._get(field)
        elif field == 'comments':
            return self.getComments()
        elif field == 'author':
            return self.getAuthor()
        elif field == 'author_id':
            return self._get('author')
        elif field == 'all':
            return self.getLink()
        else:
            return None

    def _get(self, field):
        key = LINK.format(link_id=self.link_id)
        result = self.db.hget(key, field)
        return result

    # Bytes to str
    def _bytes2str(self, byte, doit=True):
        if not isinstance(byte, bytes):
            return byte

        if doit == True:
            return bytes.decode(byte)
        else:
            return byte
