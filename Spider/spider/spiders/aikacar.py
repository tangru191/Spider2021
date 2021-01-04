# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper

"""
author:tangru
date: 2018.12.20
function:爱卡汽车数据爬取
"""


class AikacarSpider(CrawlSpider):
    name = "aikacar"
    allowed_domains = ["xcar.com.cn"]
    start_urls = ['http://newcar.xcar.com.cn/car/0-0-0-0-%d-0-0-0-0-0-0-0/' % i for i in range(1, 300)]

    def parse(self, response):
        item = dict()
        brand_id = self.get_brand_id(response)
        """
             品牌入库
             brand_name = response.xpath('//*[@class="title_tj"]/h2/a/text()').extract()
             if brand_name is None:
                 item['app_id'] = "10"
                 yield item
             else:
                 item['app_id'] = "10"
                 item['brand_id'] = brand_id
                 item['brand_name'] = brand_name[0]
                 table = 'datau_crawler_brand'
                 item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                 item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                 CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                 yield item
                 """

        series_name = response.xpath('//*[@class="title"]/a/text()').extract()
        series_url = response.xpath('//*[@class="title"]/a/@href').extract()
        series_id = self.get_series_id(response)

        # 入车系表
        if series_name is None:
            item["app_id"] = '10'
            item["brand_id"] = brand_id
            yield item
        else:
            for i in range(len(series_name)):
                item["app_id"] = '10'
                item["brand_id"] = brand_id
                item["series_id"] = series_id[i]
                item["series_name"] = series_name[i]
                item['series_url'] = "https://a.xcar.com.cn/" + series_id[i] + "/"
                table = 'datau_crawler_carseries'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item

        for series_url_a in series_url:
            series_url_b = "http://newcar.xcar.com.cn" + series_url_a
            yield scrapy.Request(series_url_b, dont_filter=True,
                                 callback=self.vm_page)

    def vm_page(self, response):
        item = dict()
        vm_series_id = self.get_vm_series_id(response)
        vm_name = response.xpath('//*[@class="table_bord"]/td[1]/p[1]/a/text()').extract()
        # vm_url = response.xpath('//*[@class="table_bord"]/td[1]/p[1]/a/@href').extract()
        vm_id = self.get_vm_id(response)
        if vm_name is None:
            item["app_id"] = "10"
            item["series_id"] = vm_series_id
            yield item
        else:
            for i in range(len(vm_name)):
                item["app_id"] = "10"
                item["series_id"] = vm_series_id
                item["vm_name"] = vm_name[i]
                item["vm_id"] = vm_id[i]
                item['vm_url'] = "https://a.xcar.com.cn/" + vm_series_id +\
                                 "/" + vm_id[i] + "/"
                # 向车系表插入爬取数据
                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                # yield item

    @staticmethod
    def get_series_id(response):
        series_url = response.xpath('//*[@class="title"]/a/@href').extract()
        series_id = []
        for series_url_a in series_url:
            series_id_b = re.sub("\D", "", str(series_url_a))
            series_id.append(series_id_b)
        return series_id

    @staticmethod
    def get_vm_series_id(response):
        series_url = response.url
        vm_url_c = re.sub("\D", "", series_url)
        return vm_url_c

    @staticmethod
    def get_vm_id(response):
        vm_url = response.xpath('//*[@class="table_bord"]/td[1]/p[1]/a/@href').extract()
        vm_id = []
        for vm_url_a in vm_url:
            vm_url_c = "m" + re.sub("\D", "", vm_url_a)
            vm_id.append(vm_url_c)
        return vm_id

    @staticmethod
    def get_brand_id(response):
        brand_id_a = response.xpath('//*[@class="title_tj"]/h2/a/@href').extract()[0]
        brand_id = re.sub("\D", "", brand_id_a)
        return brand_id
