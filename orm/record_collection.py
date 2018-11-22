# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""


class RecordCollection(object):
    """

    """

    def __init__(self, rows, rowcount):
        """
        row: Record obj 的生成器
        :param rows:
        """
        self._rows = rows
        self._all_rows = []
        self._rowcount = rowcount
        self.pending = True

    def __len__(self):
        return len(self._all_rows)

    def __next__(self):
        """
        next
        :return:
        """
        try:
            nextrow = next(self._rows)
            self._all_rows.append(nextrow)
            return nextrow
        except StopIteration as e:
            self.pending = False
            raise StopIteration('RecordCollection contains no more rows.')

    def __repr__(self):
        """
        len(self)
        :return:
        """
        rowcount = self._rowcount
        return '<RecordCollection size={} pending={}>'.format(rowcount, self.pending)

    def __getitem__(self, key):
        """
        self[i]
        :param key:
        :return:
        """
        is_int = isinstance(key, int)
        if is_int:
            # 切片对象，slice(start, stop[, step])
            key = slice(key, key + 1)

        while (key.stop is None) or (len(self) < key.stop):
            try:
                next(self)
            except StopIteration:
                break

        rows = self._all_rows[key]
        if is_int:
            return rows[0]
        else:
            return RecordCollection(iter(rows), len(rows))
            # return rows

    # def __iter__(self):
    #     """
    #     Iterate over all rows
    #     :return:
    #     """
    #     i = 0
    #     while True:
    #         if i < len(self):
    #             yield self[i]
    #         else:
    #             try:
    #                 yield next(self)
    #             except StopIteration as e:
    #                 return
    #         i += 1

    def next(self):
        return self.__next__()

    def all(self, as_dict=False):
        """
        Returns a list of all rows for the RecordCollection
        :return:
        """
        # rows = list(self)
        #
        # return rows
        rows = list(self)

        if as_dict:
            return [r.as_dict() for r in rows]

        return rows

    def first(self, default=None, as_dict=False):
        """

        :return:
        """

        try:
            record = self[0]
        except IndexError:
            # if isexception(default):
            #     raise default
            return default

        if as_dict:
            return record.as_dict()

        return record
