#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

class DB(object):
    def __init__(self, host='localhost', port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.r = redis.Redis(connection_pool=self.pool)

    def isInside(self):
        pass

    def set(self, key, value, outtime=0):
        result = self.r.set(key, value)
        if outtime != 0:
            self.r.expire(key, outtime)

        return result

    def hset(self, key, field, value):
        try:
            result = self.r.hset(key, field, value)
            return result
        except:
            return 0

    def hget(self, key, field, convert=True):
        result = self.r.hget(key, field)

        if convert:
            try:
                return bytes.decode(result)
            except:
                return None

    def get(self, key, convert=True):
        if convert:
            try:
                result = self.r.get(key)
                return bytes.decode(result)
            except:
                return None

    def flushdb(self):
        pass
        #return self.r.flushdb()

    def _bytes2str(self, byte, doit=True):
        if not isinstance(byte, bytes):
            return byte

        if doit:
            return bytes.decode(byte)
        else:
            return byte

db = DB(host = 'localhost', port = 6379)

