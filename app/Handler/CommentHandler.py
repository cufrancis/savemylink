#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from app.Handler.BaseHandler import BaseHandler
import tornado.web

from lib.DB import db
from lib.Comment import Comment
from lib.Link import Link
from lib.define import *
import time

class reply(BaseHandler):
    def get(self, cid):
        comment = Comment(cid)
        print(comment.lid)
        link = Link(comment.lid)
        print(link.lid)
        self.write("Reply")
        self.render_pjax('comment/reply.html', comment=comment, link=link)

    def post(self, cid):
        print(cid)
        print(self.get_argument('parent'))
        parent = self.get_argument('parent')
        lid = self.get_argument('lid')

        comment_content = dict(
            author_id = self.user.uid,
            lid = lid,
            content = self.get_argument('text'),
            created_at = int(time.time()),
            up = 0,
            sub = 0,
        )

        comment_count = COMMENT_COUNT
        cid = self.db.r.incr(comment_count)
        comment = COMMENT.format(cid=cid)
        comment_reply = COMMENT_REPLY.format(cid=cid)
        link_comments = LINK_COMMENT_COUNT.format(lid=lid)

        self.db.r.hmset(comment, comment_content)
        self.db.r.sadd(link_comments, cid)
        if parent != 0:
            comment_reply = COMMENT_REPLY.format(cid=parent)
            parent_comment = COMMENT.format(cid=parent)
            self.db.r.sadd(comment_reply, cid)
            self.db.r.hincrby(parent_comment, 'sub')

        self.redirect('/link/{lid}'.format(lid=lid))
