#!/usr/bin/env python
# coding=utf-8


from sanic.views import HTTPMethodView
from jinja2 import Environment, PackageLoader, FileSystemLoader
from sanic.response import html

from lib.DB import db
from lib.Account import Account

class BaseHandler(HTTPMethodView):

    def __init__(self):
        #super(BaseHandler, self).__init__()
        self.env = Environment(loader=PackageLoader("game", 'templates'))
        self.db = db

    def render(self, tplname, *args, **kwargs):
        template = self.env.get_template(tplname)

        return html(template.render(*args, **kwargs))

    def getUser(self, request):
        uid = request.cookies.get('id')
        print('cookie_uid')
        print(uid)
        if uid is not None:
            #redis_uid = self.db.r.sismember('account:login:set', cookie_uid)
            #print(redis_uid)
            if self.db.r.sismember('account:login:set', uid) is True:
                #return uid
                return Account(uid)
            else:
                return None
        else:
            return  None
