# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper

"""
author:tangru
date: 2018.12.18
function:凤凰汽车数据爬取
"""


class FenghuangcarSpider(CrawlSpider):
    name = "fenghuangcar"
    allowed_domains = ["car.auto.ifeng.com"]
    start_urls = ['http://car.auto.ifeng.com/']

    def parse(self, response):
        item = dict()
        item['app_id'] = "5"
        brand_name = response.xpath('//*[@class="lt-list"]/dl/dt/a[2]/text()').extract()
        brand_id = self.get_brand_id(response)
        # 品牌入库
        if brand_name is not None:
            for i in range(len(brand_name)):
                item['brand_name'] = brand_name[i]
                item['brand_id'] = brand_id[i]
                table = 'datau_crawler_brand'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item
        brand_url = response.xpath('//*[@class="lt-list"]/dl/dt/a[2]/@href').extract()
        for brand_url_aa in brand_url:
            yield scrapy.Request(brand_url_aa,
                                 meta={'item': item}, dont_filter=True, callback=self.series_page)

    def series_page(self, response):
        item = dict()
        itemseries = response.meta['item']
        app_id = itemseries['app_id']
        series_brand_id = self.get_series_brand_id(response)
        # series_url = response.xpath('//*[@class="pw-cars"]/div/a/@href').extract()
        series_name = response.xpath('//*[@class="pw-cars"]/div/a/text()').extract()
        series_id = self.get_series_id(response)
        if series_name is None:
            item["app_id"] = app_id
            item["brand_id"] = series_brand_id
            # 向车系表插入爬取数据
            table = 'datau_crawler_carseries'
            item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
            yield item
        else:
            for i in range(len(series_name)):
                item["app_id"] = app_id
                item["brand_id"] = series_brand_id
                item["series_id"] = series_id[i]
                item["series_name"] = series_name[i]
                item['series_url'] = "https://iauto.ifeng.com/index.php?c=serial&a=index&sid=" + str(series_id[i])
                # 向车系表插入爬取数据
                table = 'datau_crawler_carseries'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item
        # for vm_url_a in series_url:
        #     yield scrapy.Request(vm_url_a, meta={'item': item}, dont_filter=True,
        #                      callback=self.vm_page)

    def vm_page(self, response):
        item = dict()
        itemseries = response.meta['item']
        app_id = itemseries['app_id']
        series_id = self.get_vm_series_id(response)
        vm_id = self.get_vm_id(response)
        vm_name = response.xpath('//*[@class="tit"]/a/text()').extract()
        if vm_name is None:
            item["app_id"] = app_id
            item["series_id"] = series_id
            # 向车系表插入爬取数据
            table = 'datau_crawler_vehiclemodel'
            item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
            yield item
        else:
            for i in range(len(vm_name)):
                item["app_id"] = app_id
                item["series_id"] = series_id
                item["vm_name"] = vm_name[i]
                item["vm_id"] = vm_id[i]
                item['vm_url'] = "https://iauto.ifeng.com/index.php?c=car&a=index&cid=" + str(vm_id[i])
                # 向车系表插入爬取数据
                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item

    @staticmethod
    def get_brand_id(response):
        blandurl = response.xpath('//*[@class="lt-list"]/dl/dt/a[2]/@href').extract()
        bland_url = []
        for blandurla in blandurl:
            blandurlb = re.sub("\D", "", str(blandurla))
            bland_url.append(blandurlb)
        return bland_url

    @staticmethod
    def get_series_brand_id(response):
        series_brand_url = response.url
        series_bland_urla = re.sub("\D", "", series_brand_url)
        return series_bland_urla

    @staticmethod
    def get_series_id(response):
        series_url = response.xpath('//*[@class="pw-cars"]/div/a/@href').extract()
        series_id = []
        for series_id_a in series_url:
            series_id_b = re.sub("\D", "", series_id_a)
            series_id.append(series_id_b)
        return series_id

    @staticmethod
    def get_vm_series_id(response):
        series_url = response.url
        vm_series_id = re.sub("\D", "", series_url)
        return vm_series_id

    @staticmethod
    def get_vm_id(response):
        vm_url = response.xpath('//*[@class="tit"]/a/@href').extract()
        vm_id = []
        for vm_url_a in vm_url:
            vm_id_a = re.sub("\D", "", vm_url_a)
            vm_id.append(vm_id_a)
        return vm_id
