#!/usr/bin/env python
# coding=utf-8

def convert(data):
    """
    dict bytes key to str value
    """
    if not isinstance(data, dict):
        return data
    return dict([(bytes.decode(k), bytes.decode(v)) for k, v in data.items()])
