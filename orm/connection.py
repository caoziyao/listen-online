# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""
from orm.record import Record
from orm.record_collection import RecordCollection


class Connection(object):
    """
    database connection
    """

    def __init__(self, connection):
        self._conn = connection

    def close(self):
        pass

    def query(self, query, fetchall=False):
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

        results = RecordCollection(row_gen, cursor.rowcount)
        # if fetchall:
        #     results.all()

        return results
