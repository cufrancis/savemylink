#!/usr/bin/env python
# coding=utf-8

from module.DB import db
from module.define import *

class Favourite(object):

    db = db
    link_list = []
    value_dict = dict()
    favourite_public = FAVOURITE_PUBLIC
    favourite_count = FAVOURITE_COUNT


    def __init__(self, fid = 0):

        if not isinstance(fid, int):
            raise TypeError('Bad operand type')

        self.db = db
        self.fid = fid
        self.favourite_info = FAVOURITE_INFO.format(fid=self.fid)
        self.favourite_count = FAVOURITE_COUNT
        self.favourite = FAVOURITE.format(fid=self.fid)
        self.favourite_public = FAVOURITE_PUBLIC



    @classmethod
    def create(cls,info):
        #info = dict(
        #    name='name',
        #    created_at = 'created_at'
        #)
        favourite_count = FAVOURITE_COUNT

        fid = cls.db.r.incr(cls.favourite_count)

        favourite_info = FAVOURITE_INFO.format(fid=fid)
        cls.db.r.hmset(favourite_info, info)

        if info['public']:
            cls.db.r.sadd(cls.favourite_public, fid)

        # only return fid
        # if you want add fid to account_favourite table
        # you need run down code
        # user = Account(id)
        # account_favourite = ACCOUNT_FAVOURITE.format(uid=uid)
        # cls.db.r.sadd(account_favourite, fid)
        return fid

    @classmethod
    def public(cls):
        """
        返回所有公开的收藏夹
        """

        # 在这里可以做分页
        pub = cls.db.smembers(cls.favourite_public)

        result = []
        if pub:
            for k in pub:
                result.append(Favourite(k))
            return result
        else:
            return []

    @property
    def isPublic(self):
        public = self.db.r.sismembers(self.favourite_public, self.fid)
        return public

    @property
    def name(self):
        #favourite_info = FAVOURITE_INFO.format(fid=self.fid)
        result = self.db.r.hget(self.favourite_info, 'name')

        return result

    @property
    def author(self):
        user_id = int(self.db.hget(self.favourite_info, 'author'))
        # print(self.db.r.hgetall(self.favourite_info))
        # print(type(user_id))
        if user_id:
            from lib.Account import Account
            return Account(user_id)

    @name.setter
    def name(self, value):
        self.value_dict['name'] = value


    @property
    def created_at(self):
        #favourite_info = FAVOURITE_INFO.format(fid=self.fid)

        return self.db.r.hget(self.favourite_info, 'created_at')

    @created_at.setter
    def created_at(self, value):
        self.value_dict['created_at'] = value



    # add linkid to favourite , if not run save , the data is in buffer
    def addlink(self, lid):

        if isinstance(lid, list):
            for k in lid:
                if k not in self.link_list:
                    self.link_list.append(lid)
        else:
            lid = int(lid)
            if lid not in self.link_list:
                #self.linkid = []
                self.link_list.append(lid)

        return True
        #print(self.link_list)


    def save(self):
        # save Favourite information
        if len(self.value_dict) > 0:
            self.db.r.hmset(self.favourite_info, self.value_dict)
        # save link id into the favourite
        if len(self.link_list) > 0:
            for k in self.link_list:
                self.db.r.sadd(self.favourite, k)

        #del self.link_list[:]
        self.link_list = []
        self.value_dict = {}

        return True


    def links(self):
        # get all links in favourites,
        # return Link Class
        #"""
        favourite_links = FAVOURITE.format(fid=self.fid)

        tmp = self.db.smembers(favourite_links)

        print(tmp)
        # only return link id
        # new class in Handler's
        return tmp

        #print(tmp)

        #if len(tmp) > 0:
        #    result = []
        #    from lib.Link import Link
        #    for k in tmp:
        #        result.append(Link(k))
        #    return result
        #else:
        #    return None
