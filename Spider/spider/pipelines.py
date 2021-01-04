# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import kafka
import pymongo
from scrapy.conf import settings

from spider.Utils.CarDBHelper import DataDBHelper
import json
import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from spider.Utils.MysqlHelper import MysqlHelper
from spider.Utils import CarDBHelper


class SpiderPipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        # data = dict(item)
        # self.post.insert(data)
        return item


class QiCheZhiJiaPipeline(object):
    def __init__(self):
        # 连接数据库
        self.db = DataDBHelper()

    # 处理存数据入数据库
    def process_item(self, item, spider):
        # self.save(table=table,item=item)
        return item


class KafkaProducerPipeline(object):
    def __init__(self):
        self.kafkaHost = settings["KAFAKA_HOST"]
        self.kafkaPort = settings["KAFAKA_PORT"]
        self.kafkatopic = settings["KAFAKA_TOPIC"]
        self.key = settings["KAFKA_KEY"]
        self.groupid = settings["GROUP_ID"]

    def process_item(self, item, spider):
        producer = Kafka_producer(self.kafkaHost,self.kafkaPort,self.kafkatopic)
        producer.sendjsondata(item)


    def spider_closed(self, spider):
        # 当爬虫请求结束以后发送结束爬虫信息，则打开的浏览器关闭
        print('spider closed')
        for _, k in kafka.iteritems():
            k.producer.stop()


class Kafka_producer():
    """
    使用kafka的生产模块
    """

    def __init__(self, kafkahost, kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(
            bootstrap_servers='{kafka_host}:{kafka_port}'.format(kafka_host=self.kafkaHost, kafka_port=self.kafkaPort)
        )

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafkatopic, parmas_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print(e)