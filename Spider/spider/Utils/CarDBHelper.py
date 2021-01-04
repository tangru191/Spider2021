from spider.Utils.MysqlHelper import MysqlHelper
from spider.Utils.dbhelper import DBHelper


"""
#@Time:2018
#@Author:tangru
"""


class DataDBHelper:
    """
      本工具是为了解决爬虫数据插入多个关联表的问题，在dataInsert位置编写sql和相应的插入操作就可以，不用关心item中传过来的数据是什么格式

     """
    def __init__(self):
        self.dbHelper = DBHelper()
    # 创建数据库，有需求的时候可以使用，暂且不用
    # def dataCreateDatebase(self):
    #     self.dbHelper.createDatabase()
    # 创建表操作，有需要的时候可以使用，暂且不用
    # def dataCreateTable(self):
    #     sql = "create table if not exists test2(id int primary key auto_increment,new1 varchar(50),new2 varchar(200))"
    #     self.dbHelper.createTable(sql)
    # 插入数据，这里可以针对不同的表插入数据，piplines传递过来的item存储的是所有数据，可以分类插入不同的表
    # pymysql中也可以在这里对不同的表进行操作，不许需要考虑item数据的传递分类，根据自己的需要取就行，根据需要存即可

    @staticmethod
    def save(**kwargs):
        database = MysqlHelper("10.199.10.2", "ocdp", "ocdp@#123", "carData", "utf8")

        """新增一条记录
          table: 表名
          data: dict 插入的数据
        """
        fields = ','.join('`' + k + '`' for k in kwargs["item"].keys())
        values = ','.join(("%s",) * len(kwargs["item"]))
        sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (kwargs["table"], fields, values)

        database.open()
        '''执行sql'''
        database.curs.execute(sql, tuple(kwargs["item"].values()))
        '''插入记录后取得主键id'''
        insert_id = database.curs.lastrowid
        '''提交修改'''
        database.db.commit()
        database.close()
        # print("存储失败")
        return insert_id
