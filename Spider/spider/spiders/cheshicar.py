# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper

"""
author:tangru
date: 2018.12.21
function:网上车市网站汽车数据爬取
"""


class CheshicarSpider(CrawlSpider):
    name = "cheshicar"
    allowed_domains = ["cheshi.com"]
    # start_urls = ['http://product.cheshi.com/static/selectcar/%s.html'% chr(ord('A') + i) for i in range(2)]
    start_urls = ['http://product.cheshi.com/static/selectcar/%s.html'
                  % chr(ord('A') + i) for i in range(26)]

    def parse(self, response):
        item = dict()
        brand_id = self.get_brand_id(response)
        brand_url = response.xpath('//*[@class="list-box"]/div/a/@href').extract()
        if brand_id is not None:
            for i in range(len(brand_id)):
                item["brand_id"] = brand_id[i]
                item["brand_url"] = brand_url[i]
                # yield item
                yield scrapy.Request(brand_url[i], meta={'item': item}, dont_filter=True,
                                     callback=self.series_page)

    def series_page(self, response):
        itemseries = response.meta['item']
        brand_id = itemseries['brand_id']
        item = dict()
        series_id = self.get_series_id(response)
        series_name = response.xpath('//*[@class="p_list"]/strong/a/text()').extract()
        series_url = response.xpath('//*[@class="p_list"]/strong/a/@href').extract()
        if series_id is not None:
            for i in range(len(series_id)):
                item["app_id"] = "12"
                item["brand_id"] = brand_id
                item["series_id"] = series_id[i]
                item["series_name"] = series_name[i]
                item["series_url"] = "https://a.cheshi.com/" + str(series_id[i]) + "/"
                # # 向车系表插入爬取数据
                table = 'datau_crawler_carseries'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                series_url_one = series_url[i]
                yield scrapy.Request(series_url_one, meta={'item': item}, dont_filter=True,
                                     callback=self.vm_page)

    def vm_page(self, response):
        itemchexing = response.meta['item']
        series_id = itemchexing['series_id']
        item = dict()
        vm_name = self.get_vm_name(response)
        # vm_url = response.xpath('//*[@class="table-compare-box"]/table/tbody/tr/td/div[1]/a/@href').extract()
        vm_id = self.get_vm_id(response)
        if vm_id is not None:
            for i in range(len(vm_id)):
                item["app_id"] = "12"
                item["series_id"] = series_id
                item["vm_id"] = vm_id[i]
                item["vm_name"] = vm_name[i]
                item["vm_url"] = "https://a.cheshi.com/" + str(vm_id[i]) + "/"
                # 向车型表插入爬取数据
                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item

        """
        item = dict()
        brand_name = response.xpath('//*[@class="list-box"]/div/a/span/text()').extract()
        brand_id = self.get_brand_id(response)
        # series_name = response.xpath('//*[@class="clearfix"]/dd/div/h4/a/text()').extract()
        # series_url = response.xpath('//*[@class="clearfix"]/dd/div/h4/a/text()').extract()
        # 品牌名和品牌id字段到品牌表
        if brand_id is not None:
            for i in range(len(brand_id)):
                item["app_id"] = "12"
                item["brand_name"] = brand_name[i]
                item["brand_id"] = brand_id[i]
                table = 'datau_crawler_brand'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item
            """

    @staticmethod
    def get_brand_id(response):
        brand_url = response.xpath('//*[@class="list-box"]/div/a/@href').extract()
        brand_id = []
        for brand_url_a in brand_url:
            brand_url_d = "logo_" + re.sub("\D", "", str(brand_url_a))
            brand_id.append(brand_url_d)
        return brand_id

    @staticmethod
    def get_series_id(response):
        series_url = response.xpath('//*[@class="p_list"]/strong/a/@href').extract()
        series_id = []
        for series_urla in series_url:
            series_urlb = "bseries_" + re.sub("\D", "", str(series_urla))
            series_id.append(series_urlb)
        return series_id

    @staticmethod
    def get_vm_name(response):
        vm_namea = response.xpath('//*[@class="table-compare-box"]/table/tbody/tr/td/div[1]/a/text()').extract()
        vm_name = []
        for vm_nameb in vm_namea:
            vm_namec = "".join(vm_nameb.split())
            vm_name.append(vm_namec)
        return vm_name

    @staticmethod
    def get_vm_id(response):
        vm_url = response.xpath('//*[@class="table-compare-box"]/table/tbody/tr/td/div[1]/a/@href').extract()
        vm_id = []
        for vm_urla in vm_url:
            vm_urlb = "model_" + re.sub("\D", "", str(vm_urla))
            vm_id.append(vm_urlb)
        return vm_id
