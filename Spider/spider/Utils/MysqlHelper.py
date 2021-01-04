# -*- coding:UTF-8 -*-

import pymysql as ps

"""
#@Time:2018
#@Author:tangru
本部分为操作mysql数据库工具类
"""


class MysqlHelper:
    def __init__(self, host, user, password, database, charset):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db = None
        self.curs = None

    def open(self):
        self.db = ps.connect(host=self.host, user=self.user, password=self.password,
                             database=self.database, charset=self.charset)
        self.curs = self.db.cursor()

    def close(self):
        self.curs.close()
        self.db.close()

    def cud(self, sql, params):
        self.open()
        try:
            self.curs.execute(sql, params)
            self.db.commit()
            print("ok")
        except Exception:
            print("cud出现错误")
            self.db.rollback()
        self.close()

    def find(self, sql, params):
        self.open()
        try:
            result = self.curs.execute(sql, params)
            self.close()
            print("ok")
            return result
        except Exception:
            print("find出现错误")
