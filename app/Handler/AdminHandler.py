#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from app.Handler.BaseHandler import BaseHandler
import tornado.web
from module.Error import PermissionError
from module.Link import Link

class index(BaseHandler):

    def get(self):
        try:
            if not self.user.isAdmin():
                raise PermissionError("You do not have administrative privileges!")
            # show admin page
            self.render("admin/index.html")
        except PermissionError as e:
            self.write(e.message)

class link(BaseHandler):
    def get(self, lid=0):
        print(self.user)
        try:
            if self.user == None or not self.user.isAdmin:
                raise PermissionError("You do not have administrative privilieges!")
            links = Link.all()
            self.render("admin/links.html", links=links)
        except PermissionError as e:
            self.write(e.message)
