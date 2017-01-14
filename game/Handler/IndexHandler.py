#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from game.Handler.BaseHandler import BaseHandler
import tornado.web

from lib.DB import db
from lib.Link import Link
from lib.Account import Account

class index(BaseHandler):
    def get(self):
        link = Link(1)
        print("User")
        print(self.user)
        u1 = Account(1)
        print(u1.email)

        print(link.comments)
        print("++++++++")
        print(link.author.password)
        print("++++++++")

        comments = []
        links_content = Link().getAll()

 #       print(links_content)

        self.render('index.html',user=self.user, links=links_content)
