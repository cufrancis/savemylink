#!/usr/bin/env python
# coding=utf-8

import tornado.web

class remodal(tornado.web.UIModule):
    def render(self):
        return self.render_string(
            "module-remodal.html"
        )
