# -*- coding: utf-8 -*-
from . import unittest, mock
from mrmino-tes import mrmino-test


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.obj = mrmino-test()

    def test_something(self):
        self.assertEqual(2, 1 + 1)
