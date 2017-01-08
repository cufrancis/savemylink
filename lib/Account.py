#!/usr/bin/env python
# coding=utf-8

from lib.DB import db
import hashlib
import time
from lib.util import convert

from lib.define import *

slat = 'password'


class Account(object):


    def __init__(self, uid=0):
        self.db = db
        self.uid = uid
        self.key = ACCOUNT_USER.format(uid=uid)
        self.account_key = ACCOUNT_USER.format(uid=uid)

    def __getattr__(self, field):
        print("__getattr__:{field}".format(field=field))
        result = self._get(field)
        if result:
            return result
        else:
            return None
        #print(result)

    def _get(self, field):
        result = self.db.r.hget(ACCOUNT_USER.format(uid=self.uid), field)
        if result:
            result = bytes.decode(result)
        return result

    def _set(self, field, value):
        return self.db.hset(self.key, field, value)

    def links(self):
        print(self.uid)
        result = self.db.r.smembers(ACCOUNT_LINK.format(uid=self.uid))
        result = list(result)
        links = []
        tmp = []
        for k in result:
            tmp.append(bytes.decode(k))
            links.append(convert(self.db.r.hgetall(LINK.format(link_id=bytes.decode(k)))))

        return links

    # register account
    def register(self, email, password):
        if email is None or password is None:
            return -1
            #return "cannot register"
        else:
            if self.db.r.exists(ACCOUNT_EMAIL.format(email=email)) is False:
                uid = self.db.r.incr(ACCOUNT_COUNT)
                userinfo = {
                    'email' :email,
                    'password': password,
                    'sex' : 'male',
                    'age' : 18,
                    'desc': '',
                    'image': '',
                    'status': 'open',
                    'mobile': ''
                }

                self.db.r.set(ACCOUNT_EMAIL.format(email=email), uid)
                self.db.r.sadd(ACCOUNT_USERLIST, uid)
                self.db.r.hmset(ACCOUNT_USER.format(uid=uid),userinfo)
                print(uid)
                return int(uid)
            else:
                return -2
                #return 'mobile has register!'

    def login(self, email, password):
        if email is None or password is None:
            # mobile or password is None
            return -1
        else:
            if self.db.r.exists(ACCOUNT_EMAIL.format(email=email)) is True:
                print("True")

                uid = self.db.get(ACCOUNT_EMAIL.format(email=email))

                if self.db.hget(ACCOUNT_USER.format(uid=uid), 'password') == str.encode(password):
                    self.db.r.sadd(ACCOUNT_LOGIN, uid)
                    # Session setting
                    #self.db.r.set('account:login:{id}'.format(id=id), '')
                    lastlogin = {
                        'ip':'127.0.0.1',
                        'time':time.time()
                    }
                    self.db.r.hmset(ACCOUNT_LAST_LOGIN.format(uid=uid), lastlogin)
                    # add session key and set expire time is 3600s
                    self.db.set('session:{id}'.format(id=uid), uid, 3600)
                    print(ACCOUNT_LOGIN)
                    return int(uid)
                else:
                    return -2
                    #return "password error"
            else:
                # no account information
                return -3
                #return "no have this account"

    def _handle(self, field, value=None):

        if value is None:
            result = self._get(field)
            result = bytes.decode(result)
            return result
        else:
            return self._set(field, value)

   # def email(self, value=None):
    #    if value is not None:
     #       self._set('email', value)
      #  else:
       #     return self._get('email')
            #return self._handle('email', value)

    def mobile(self, value=None):
        return self._handle('mobile', value)

    def password(self, value=None):
        if value is not None:
            #md5 = hashlib.md5()
            #md5.update(str.encode(value+slat))
            #value = md5.digest()
            self._set('password', value)
        else:
            return self._get('password')

    def avatars(self, value=None):
        key = ACCOUNT_AVATARS.format(id=self.id)

        if value is None:
            return self.db.r.smembers(key)
        else:
            return self.db.r.sadd(key, value)

#account = Account(1)

#print(account.password())

#print(db.r.keys())
