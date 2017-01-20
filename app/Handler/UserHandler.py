#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append('../../')

from app.Handler.BaseHandler import BaseHandler

from lib.Account import Account
from lib.DB import db
from lib.define import *
from lib.Error import Error, LoginError
import time

class index(BaseHandler):
    def get(self, uid):
        user = Account(uid)
        links = user.links()

        print(user.links())

        self.render_pjax('user/index.html', user=user, links=links)

class login(BaseHandler):
    def get(self):
        self.render_pjax('login.html')

    def post(self):
        account = Account()
        email = self.get_argument('mobile')
        password = self.get_argument('password')

        try:
            if email is None:
                raise LoginError("email is None!")
            if password is None:
                raise LoginError("password is None!")

            account_email = ACCOUNT_EMAIL.format(email=email)
            if self.db.r.exists(account_email) is False:
                raise LoginError("Email does not exists!")
            uid = self.db.get(account_email)
            account_user = ACCOUNT_USER.format(uid=uid)
            if self.db.hget(account_user, 'password') != password:
                raise LoginError("Incorrect passord!")

            account_login = ACCOUNT_LOGIN
            session = SESSION_USER.format(uid=uid)
            lastlogin = dict(
                ip="127.0.0.1",
                time =int(time.time())
            )

            self.db.r.zadd(account_login, uid, 1)
            # session setting
            self.db.set(session, uid, 3600)

            # set secure cookie
            self.set_secure_cookie('uid', str(uid))
        except LoginError as e:
            self.write(e.message)
        else:
            self.write("Login successful!")

class register(BaseHandler):
    def get(self):
        self.render_pjax('register.html', title='register')

    def post(self):
        account = Account()
        email = self.get_argument('mobile')
        password = self.get_argument('password')

        account_email = ACCOUNT_EMAIL.format(email=email)
        account_count = ACCOUNT_COUNT

        userinfo = dict(
            email = email,
            password = password,
            sex = 'male',
            age = 18,
            desc = '',
            image = '',
            status = 'open',
            mobile = ''
        )

        try:
            if self.db.r.exists(account_email) is True:
                raise LoginError("email is exists!")

            uid = self.db.r.incr(account_count)

            account_userlist = ACCOUNT_USERLIST
            account_user = ACCOUNT_USER.format(uid=uid)

            self.db.r.set(account_email, uid)
            self.db.r.sadd(account_userlist, uid)
            self.db.r.hmset(account_user, userinfo)
        except LoginError as e:
            self.write(e.value)
        else:
            self.write("Register successful!")

class logout(BaseHandler):

    def get(self):
        print(self.user.uid)
        if self.user.logout():
            self.clear_cookie('uid')

        self.write("logout successful")
