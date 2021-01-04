import json

from kafka import KafkaConsumer

from Utils.MysqlHelper import MysqlHelper

"""
#@Time:2019
#@Author:tangru
"""


class Kafka_consumer:
    """
    消费模块: 通过不同groupid消费topic里面的消息
    """

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.consumer = KafkaConsumer(self.kafkatopic, group_id=self.groupid,
                                      bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort)
                                      )

    def consume_data(self):
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print(e)


def saveTagTable(**kwargs):
    database = MysqlHelper("10.199.10.5", "dytag_test", "Dytag@test11", "TagVerification", "utf8")

    """
    新增一条记录
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
    return insert_id


def main():

    KAFAKA_HOST = "10.199.10.2"
    KAFAKA_PORT = 6667
    KAFAKA_TOPIC = "data201901031"
    GROUP_ID = "201901031"
    consumer = Kafka_consumer(KAFAKA_HOST, KAFAKA_PORT, KAFAKA_TOPIC, GROUP_ID)
    messages = consumer.consume_data()
    for message in messages:
        itemData = json.loads(message.value.decode('utf-8'))
        print("==================================start_consumer=============================================")
        table = "tag_url"
        item = {
            "top_domain": itemData["top_domain"],
            "url_title": itemData["url_title"],
            "url": itemData["url"],
            "info_id": itemData["info_id"],
            "create_time": itemData["create_time"],
            "update_time": itemData["update_time"]
        }
        saveTagTable(table=table, item=item)
        print("==================================over_consumer=============================================")


if __name__ == '__main__':
    while 1:
        main()
