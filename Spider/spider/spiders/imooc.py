# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

import ConfigHelper
from spider.Utils import TimeHelper, CarDBHelper


class ImoocSpider(RedisCrawlSpider):
    # global true_socket
    # true_socket = socket.socket
    # global ipbind
    # ipbind = '118.190.145.138'
    #
    #
    # def bound_socket(*a, **k):
    #     sock = true_socket(*a, **k)
    #     sock.bind((ipbind, 0))
    #     return sock
    #
    # socket.socket = bound_socket
    #name = 'imooc'
    name = ConfigHelper.get_config_values('spider_name', 'name')
    # allowed_domains = ['imooc.com']
    # start_urls = ['http://imooc.com/']
    redis_key = 'imooc:start_urls'
    page_lx = LinkExtractor(allow="course/list\?page=\d+")
    content_lx = LinkExtractor(allow="www.imooc.com/learn/\d+")
    rules = (
        Rule(page_lx, follow=True),
        Rule(content_lx, callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = dict()

        table = 'users'
        item['add_time'] = '1'
        item["name"] = self.get_lesson_name(response)
        CarDBHelper.DataDBHelper.save(table=table, item=item)
        item['top_domain'] = 'imooc.com'
        item["url_title"] = self.get_lesson_name(response)
        item['url'] = response.url
        item['info_id'] = '5'
        item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
        item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
        # print(tagItem)
        # CarDBHelper.DataDBHelper.saveTagTable(self=None, table=tagtable, item=tagItem)
        # item["lesson_score"] = self.get_lesson_score(response)
        # item["lesson_grade"] = self.get_lesson_grade(response)
        # item["lesson_time"] = self.get_lesson_time(response)
        # # item["student_number"] = self.get_student_number(response)
        # item["lesson_content"] = self.get_lesson_content(response)
        # item["crawled"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # item["spider"] = ImoocSpider.name
        yield item

    # 课程评分
    @staticmethod
    def get_lesson_score(response):
        lesson_score = response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[5]/span[2]/text()').extract()
        if len(lesson_score) > 0:
            lesson_score = lesson_score[0]
        else:
            lesson_score = ""
        return lesson_score.strip()

    # 课程时长
    @staticmethod
    def get_lesson_time(response):
        lesson_time = response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[3]/span[2]/text()').extract()
        if len(lesson_time) > 0:
            lesson_time = lesson_time[0]
        else:
            lesson_time = ""
        return lesson_time.strip()

    # 课程名称
    @staticmethod
    def get_lesson_name(response):
        lesson_name = response.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/h2/text()').extract()
        if len(lesson_name) > 0:
            lesson_name = lesson_name[0]
        else:
            lesson_name = ""
        return lesson_name.strip()

    # 课程难度
    @staticmethod
    def get_lesson_grade(response):
        lesson_grade = response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[2]/span[2]/text()').extract()
        if len(lesson_grade) > 0:
            lesson_grade = lesson_grade[0]
        else:
            lesson_grade = ""
        return lesson_grade.strip()
        # 学习人数
        # def get_student_number(self, response):
        #     student_number = response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[4]/span[2]/text()').extract()
        #     if len(student_number) > 0:
        #         student_number = student_number
        #     else:
        #         student_number = ""
        #     return student_number.strip()
        # 课程内容

    @staticmethod
    def get_lesson_content(response):
        lesson_content = response.xpath('//*[@id="main"]/div[3]/div[1]/div[1]/div[1]/text()').extract()
        if len(lesson_content) > 0:
            lesson_content = lesson_content[0]
        else:
            lesson_content = ""
        return lesson_content.strip()
