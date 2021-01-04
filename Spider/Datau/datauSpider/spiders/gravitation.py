# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datauSpider.items import *
from datauSpider.loaders import *
from datauSpider.utils import get_config
from datauSpider import urls
from datauSpider.rules import rules


class UniversalSpider(CrawlSpider):
    name = 'gravitation'
    '''
    在启动爬虫的时候先获取爬虫的相关配置
    '''
    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        # 获取配置文件rules
        self.rules = rules.get(config.get('rules'))
        # 获取start_urls 此处的url是分为单条和多条的形式  按照static和dynamic进行区分
        start_urls = config.get('start_urls')
        if start_urls:
            # static类型  直接获取url开始爬虫
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('args')
            # dynamic类型的需对url进行加工 然后开始爬虫，start_urls必须为list类型
            elif start_urls.get('type') == 'dynamic':
                self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
        # 获取allowed_domains  过滤掉非本allowed_domains的url
        self.allowed_domains = config.get('allowed_domains')
        super(UniversalSpider, self).__init__(*args, **kwargs)
    
    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)
            # 动态获取属性配置
            for key, value in item.get('attrs').items():
                for extractor in value:
                    #属性为xpath的情况
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    # 属性为css的情况
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    # 属性直接为value的情况
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    #属性为元素attr的形式
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()