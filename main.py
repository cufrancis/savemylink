# from sanic import Sanic
# from sanic.response import html
import tornado.ioloop
import tornado.web
#from jinja2 import Environment, PackageLoader, FileSystemLoader

#from sanic.views import HTTPMethodView
#env = Environment(loader=FileSystemLoader("./templates"))


#app = Sanic(__name__)


import game.Handler.IndexHandler as Index
import game.Handler.UserHandler as User

from game.url import url
from game.config import config

def make_app():
    return tornado.web.Application(
        handlers = url,
        **config
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


#app.add_route(IndexHandler.index(), '/')
#app.add_route(UserHandler.login(), '/login')
#app.add_route(UserHandler.register(), '/register')
#app.add_route(UserHandler.logout(), '/logout')

#app.run(host="0.0.0.0", port=8888, debug=True)
