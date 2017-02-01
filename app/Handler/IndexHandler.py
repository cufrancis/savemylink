#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from app.Handler.BaseHandler import BaseHandler
import tornado.web
import tornado.log

from lib.DB import db
from lib.Link import Link
from lib.Account import Account
import json

class index(BaseHandler):
    def get(self):
        links = Link.all()

        #print(self.user.isAdmin())
        #data = json.load(links)
        #self.write(data)
        self.render_pjax("index.html", user=self.user, links=links)

        #self.render('index.html',user=self.user, links=links)
