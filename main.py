from sanic import Sanic
from sanic.response import html
from jinja2 import Environment, PackageLoader, FileSystemLoader

from sanic.views import HTTPMethodView
env = Environment(loader=FileSystemLoader("./templates"))


app = Sanic(__name__)


import game.Handler.IndexHandler as IndexHandler
import game.Handler.UserHandler as UserHandler


app.add_route(IndexHandler.index(), '/')
app.add_route(UserHandler.login(), '/login')
app.add_route(UserHandler.register(), '/register')

app.run(host="0.0.0.0", port=8888, debug=True)
