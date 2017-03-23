#!/usr/bin/env python
# coding=utf-8

class NoneClass(object):

    def __init__(self):
        pass

    def __repr__(self):
        return str(None)

    def __getattr__(self, value):
        try:
            #return NoneClass()
            return NoneClass()
        except:
            return NoneClass()


s = NoneClass()

#print(type(s.name))
print(s.name.age)


if (isinstance(s.name.age, NoneClass)):
    print("Yes")
else:
    print("No")
