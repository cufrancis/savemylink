#!/usr/bin/env python
# coding=utf-8

import datetime
import time

def convert(data):
    """
    dict bytes key to str value
    """
    if not isinstance(data, dict):
        return data
    return dict([(bytes.decode(k), bytes.decode(v)) for k, v in data.items()])

def before_time(times):
    now = int(time.time())
    c = int(now - times)
    print(c)

    if c < 60:
        msg = "{second} Second before!".format(second=c)
    elif c >= 60 and c < 3600:
        msg = "{minute} minute before!".format(minute=int(c/60))
    elif c >= 3600:
        msg = "{hour} hours before".format(hour=int(c/3600))

    print(msg)

before_time(1483849573)

