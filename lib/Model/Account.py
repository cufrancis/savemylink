#!/usr/bin/env python
# coding=utf-8

from DB import db
import hashlib
import time
from util import convert

from define import *
import logging
LEVELS = {
    'debug':logging.DEBUG,
    'info':logging.INFO,
    'warning':logging.WARNING,
    'error':logging.ERROR,
    'critical':logging.CRITICAL
}

slat = 'password'

class Account(object):
    db = db

    def __init__(self, uid=0):
        self.db = db
        self.uid = uid
        self.key = ACCOUNT_USER.format(uid=uid)
        self.account_key = ACCOUNT_USER.format(uid=uid)

    def __getattr__(self, field):
        print("Account.__getattr__.{field}".format(field=field))

        attributes = ['email','mobile', 'nick_name', 'age', 'sex', 'password', 'desc', 'status', 'avatar']

        if field in attributes:
#            if self._get(fied)
            return self._get(field)

    def _get(self, field):
        key = ACCOUNT_USER.format(uid=self.uid)

        result = self.db.hget(key, field)
        return result

    def _set(self, field, value):
        return self.db.hset(self.key, field, value)

    @classmethod
    def isLogin(cls, uid=0):
        """
        is login
        account:login:set (zset)
        check session:{id}
        """
        session_user = SESSION_USER.format(uid=uid)
        if cls.db.r.exists(session_user):
            return True
        else:
            return False

    def logout(self):
        print(self.uid)
        account_login = ACCOUNT_LOGIN
        session_user = SESSION_USER.format(uid=self.uid)

        try:
            self.db.r.zrem(account_login, self.uid)
            self.db.r.delete(session_user)
            return True
        except:
            return False

    def links(self):
        result = self.db.r.smembers(ACCOUNT_LINK.format(uid=self.uid))
        result = list(result)
        links = []
        tmp = []
        for k in result:
            tmp.append(bytes.decode(k))
            links.append(convert(self.db.r.hgetall(LINK.format(lid=bytes.decode(k)))))

        return links

    def _handle(self, field, value=None):

        if value is None:
            result = self._get(field)
            result = bytes.decode(result)
            return result
        else:
            return self._set(field, value)

    def mobile(self, value=None):
        return self._handle('mobile', value)

#    def password(self, value=None):
#        if value is not None:
#            self._set('password', value)
#        else:
#            return self._get('password')

    def avatars(self, value=None):
        key = ACCOUNT_AVATARS.format(id=self.id)

        if value is None:
            return self.db.r.smembers(key)
        else:
            return self.db.r.sadd(key, value)


def test_aswer():
    assert(Account(1).nickname)
