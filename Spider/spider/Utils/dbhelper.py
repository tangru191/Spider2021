# coding:utf-8
import pymysql
from scrapy.utils.project import get_project_settings  # 引入settings配置

"""
#@Time:2018
#@Author:tangru
本工具为了操作mysql数据库，在爬虫部分主要做插入数据的工作
"""


class DBHelper:
    def __init__(self):
        self.settings = get_project_settings()  # 获取settings配置数据
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

    # 连接mysql
    def connectMysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               charset='utf8')
        return conn

    # 连接数据库
    def connectDatabase(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')
        print("链接数据库成功")
        return conn

    # 创建数据库
    def createDatabase(self):
        conn = self.connectMysql()
        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 创建数据表
    def createTable(self, sql):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 插入数据
    def insert(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()  # 这里；是数据库操作语句结束符号
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    # 更新数据
    def update(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    # 删除数据
    def delete(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()
