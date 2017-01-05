#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from game.Handler.BaseHandler import BaseHandler
import tornado.web

from lib.DB import db

class index(BaseHandler):
    def get(self):

        user = self.getUser()

        self.render('index.html', user=user)
