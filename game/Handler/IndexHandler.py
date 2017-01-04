#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from game.Handler.BaseHandler import BaseHandler

from sanic.response import html
from lib.DB import db

class index(BaseHandler):
    def get(self, request):
        user = self.getUser(request)
        print("User:{user}".format(user=user))
        print(user.email())
        template = self.env.get_template('index.html')

        return html(template.render(user=user))
