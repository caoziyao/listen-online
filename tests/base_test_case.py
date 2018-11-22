# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""
import unittest
from orm.data_base import Database


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        url = 'mysql://root:zy123456@localhost/wiki?charset=utf8'
        self.db = Database(url)
