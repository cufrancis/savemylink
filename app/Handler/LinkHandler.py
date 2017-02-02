#!/usr/bin/env python
# coding=utf-8
#

import sys
sys.path.append("../../../")

from app.Handler.BaseHandler import BaseHandler
import tornado.web

from lib.DB import db
from lib.Link import Link
import time
from lib.define import *
from lib.Account import Account
from lib.Error import PermissionError

class index(BaseHandler):
    def get(self, lid):
        link = Link(lid)
        self.render_pjax('link/index.html', link=link)
        #self.write("Link.index")

    @tornado.web.authenticated
    def post(self, lid):
        parent = self.get_argument('parent') # reply comment id, if not reply , this is 0

        comment_context = dict(
            author_id = self.user.uid,
            lid = lid, # link_id
            content = self.get_argument('text'),
            created_at = int(time.time()),
            up = 0, # incr
            sub = 0, # incr, reply count
        )
        print(parent)

        if parent == '0':
            print(parent)
            link_comment = LINK_COMMENT.format(lid=lid)
            comment_count = COMMENT_COUNT
            link_comments_set = LINK_COMMENT_COUNT.format(lid=lid)
            cid = self.db.r.incr(comment_count)
            comment = COMMENT.format(cid=cid)

            self.db.r.zadd(link_comment, cid, 0)
            #self.db.r.incr(link_comment_count)
            self.db.r.sadd(link_comments_set, cid)
            self.db.r.hmset(comment, comment_context)
            self.redirect("/link/{lid}".format(lid=lid))
        else:
            pass

class delete(BaseHandler):
    @tornado.web.authenticated
    def get(self, lid):
        try:
            if self.user == None or not self.user.isAdmin():
                raise PermissionError("No admin")
            result = Link.delete(lid)
        except PermissionError as e:
            print(e)
            self.write(e.message)
        else:
            print(result)

class create(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render_pjax('link/create.html')

    @tornado.web.authenticated
    def post(self):
        url = self.get_argument('url')
        title = self.get_argument('title')

        info = {
            'author':self.user.uid,
            'title':title,
            'url':url,
            'created_at':int(time.time()),
            'updated_at':int(time.time())
        }

        link_count = LINK_COUNT
        lid = self.db.r.incr(link_count)

        link_link = LINK.format(lid=lid)
        link_all = LINK_ALL
        link_sort_bytime = LINK_SORT_BYTIME.format(lid=lid)
        link_sort_byvisit = LINK_SORT_BYVISIT.format(lid=lid)
        account_link = ACCOUNT_LINK.format(uid=info['author'])

        try:
            self.db.r.hmset(link_link, info)
            self.db.r.sadd(link_all, lid)
            self.db.r.zadd(link_sort_bytime, lid, int(time.time()))
            self.db.r.zadd(link_sort_byvisit, lid, 0)
            self.db.r.sadd(account_link, lid)
        except :
            self.write_json(1, "Some error")
            # self.write("Error............")
        else:
            self.write_json(0, "created successful")
            # self.write("Created successful!")

class check_url(BaseHandler):

    def post(self):
        url = self.get_argument('url')

        if len(url) <= 0:
            self.write_json(1, "URL 不能为空")

        self.write_json(0, "验证通过")

class get_title(BaseHandler):

    def post(self):
        url = self.get_argument('url')

        try:
            from bs4 import BeautifulSoup
            import requests
            r = requests.get(url, timeout=2)
            soup = BeautifulSoup(r.text,"html.parser")
        except:
            self.write_json("")
        else:
            self.write_json(soup.title.string)

class vote_up(BaseHandler):
    def post(self):
        if self.current_user:
            lid = int(self.get_argument('lid'))
            link = Link(lid)
            link.vote_up()
            # print(link.points)
            # data = {
            #     "points":link.points
            # }
            self.write_json(dict(status=0, points=link.points))
        else:
            self.write_json(dict(status=1), "未登陆")

class vote_down(BaseHandler):
    def post(self):
        # data = dict()

        if self.current_user:
            lid = int(self.get_argument('lid'))
            link = Link(lid)
            link.vote_down()
            # data = {
            #     'status':0
            #     "points":link.points
            # }
            self.write_json(dict(status=0, points=link.points))
        else:
            self.write_json(dict(status=1), "未登陆！")
            # data['status'] = 1

        # self.write_json(data)

class api_link(BaseHandler):

    def get(self):
        pass
