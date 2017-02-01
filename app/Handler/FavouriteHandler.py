#!/usr/bin/env python
# coding=utf-8

from app.Handler.BaseHandler import BaseHandler
import tornado.web

from lib.Favourite import Favourite
from lib.Link import Link

class index(BaseHandler):
    def get(self, fid):
        fid = int(fid)

        favourite = Favourite(fid)
        #links = favourite.links() # get all links in favourite
        links = []

        for k in favourite.links():
            links.append(Link(k))

        print(links)
        self.render("favourite/index.html", links = links)

class create(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("favourite/create.html")

    @tornado.web.authenticated
    def post(self):
        info = dict(
            name = self.get_argument('name')
        )

        try:
            fid = Favourite.create(info)
            self.user.add_favourite(fid)
            self.redirect('/user/'+self.user.uid+'/favourite')
        except:
            self.write("add favourite Error")

class addlink(BaseHandler):
    @tornado.web.authenticated
    def get(self, fid, lid):
        print("addlink!!!!")
        fid = int(fid)
        lid = int(lid)
        # add link id to favourite
        favourite = Favourite(fid)
        #print(favourite.addlink(lid))
        favourite.addlink(lid)
        favourite.save()

        print(favourite.links())

        self.redirect('/')
