# -*- coding: utf-8 -*-

# Define here the models for your scraped Extensions
import logging

from scrapy import signals
from scrapy.exceptions import NotConfigured

logging = logging.getLogger(__name__)

"""
#@Time:2018
#@Author:tangru
本模块解决爬虫请求结束后空跑问题
1、scrapy内部的信号系统会在爬虫耗尽内部队列中的request时，就会触发spider_idle信号。

2、爬虫的信号管理器收到spider_idle信号后，将调用注册spider_idle信号的处理器进行处理。

3、当该信号的所有处理器(handler)被调用后，如果spider仍然保持空闲状态， 引擎将会关闭该spider

"""


class RedisSpiderSmartIdleClosedExensions(object):

    def __init__(self, idle_number, crawler):
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        # 配置仅仅支持RedisSpider
        if 'redis_key' not in crawler.spidercls.__dict__.keys():
            raise NotConfigured('Only supports RedisSpider')
        # get the number of items from settings# 配置空闲持续时间单位默认为360个 ，一个时间单位为5s
        idle_number = crawler.settings.getint('IDLE_NUMBER', 360)

        # instantiate the extension object
        # 实例化扩展对象
        ext = cls(idle_number, crawler)

        # connect the extension object to signals
        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        return ext

    def spider_opened(self, spider):
        spider.logger.info("opened spider {}, Allow waiting time:{} second".format(spider.name, self.idle_number * 5))

    def spider_closed(self, spider):
        spider.logger.info(
            "closed spider {}, Waiting time exceeded {} second".format(spider.name, self.idle_number * 5))

    def spider_idle(self, spider):
        # 程序启动的时候会调用这个方法一次，之后每隔5秒再请求一次
        # 当持续半个小时都没有spider.redis_key，就关闭爬虫
        # 判断是否存在 redis_key
        if not spider.server.exists(spider.redis_key):
            self.idle_count += 1
        else:
            self.idle_count = 0
        # redis中统计的idle_count大于配置中IDLE_NUMBER则将爬虫关闭
        if self.idle_count > self.idle_number:
            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'Waiting time exceeded')
