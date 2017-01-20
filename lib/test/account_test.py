#!/usr/bin.env python
# coding=utf-8
import sys

#sys.path.append("../../../")

import unittest

from ..Model import Account

class DefaultWidgetSizeTestCase(unittest.TestCase):

    def runTest(self):
        user = Account(1)
        assert user.nickname == None, 'incorrect default size'


if __name__ == '__main__':
    unittest.main()
