#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append('../')

from tornado.test.util import unittest
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from game.Handler.IndexHandler import IndexHandler

class BaseTest(AsyncHTTPTestCase):
    def setUp(self):
        pass
        super(BaseTest, self).setUp()


class WebHandlerTest(BaseTest):

    def get_app(self):
        return Application([
            (r'/test', IndexHandler),
        ])

    def test_sub(self):
        body = 'hello world'
        response = self.fetch('/test/', method='POST', body=body)
        self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()

