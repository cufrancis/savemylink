#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from app.Handler.BaseHandler import BaseHandler
import tornado.web
import tornado.log

from module import db, Link, Account
import json

class index(BaseHandler):
    def get(self):
        links = Link.all()

        self.render("index.html", user=self.user, links=links)
