#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append('../../')

from game.Handler.BaseHandler import BaseHandler

from lib.Account import Account
from lib.DB import db

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
        id = account.login(mobile, password)

        if id != None:
            self.set_secure_cookie('id', id)
            self.write("login successful!")
        else:
            return "error"

class register(BaseHandler):
    def get(self):
        self.render('register.html', title='register')

    def post(self):
        account = Account()
        email = self.get_argument('mobile')
        password = self.get_argument('password')

        uid = account.register(email, password)
        self.set_secure_cookie('uid', 'hello')

        if uid != None:
            self.set_secure_cookie('id', str(uid))
            msg = "register sccessful!"
        else:
            msg = 'register error'

        self.write(msg)

class logout(BaseHandler):

    def get(self):
        db.r.srem('account:login:set', uid)
        db.r.delete('session:{id}'.format(id=uid))
        self.clear_cookie('id')

        self.write("logout successful")
