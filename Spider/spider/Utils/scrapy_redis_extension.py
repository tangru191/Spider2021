# -*- coding: utf-8 -*-
import time
from venv import logger

from scrapy import signals

"""
#@Time:2018
#@Author:tangru
本模块解决爬虫请求结束后空跑问题
1、scrapy内部的信号系统会在爬虫耗尽内部队列中的request时，就会触发spider_idle信号。

2、爬虫的信号管理器收到spider_idle信号后，将调用注册spider_idle信号的处理器进行处理。

3、当该信号的所有处理器(handler)被调用后，如果spider仍然保持空闲状态， 引擎将会关闭该spider

"""


class RedisSpiderClosedExensions  (object):

    def __init__(self, idle_number, crawler):
        self.crawler = crawler
        # 等待时间
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # IDLE_NUMBER目前被设定为等待时间，IDLE一个时间片5秒，所以setting.py中设置的时间除以5就是时间片的数量
        idle_number = crawler.settings.getint('IDLE_TIME', 600) // 5
        # 实例化扩展对象
        ext = cls(idle_number, crawler)
        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s redis spider Idle, Continuous idle limit： %d", spider.name, self.idle_number)

    def spider_closed(self, spider):
        logger.info("closed spider %s, idle count %d , Continuous idle count %d",
                    spider.name, self.idle_count, len(self.idle_list))

    def spider_idle(self, spider):
        # 空闲计数
        self.idle_count += 1
        # 每次触发 spider_idle时，记录下触发时间戳
        self.idle_list.append(time.time())
        # 获取当前已经连续触发的次数
        idle_list_len = len(self.idle_list)
        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_number:
            idle_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.idle_list[0]))
            idle_close_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.idle_list[0]))
            # 连续触发的次数达到配置次数后关闭爬虫
            logger.info('\n continued idle number exceed {} Times'
                        '\n meet the idle shutdown conditions, will close the reptile operation'
                        '\n idle start time: {},  close spider time: {}'.format(self.idle_number, idle_start_time,
                                                                                idle_close_time))
            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')
