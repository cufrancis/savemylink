#!/usr/bin/env python
# coding=utf-8

import tornado.web
import tornado.ioloop
from tornado.web import RequestHandler
from tornado import template

from lib.DB import db
from lib.Account import Account
from lib.define import *
from lib.util.convert import ago
import os
from ..config import config
from lib.util.json import dumps


AJAX_HEADERS = ('X_PJAX', 'X-Requested-With',)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PJAX_TEMPLATE = '''
{{% extends "{0}/layout.html" %}}
{{% include "{0}/{1}" %}}
'''

class BaseHandler(tornado.web.RequestHandler):


    def _get_loader(self):
        template_path = self.get_template_path()
        with RequestHandler._template_loader_lock:
            if template_path not in RequestHandler._template_loaders:
                loader = self.create_template_loader(template_path)
                RequestHandler._template_loaders[template_path] = loader
            else:
                loader = RequestHandler._template_loaders[template_path]
        return loader

    def render(self, template_name, **kwargs):
        return self.render_pjax(template_name, **kwargs)

    def render_pjax(self, template_name, **kwargs):
        print(self.get_template_namespace())
        if not self.is_ajax:
            loader = self._get_loader()
            templates = PJAX_TEMPLATE.format(self.get_template_path(), template_name)
            namespace = self.get_template_namespace()
            namespace.update(kwargs)
            print(templates)
            print("Runnnnnnnnnnnnnnnnnn!!!!!!!!!!")
            t = template.Template(templates, loader=loader)
            self.write(t.generate(**namespace))
            #self.render(tornado.template.Template(template, loader=loader).generate(**namespace))
        else:
            print(template_name)
            self.write(self.render_string(template_name, **kwargs))

    # write json
    # when you want use api
    def write_json(self, data, msg='success.', status_code=200):
        self.finish(dumps({
            'code': status_code,
            'msg': msg,
            'data': data
        }))

    def initialize(self):
        self.is_ajax = False

    def prepare(self):
        self.is_ajax = any(hdr in self.request.headers for hdr in AJAX_HEADERS)

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.db = db
        self.user = self.get_current_user()
        self.title = self.settings['title']

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        result = super(BaseHandler, self).get_secure_cookie(name, value, max_age_days, min_version)
        try:
            return bytes.decode(result)
        except:
            return result

    def get_current_user(self):
        uid = self.get_secure_cookie('uid')
        if Account.isLogin(uid):
            return Account(uid)
        else:
            # clear cookie and return None Accont object
            self.clear_cookie('uid')
            return None
            #return Account(0)

    def getUser(self):
        uid = self.get_secure_cookie('uid')
        if Account.isLogin(uid):
            try:
                return Account(uid)
            except:
                return Account(0)

    def get_template_namespace(self):
        namespace = dict(
            ago = ago,
            is_ajax = self.is_ajax,
            title = self.title,
        )

        namespace.update(super().get_template_namespace())

        return namespace
