#!/usr/bin/env python
# coding utf-8

import unittest

from Account import Account
from DB import db

class AccountTest(unittest.TestCase):

    def setUp(self):
        self.db = db

    def test_init(self):
        user = Account(1)
        self.assertTrue(isinstance(user.links, list))
