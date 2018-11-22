# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""
from app.record import Record

class Connection(object):
    """
    database connection
    """

    def __init__(self, connection):
        self._conn = connection

    def close(self):
        pass

    def query(self, query):
        """

        :param query:
        :return:
        """
        # Execute the given query.
        cursor = self._conn.execute(query)
        # print(cursor.fetchall())
        # print(cursor.keys())
        # row_gen = (Record(cursor.keys(), row) for row in cursor)
        keys = cursor.keys()
        row_gen = (Record(keys, row) for row in cursor)
        # row_gen = [Record(keys, row) for row in cursor]

        for row in row_gen:
            pass
            # print(row.keys(), row.values())
            print(row.get('id2', 'sss'))
            # print(row.get('id'))
        a = 1
