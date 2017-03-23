#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append('../../')

from app.Handler.BaseHandler import BaseHandler

from module import Account, db, Link
from module.define import *
from module.Error import Error, LoginError
import time
import tornado.web

class index(BaseHandler):
    def get(self, uid):

        # try:
        uid = int(uid)
        user = Account(uid)
        links = user.links()
        # except NotExistsError as e:
        #     self.write("user Not exists!")


        self.render('user/index.html', user=user, links=links)

class login(BaseHandler):
    def get(self):
        self.render('user/login.html')

    def post(self):
        email = self.get_argument('mobile')
        password = self.get_argument('password')

        # print("email")
        # print(email)

        try:
            uid = Account.login(email, password)
            self.set_secure_cookie('uid', str(uid))
        except LoginError as e:
            self.write(e.message)
        else:
            self.redirect('/')

    def checkEmail(self):
        pass

class register(BaseHandler):
    def get(self):
        self.render('user/register.html', title='register')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        nickname = self.get_argument('nickname')

        # self.write(email)

        userinfo = dict(
            email = email,
            nickname = nickname,
            password = password,
            sex = 'male',
            age = 18,
            desc = '',
            image = '',
            status = 'open',
            mobile = '',
            expired = 3600,
        )
        try:
            uid = Account.register(userinfo)
        except LoginError as e:
            self.write_json(1, e.message)
            # self.write(e.message)
        else:
            try:
                uid = Account.login(email, password)
                self.set_secure_cookie('uid', str(uid))
            except LoginError as e:
                self.write_json(1, e.message)
                # self.write(e.message)
            else:
                self.write_json(0, "注册成功！")
                # self.redirect('/')

class favourite(BaseHandler):
    #@tornado.web.authenticated
    def get(self, uid):
        # show user favourite (alls), need login

        user = self.user

        if isinstance(uid, int):
            user = Account(uid)

        self.render("user/favourite.html", user=user)

class add_favourite(BaseHandler):

    @tornado.web.authenticated
    def get(self, lid):
        #lid = int(lid)
        link = Link(lid)
        favourites = self.user.favourites()

        self.render("user/add_favourite.html", favourites=favourites, link=link)

class logout(BaseHandler):

    def get(self):
        if self.user.logout():
            self.clear_cookie('uid')

        self.redirect("/")

class check_nickname(BaseHandler):
    """
    检查昵称
    不可重名
    不可为空
    不可为非法字符
    """
    def post(self):
        nickname = self.get_argument('nickname')

        # user_nickname = USER_NICKNAME.format(nickname=nickname)
        nickname_set = NICKNAME

        if len(nickname) <= 0:
            self.write_json(1, "昵称不能为空" )

        if self.db.r.sismember(nickname_set, nickname):
            self.write_json(1, "昵称已存在")
        else:
            self.write_json(0, "昵称不存在")

class check_email(BaseHandler):

    def post(self):
        email = self.get_argument('email')
        email_set = EMAIL

        if len(email) <= 0:
            self.write_json(1, "邮箱不能为空")

        if self.db.r.sismember(email_set, email):
            self.write_json(1, "邮箱已存在")
        else:
            self.write_json(0, "邮箱不存在")

        self.write_json(200)

class setting(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('user/settings.html')

    @tornado.web.authenticated
    def post(self):
        tmp = self.request.arguments
        data = dict()
        for k, v in tmp.items():
            data[k] = bytes.decode(v[0])
            # print(v[0])
        # print(data)
        print(self.current_user.update(data))
