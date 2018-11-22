# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""
import unittest
from tests.base_test_case import BaseTestCase
from orm.data_base import Database


class TestORM(BaseTestCase):
    """
    TestORM
    """

    @unittest.skip("test_connect")
    def test_connect(self):
        """
        """
        url = 'mysql://root:zy123456@localhost/wiki?charset=utf8'
        db = Database(url)

    @unittest.skip("query skip")
    def test_query(self):
        """

        :return:
        """
        # url = 'mysql://root:zy123456@localhost/wiki?charset=utf8'
        # db = Database(url)
        db = self.db
        sql = 'select * from tb_user'
        rows = db.query(sql)

        print(rows)

        print(rows[0])  # Record

        for r in rows:
            print(r.id, r.username)

        print(rows.all())  # [Record, Record]
        print(rows.first())  # Record

        pass


if __name__ == '__main__':
    unittest.main()
