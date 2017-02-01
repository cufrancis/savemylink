#!/usr/bin/env python
# coding=utf-8

import tornado.web

class remodal(tornado.web.UIModule):
    def css_files(self):
        return [
        '//cdn.bootcss.com/remodal/1.1.1/remodal.css', '//cdn.bootcss.com/remodal/1.1.1/remodal-default-theme.css'
        ]

    def javascript_files(self):
        return "//cdn.bootcss.com/remodal/1.1.1/remodal.js"
    def render(self):
        return self.render_string(
            "module-remodal.html"
        )
