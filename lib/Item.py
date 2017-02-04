#!/usr/bin/env python
# coding=utf-8

from DB import db

# item Base class
class item(object):

    def __init__(self, id):
        self.db = db
        self.id = id
        self.key = 'item:{id}'.format(id=self.id)

    #def __getattr__(self, field):
     #   return self._handle(field)
        #print("key:"+self.key)

    #def __setattr__(self, field, value):
     #   print("Setattribute:"+field+"|"+value)

    # set redis
    def _set(self, field, value):
        #key = '{prefix}{key}'.format(prefix=self.prefix, key=key)
        return self.db.hset(self.key, field, value)

    # get redis
    def _get(self, field):
        # compose key, prefix and key .like as Item:{id}:{key}
        #key = '{prefix}{key}'.format(prefix=self.prefix, key=key)
        return self.db.hget(self.key, field)

    def _handle(self, field, value=None):
        #key = '{prefix}{key}'.format(prefix=self.prefix, key=key)

        if value is None:
            return self._get(field)
        else:
            return self._set(field, value)

    def name(self, value=None):
        return self._handle('name', value)

    def desc(self, value=None):
        return self._handle('desc', value)

    def image(self, value=None):
        return self._handle('image', value)

    def price(self, value=None):
        return self._handle('price', value)

    def attack(self, value=None):
        return self._handle('attack', value)

    def defense(self, value=None):
        return self._handle('defense', value)

i1 = item(1)

print(db.r.keys('item*'))
