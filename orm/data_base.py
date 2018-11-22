# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""
import pymysql
from sqlalchemy import create_engine, exc, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from orm.connection import Connection


class Database(object):
    """
    Database
    """

    def __init__(self, db_url, **kwargs):
        self.db_url = db_url

        if not self.db_url:
            raise ValueError('You must provide a db_url.')

        # Create an engine.
        pymysql.install_as_MySQLdb()
        self._engine = create_engine(self.db_url, **kwargs)
        BaseModel = declarative_base()

    def close(self):
        """
        close database
        :return:
        """
        pass

    def get_connection(self):
        """

        :return:
        """
        return Connection(self._engine.connect())

    def query(self, query):
        """
        query
        :param query:
        :return:
        """
        conn = self.get_connection()
        return conn.query(query)
