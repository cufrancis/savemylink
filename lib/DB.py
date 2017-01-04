#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

class DB(object):
    def __init__(self, host='localhost', port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.r = redis.Redis(connection_pool=self.pool)

    def set(self, key, value, outtime=0):
        result = self.r.set(key, value)
        if outtime != 0:
            self.r.expire(key, outtime)
        return result

    def hset(self, key, field, value):
        result = self.r.hset(key, field, value)
        print(type(result))

    def hget(self, key, field):
        result = self.r.hget(key, field)
        #result = bytes.decode(result)
        return result

    def get(self, key):
        result = self.r.get(key)
        return bytes.decode(result)

    def flushdb(self):
        return self.r.flushdb()

db = DB(host = 'localhost', port = 6379)

