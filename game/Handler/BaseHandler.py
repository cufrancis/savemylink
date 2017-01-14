#!/usr/bin/env python
# coding=utf-8


#from sanic.views import HTTPMethodView
import tornado.web
import tornado.ioloop

#from jinja2 import Environment, PackageLoader, FileSystemLoader
#from sanic.response import html

from lib.DB import db
from lib.Account import Account
from lib.define import *

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.db = db
        self.user = self.getUser()

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        result = super(BaseHandler, self).get_secure_cookie(name, value, max_age_days, min_version)
        try:
            return bytes.decode(result)
        except:
            return result


    def getUser(self):
        uid = self.get_secure_cookie('uid')
        if Account.isLogin(uid):
            try:
                return Account(uid)
            except:
                return None
