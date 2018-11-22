# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""
from orm.data_base import Database


def main():
    url = 'mysql://root:zy123456@localhost/wiki?charset=utf8'
    db = Database(url)

    sql = 'select * from tb_user'
    rows = db.query(sql)

    print(rows)

    print(rows[0])  # Record

    for r in rows:
        print(r.id, r.username)

    print(rows.all())  # [Record, Record]
    print(rows.first())  # Record


if __name__ == '__main__':
    main()
