#!/usr/bin/env python
# coding=utf-8

from lib.DB import db
import hashlib
import time

slat = 'password'
ACCOUNT_COUNT = 'account:count'
ACCOUNT_USERLIST = 'account:userlist'
ACCOUNT_EMAIL = 'account:email:{email}'
ACCOUNT = 'account:{id}'


class Account(object):


    def __init__(self, account_id=0):
        self.db = db
        self.id = account_id
        self.key = ACCOUNT.format(id=self.id)
        self.account_key = ACCOUNT.format(id=self.id)

    def _get(self, field):
        #return self.key
        result = self.db.r.hget('account:{id}'.format(id=self.id), field)
        #print(self.id)
        #print(result)
        return result
        #return self.db.hget(self.key, field)

    def _set(self, field, value):
        return self.db.hset(self.key, field, value)

    # register account
    def register(self, email, password):
        if email is None or password is None:
            return -1
            #return "cannot register"
        else:
            if self.db.r.exists('account:email:{email}'.format(email=email)) is False:
                id = self.db.r.incr('account:count')
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

                self.db.r.set('account:email:{email}'.format(email=email), id)
                self.db.r.sadd('account:userlist', id)
                self.db.r.hmset('account:{id}'.format(id=id),userinfo)
                return id
            else:
                return -2
                #return 'mobile has register!'

    def login(self, email, password):
        if email is None or password is None:
            # mobile or password is None
            return -1
        else:
            if self.db.r.exists('account:email:{email}'.format(email=email)) is True:

                account_id = self.db.get('account:email:{email}'.format(email=email))

                if self.db.hget('account:{id}'.format(id=account_id), 'password') == str.encode(password):
                    self.db.r.sadd('account:login:set', account_id)
                    # Session setting
                    #self.db.r.set('account:login:{id}'.format(id=id), '')
                    lastlogin = {
                        'ip':'127.0.0.1',
                        'time':time.time()
                    }
                    self.db.r.hmset('account:{id}:lastlogin'.format(id=account_id), lastlogin)
                    # add session key and set expire time is 3600s
                    self.db.set('session:{id}'.format(id=account_id), account_id, 3600)
                    print("account:login:set")
                    return account_id
                else:
                    return "password error"
            else:
                # no account information
                return "no have this account"

    def _handle(self, field, value=None):

        if value is None:
            return self._get(field)
        else:
            return self._set(field, value)

    def email(self, value=None):
        if value is not None:
            self._set('email', value)
        else:
            return bytes.decode(self._get('email'))
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
        key = 'account:{id}:avatars'.format(id=self.id)

        if value is None:
            return self.db.r.smembers(key)
        else:
            return self.db.r.sadd(key, value)

account = Account(1)

print(account.password())

print(db.r.keys())
