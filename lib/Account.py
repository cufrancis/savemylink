#!/usr/bin/env python
# coding=utf-8

from lib.DB import db
import hashlib
import time
from lib.util.convert import convert
from lib.Error import LoginError

from lib.define import *
from lib.Favourite import Favourite
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

        #if not isinstance(uid, int):
        #    raise TypeError('Bad operand type')

        self.db = db
        self.uid = uid
        self.key = ACCOUNT_USER.format(uid=uid)
        self.account_key = ACCOUNT_USER.format(uid=uid)
        #ACCOUNT_USER.format(uid=self.uid)

    def favourites(self):

        account_favourite = ACCOUNT_FAVOURITE.format(uid=self.uid)

        tmp = self.db.smembers(account_favourite)
        result = []

        #print("TMP ===============")
        #print(tmp)

        for k in tmp:
            result.append(Favourite(k))

        return result

        #print(result)
        #result = self.db.r.hget()

    # add favourite id to user favourite table
    # fid to account:{id}:favourite|(set)
    def add_favourite(self, fid):
        account_favourite = ACCOUNT_FAVOURITE.format(uid=self.uid)
        self.db.r.sadd(account_favourite, fid)

    def __getattr__(self, field):
        print("Account.__getattr__.{field}".format(field=field))

        attributes = ['email','mobile', 'nick_name', 'age',  'password', 'desc', 'status', 'avatar']

        if field in attributes:
#            if self._get(fied)
            return self._get(field)

    def _get(self, field):
        key = ACCOUNT_USER.format(uid=self.uid)

        result = self.db.hget(key, field)
        return result

    def _set(self, field, value):
        return self.db.hset(self.key, field, value)

    @property
    def nickname(self):
        return self.db.r.hget(self.account_key, 'nickname')

    @property
    def sex(self):
        return self.db.r.hget(self.account_key, 'sex')

    def isAdmin(self):
        # test admin data start
        self.db.r.sadd(ADMIN, 1)
        #test admin data end

        if self.db.r.sismember(ADMIN, self.uid):
            return True
        else:
            return False

    @classmethod
    def login(cls, email, password):
        print("Account.login...........")
        account = Account()
        email = email
        password = password

        if email is None:
            raise LoginError("email is None!")
        if password is None:
            raise LoginError("password is None!")

        account_email = ACCOUNT_EMAIL.format(email=email)
        if cls.db.r.exists(account_email) is False:
            raise LoginError("Email does not exists!")

        uid = cls.db.get(account_email)
        account_user = ACCOUNT_USER.format(uid=uid)
        if cls.db.hget(account_user, 'password') != password:
            raise LoginError("Incorrect passord!")

        account_login = ACCOUNT_LOGIN
        session = SESSION_USER.format(uid=uid)
        lastlogin = dict(
            ip="127.0.0.1",
            time =int(time.time())
        )

        cls.db.r.zadd(account_login, uid, 1)
        # session setting
        cls.db.set(session, uid, 3600)

        return uid

    @classmethod
    def register(cls, userinfo):
        """
        successful return uid, failed return 0
        """
        account_email = ACCOUNT_EMAIL.format(email=userinfo.get('email'))
        account_count = ACCOUNT_COUNT
        nickname_set = NICKNAME
        email_set = EMAIL
        uid = 0

        if cls.db.r.exists(account_email) is True:
            raise LoginError("email is exists!")

        uid = cls.db.r.incr(account_count)

        account_userlist = ACCOUNT_USERLIST
        account_user = ACCOUNT_USER.format(uid=uid)

        cls.db.r.set(account_email, uid)
        cls.db.r.sadd(account_userlist, uid)
        cls.db.r.hmset(account_user, userinfo)
        cls.db.r.sadd(nickname_set, userinfo.get('nickname'))
        cls.db.r.sadd(email_set, userinfo.get('email'))

        return uid

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
