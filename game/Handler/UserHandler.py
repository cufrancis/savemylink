#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append('../../')

from game.Handler.BaseHandler import BaseHandler

from lib.Account import Account
from lib.DB import db
from lib.define import *

class index(BaseHandler):
    def get(self, uid):
        user = Account(uid)
        print(user.email)
        print("userS")
        print(user.name)

        print("Links")
        links = user.links()
        print(user.links())

        self.render('user/index.html', user=user, links=links)

class login(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        account = Account()
        mobile = self.get_argument('mobile')
        password = self.get_argument('password')
        uid = account.login(mobile, password)

        if uid >= 0:
            print("Hello?")
            self.set_secure_cookie('uid', str(uid))
            self.write("login successful!")
        else:
            self.write("Error")

class register(BaseHandler):
    def get(self):
        self.render('register.html', title='register')

    def post(self):
        account = Account()
        email = self.get_argument('mobile')
        password = self.get_argument('password')

        uid = account.register(email, password)

        if uid >= 0:
            self.set_secure_cookie('uid', str(uid))
            msg = "register sccessful!"
        else:
            msg = 'register error'

        self.write(msg)

class logout(BaseHandler):

    def get(self):
        uid = self.get_secure_cookie('uid')
        db.r.srem(ACCOUNT_LOGIN, uid)
        db.r.delete(SESSION_USER.format(uid=uid))
        self.clear_cookie('uid')

        self.write("logout successful")
