#!/usr/bin/env python
# coding=utf-8

from app.Handler.BaseHandler import BaseHandler
import tornado.web

from module import Favourite, Link
import time

class all(BaseHandler):

    def get(self):
        public  = Favourite.public()

        print(public)
        self.render("favourite/all.html", public=public)

class index(BaseHandler):
    def get(self, fid):
        fid = int(fid)

        favourite = Favourite(fid)
        #links = favourite.links() # get all links in favourite
        links = []
        print(favourite.author)

        for k in favourite.links():
            links.append(Link(k))

        print(links)
        self.render("favourite/index.html", favourite=favourite,links = links)

class create(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("favourite/create.html")

    @tornado.web.authenticated
    def post(self):
        info = dict(
            name = self.get_argument('name'),
            public = int(self.get_argument('public')), # 是否public
            created_at = int(time.time()),
            author = int(self.current_user.uid),
        )

        try:
            fid = Favourite.create(info)
            self.user.add_favourite(fid)
        except:
            self.write("add favourite Error")
        else:
            self.redirect('/user/{uid}/favourite'.format(uid=self.user.uid))

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
