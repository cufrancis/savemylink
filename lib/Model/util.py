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

def ago(times, accurate=False):
    now = int(time.time())
    times = int(times)
    c = now - times
    #print(c)

    if c < 60:
        msg = "{second} Second ago".format(second=c)
    elif c >= 60 and c < 3600:
        msg = "{minute} minute ago".format(minute=int(c/60))
    elif c >= 3600 and c < 86400:
        msg = "{hour} hours ago".format(hour=int(c/3600))
    elif c >= 86400 and c < 604800:
        msg = "{day} days ago".format(day=int(c/86400))
    elif c >= 604800 and c < 2592000:
        msg = "{week} weeks ago".format(week=int(c/604800))
    elif c >= 2592000 and c < 31114000:
        msg = "{month} months ago".format(month=int(c/2592000))
    elif c >= 31114000:
        msg = "{year} years ago".format(year=int(c/31114000))

    return msg

    print(msg)

ago(1483849573)

