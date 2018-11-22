# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:

“__getattribute_”与“_ getitem_”的最大差异，示例如下：
1. “__getattribute__”只适用于所有的“.”运算符；
2. “__getitem__”只适用于所有的“[]”运算符；

“_ getattribute_”与“_ getattr_”的最大差异在于：
1. 无论调用对象的什么属性，包括不存在的属性，都会首先调用“_ getattribute_”方法；
2. 只有找不到对象的属性时，才会调用“_ getattr_”方法；
"""


class Record(object):
    """

    """

    def __init__(self, keys, values):
        self._keys = keys
        self._values = values

    def keys(self):
        """
        Returns the list of column names from the query
        :return:
        """
        return self._keys

    def values(self):
        """
        Returns the list of values from the query
        :return:
        """
        return self._values

    def __getitem__(self, key):
        """
        row['key']
        :param key:
        :return:
        """
        keys = self.keys()
        values = self.values()

        if isinstance(key, int):
            return values[key]

        if key in keys:
            i = keys.index(key)
            if keys.count(key) > 1:
                raise KeyError("Record contains multiple '{}' fields.".format(key))
            return values[i]

        raise KeyError("Record contains no '{}' field.".format(key))

    def __getattr__(self, key):
        """
        obj.key
        :param item:
        :return:
        """
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def get(self, key, default=None):
        """
        obj.get('key', defalut)
        :param key:
        :param defalut:
        :return:
        """
        try:
            return self[key]
        except KeyError:
            return default
