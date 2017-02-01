# from sanic import Sanic
# from sanic.response import html
import tornado.ioloop
import tornado.web
import logging
import yaml
#from jinja2 import Environment, PackageLoader, FileSystemLoader

#from sanic.views import HTTPMethodView
#env = Environment(loader=FileSystemLoader("./templates"))


#app = Sanic(__name__)


import app.Handler.IndexHandler as Index
import app.Handler.UserHandler as User

from app.url import url
from app.config import config

def make_app():
    return tornado.web.Application(
        handlers = url,
        **config
    )

if __name__ == "__main__":
    apps = make_app()
    apps.listen(8888)
    tornado.ioloop.IOLoop.current().start()
