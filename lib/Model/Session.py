#!/usr/bin/env python
# coding=utf-8

import redis

class Session(object):
    outtime = 0

    def __init__(self, host, port, db=0, password=None, charset='utf-8'):
        self.pool = redis.ConnectionPool(host=host, port=port, password=password)
        self.r = redis.Redis(connection_pool=self.pool)
        #self.r = redis.StrictRedis(host, port, db)

    def set(self, key, value, outtime=0):
        result =  self.r.set(key, value)
        if outtime != 0:
            self.r.expire(key, outtime)
        return result

    def get(self, key):
        return self.r.get(key)

    def delete(self, key):
        return self.r.delete(key)

    def save(self):
        pass

    def keys(self):
        return self.r.keys()

    def dbsize(self):
        return self.r.dbsize()

    def flushdb(self):
        return self.r.flushdb()

session = Session(host='localhost', port=6379)

name = 'llnhhy'
session.set('account:{id}:name'.format(id=1), 'llnhhy')
session.set('account:{name}:id'.format(name='llnhhy'), 1)
session.r.sadd('account:userlist', id)


user_id = session.get('account:{name}:id'.format(name=name))
user = session.get('account:{id}:name'.format(id=int(user_id)))

session.set('item.1', 'attack:10,max_hp:20')
item_1 = str(session.get('item.1'), encoding='utf-8')


session.r.hset('item', '1:desc', 'This is desc')
session.r.hset('Item:1:task', 'id', 1)
key = session.r.hgetall('Item')
#key = str(session.r.hgetall('Item'), encoding='utf-8')
print(key['1:desc'])
