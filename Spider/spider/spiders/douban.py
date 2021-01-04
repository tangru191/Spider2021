# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from spider.Utils import ConfigHelper


class DoubanSpider(RedisCrawlSpider):
    pass
    # name = ConfigHelper.get_config_values('spider_name', 'name')
    # #allowed_domains = ['douban.com']
    # #start_urls = ['http://douban.com/']
    # redis_key = ConfigHelper.get_config_values('start_urls', 'start_urls')
    # page_lx = LinkExtractor(allow=ConfigHelper.get_config_values('lx', 'page_lx'))
    # content_lx = LinkExtractor(allow=ConfigHelper.get_config_values('lx', 'content_lx'))
    # rules = (
    #     Rule(page_lx, follow=True),
    #     Rule(content_lx, callback='parse_item', follow=False),
    # )
    #
    # def parse_item(self, response):
    #     item = dict()
    #     item['num'] = self.get_num(response)
    #     item['title'] = self.get_title(response)
    #     item['type'] = self.get_type(response)
    #     item['time'] = self.get_time(response)
    #     # item['content'] = self.get_content(response)
    #     print(item)
    #     #yield item
    #
    # def get_num(self, response):
    #     num = response.xpath(ConfigHelper.get_config_values('xpath', 'num')).extract()[0]
    #     if len(num) > 0:
    #         num = num.strip()
    #     else:
    #         num = "NULL"
    #     return num
    #
    # def get_title(self, response):
    #     title = response.xpath(ConfigHelper.get_config_values('xpath', 'title')).extract()[0]
    #     if len(title) > 0:
    #         title = title.strip()
    #     else:
    #         title = 'null'
    #     return title
    #
    # def get_type(self, response):
    #     type = response.xpath(ConfigHelper.get_config_values('xpath', 'type')).extract()[0]
    #     if len(type) > 0:
    #         type = type.strip()
    #     else:
    #         type = 'null'
    #     return type
    #
    # def get_time(self, response):
    #     time = response.xpath(ConfigHelper.get_config_values('xpath', 'time')).extract()[0]
    #     if len(time) > 0:
    #         time = time.strip()
    #     else:
    #         time = "null"
    #     return time
    # # def get_content(self,response):
    # #     content  = response.xpath('//*[@id="link-report"]/span[1]/span/text()[1]')
    # #     if len(content) > 0:
    # #         content = content
    # #     else:
    # #         content = 'null'
    # #     return content
