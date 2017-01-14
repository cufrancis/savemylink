#!/usr/bin/env python
# coding=utf-8
#

import sys
sys.path.append("../../../")

from game.Handler.BaseHandler import BaseHandler
import tornado.web

from lib.DB import db
from lib.Link import Link
import time

class create(BaseHandler):
    def get(self):
        self.render('link/create.html')

    def post(self):
        url = self.get_argument('url')
        title = self.get_argument('title')

        info = {
            'author':self.user.uid,
            'title':title,
            'url':url,
            'created_at':int(time.time()),
            'updated_at':int(time.time())
        }

        link = Link()
        result = link.add(info)

        if (result):
            msg = "successful!"
        else:
            msg = 'Error!'

        self.write(msg)
