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
        link_cls = Link()

        links = link_cls.getAll()

        self.render('index.html',user=self.user, links=links)
