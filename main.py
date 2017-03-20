#!/usr/bin/env python
# coding=utf-8

import tornado.ioloop
import tornado.web
# import logging
# import yaml

# import app.Handler.IndexHandler as Index
# import app.Handler.UserHandler as User

from app.url import url
from app.config import config
from tornado.options import define, options
import tornado.httpserver

define("port", default=8888, help="run on the given port", type=int)


def make_app():
    return tornado.web.Application(
        handlers=url,
        **config
    )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    apps = make_app()
    http_server = tornado.httpserver.HTTPServer(apps)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    # apps.listen(8888)
    # tornado.ioloop.IOLoop.current().start()
