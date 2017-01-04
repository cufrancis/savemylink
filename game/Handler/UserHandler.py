#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append('../../')

from game.Handler.BaseHandler import BaseHandler
from sanic.response import html, text

from lib.Account import Account
from lib.DB import db

class login(BaseHandler):
    def get(self, request):
        #template = self.env.get_template('index.html')
        return self.render('login.html')

    def post(self, request):
        account = Account()
        mobile = request.form['mobile'][0]
        password = request.form['password'][0]
        id = account.login(mobile, password)

        if id != None:
            response = text("cookie up in this response")
            response.cookies['id'] = id
            response.cookies['id']['path'] = '/'
            return response
        else:
            return "error"

class register(BaseHandler):
    def get(self, request):
        print(request.cookies)
        return self.render('register.html', title='register')

    def post(self, request):
        account = Account()
        email = request.form['mobile'][0]
        password = request.form['password'][0]
        id = account.register(email, password)
        if id >= 0:
            msg = "register sccessful!"
        else:
            msg = 'register error'

        return text(msg)
