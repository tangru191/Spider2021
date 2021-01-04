# -*- coding: utf-8 -*-
import scrapy
import re
import urllib
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper


"""
author:tangru
date: 2018.12.25
function:qq汽车网站数据爬取
"""


class QqcarSpider(CrawlSpider):
    name = "qqcar1.0"
    allowed_domains = ["qq.com"]
    start_urls = ['http://data.auto.qq.com/car_brand/index.shtml']

    def parse(self, response):
        item = dict()
        listhtml = urllib.request.urlopen('http://js.data.auto.qq.com/car_public/1/manufacturer_list_json.js')
        # 通过read方法获取返回数据
        listhtmlone = listhtml.read()
        # print(listhtmlone)
        listone = str(listhtmlone)
        jsonbrandid = re.findall(r"ID:\"([^\"]\d*)\",", listone)
        for brandid in jsonbrandid:
            item['brand_id'] = brandid
            brandurl = "http://data.auto.qq.com/car_brand/" + str(brandid) + "/"
            yield scrapy.Request(brandurl, meta={'item': item}, dont_filter=True,
                                 callback=self.brand_page)

    def brand_page(self, response):
        item = dict()
        itemsebrand = response.meta['item']
        brand_id = itemsebrand['brand_id']
        brand_name = response.xpath('//*[@class="gary333"]/text()').extract()
        series_name = response.xpath('//*[@class="fl lan2 font16 fontbold"]/a/text()').extract()
        series_id = self.get_series_id(response)
        if series_name is not None:
            for i in range(len(series_name)):
                item['app_id'] = "7"
                item['series_id'] = series_id[i]
                series_url = "http://data.auto.qq.com/car_serial/" + str(series_id[i]) + "/index.shtml"
                yield scrapy.Request(series_url, meta={'item': item}, dont_filter=True,
                                     callback=self.series_page)

    def series_page(self, response):
        item = dict()
        itemsebrand = response.meta['item']
        series_id = itemsebrand['series_id']
        vm_name = response.xpath('//*[@class="tagBods_serial dis"]/table/tbody/tr/td/h3/a/text()').extract()
        vm_url = response.xpath('//*[@class="tagBods_serial dis"]/table/tbody/tr/td/h3/a/@href').extract()
        vm_id = self.get_vm_id(response)
        if vm_name is not None:
            for i in range(len(vm_name)):
                item['app_id'] = "7"
                item['series_id'] = series_id
                item['vm_id'] = vm_id[i]
                item['vm_name'] = vm_name[i]
                item['vm_url'] = "http://data.auto.qq.com" + vm_url[i]
                # 向车型表插入爬取数据
                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item

    @staticmethod
    def get_series_id(response):
        series_url = response.xpath('//*[@class="fl lan2 font16 fontbold"]/a/@href').extract()
        series_id = []
        for series_urla in series_url:
            series_urlb = re.sub("\D", "", str(series_urla))
            series_id.append(series_urlb)
        return series_id

    @staticmethod
    def get_vm_id(response):
        vm_url = response.xpath('//*[@class="tagBods_serial dis"]/table/tbody/tr/td/h3/a/@href').extract()
        vm_id = []
        for vm_urla in vm_url:
            vm_urlb = re.sub("\D", "", str(vm_urla))
            vm_id.append(vm_urlb)
        return vm_id
    """
    item['brand_id'] = brand_id
    item['series_id'] = series_id[i]
    item['series_name'] = series_name[i]
    item['series_url'] = "http://w.auto.qq.com/car_serial/" + str(series_id[i]) + "/index.shtml"
    # # 向车系表插入爬取数据
    table = 'datau_crawler_carseries'
    item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
    item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
    # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
    """


"""
item['brand_name'] = brand_name[0]
table = 'datau_crawler_brand'
item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
# CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
"""
