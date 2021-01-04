# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper

"""
author:tangru
date: 2018.12.19
function:搜狐汽车数据爬取
"""


class SohucarSpider(CrawlSpider):
    name = "sohucar"
    allowed_domains = ["sohu.com"]
    start_urls = ['http://db.auto.sohu.com/home/']

    def parse(self, response):
        item = dict()
        brand_name = self.get_brand_name(response)
        brand_id = response.xpath('//*[(@class="brand_tit")]/a/@id').extract()

        """
        # 品牌入库
        for i in range(len(brand_name)):
            item['app_id'] = "6"
            item['brand_name'] = brand_name[i]
            item['brand_id'] = brand_id[i]
            table = 'datau_crawler_brand'
            item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
            CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
            yield item
            """
        brand_url = response.xpath('//*[(@class="brand_tit")]/a/@href').extract()
        for brand_url_aa in brand_url:

            yield scrapy.Request("http://" + brand_url_aa, dont_filter=True,
                                 callback=self.series_page)

    def series_page(self, response):
        item = dict()
        series_brand_id = self.get_series_brand_id(response)
        series_name = self.get_series_name(response)
        series_url = response.xpath('//*[@class="tabcon cur"]/ul/li/a/@href').extract()
        series_id = self.get_series_id(response)
        """
        入车系表
        if series_name is None:
            item["app_id"] = '6'
            item["brand_id"] = series_brand_id
            # # 向车系表插入爬取数据
            # table = 'datau_crawler_carseries'
            # item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
            yield item
        else:
            for i in range(len(series_name)):
                item["app_id"] = '6'
                item["brand_id"] = series_brand_id
                item["series_id"] = series_id[i]
                item["series_name"] = series_name[i]
                item['series_url'] = "http:"+ series_url[i]
                向车系表插入爬取数据
                table = 'datau_crawler_carseries'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item
                """
        for series_url_a in series_url:
            series_url_b = "http:" + series_url_a
            yield scrapy.Request(series_url_b, meta={'item': item}, dont_filter=True,
                                 callback=self.vm_page)

    def vm_page(self, response):
        item = dict()
        vm_series_id = self.get_vm_series_id(response)
        vm_name = response.xpath('//*[@class="b jsq"]/table/tbody/tr/td[1]/a/text()').extract()
        vm_url = response.xpath('//*[@class="b jsq"]/table/tbody/tr/td[1]/a/@href').extract()
        vm_id = self.get_vm_id(response)
        if vm_name is None:
            item["app_id"] = "6"
            item["series_id"] = vm_series_id
            yield item
        else:
            for i in range(len(vm_name)):
                item["app_id"] = "6"
                item["series_id"] = vm_series_id
                item["vm_name"] = vm_name[i]
                item["vm_id"] = vm_id[i]
                item['vm_url'] = "http:" + vm_url[i]
                # 向车系表插入爬取数据
                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item

    @staticmethod
    def get_brand_name(response):
        brand_name_a = response.xpath('//h4[normalize-space(@class="brand_tit")]/a/text()').extract()
        brand_name = []
        for brand_name_b in brand_name_a:
            nicknameb = brand_name_b.strip()
            brand_name.append(nicknameb)
        while '' in brand_name:
            brand_name.remove('')
        return brand_name

    @staticmethod
    def get_series_name(response):
        series_name_a = response.xpath('//*[@class="tabcon cur"]/ul/li/a/span/text()')\
            .extract()
        series_name = []
        for series_name_b in series_name_a:
            series_name_c = series_name_b.strip()
            series_name.append(series_name_c)
        while '' in series_name:
            series_name.remove('')
        return series_name

    @staticmethod
    def get_series_brand_id(response):
        series_brand_url = response.url
        series_bland_urla = re.sub("\D", "", series_brand_url)
        return series_bland_urla

    @staticmethod
    def get_series_id(response):
        series_url = response.xpath('//*[@class="tabcon cur"]/ul/li/a/@href').extract()
        series_id = []
        for series_url_a in series_url:
            series_id_a = re.findall(r"(/\d*)", str(series_url_a))
            series_id_b = re.sub("\D", "", str(series_id_a))
            series_id.append(series_id_b)
        return series_id

    @staticmethod
    def get_vm_series_id(response):
        series_url = response.url
        vm_series_id = re.sub("\D", "", series_url)
        return vm_series_id

    @staticmethod
    def get_vm_id(response):
        vm_url = response.xpath('//*[@class="b jsq"]/table/tbody/tr/td[1]/a/@href').extract()
        vm_id = []
        for vm_url_a in vm_url:
            vm_url_b = re.findall(r"(/\d*\?)", str(vm_url_a))
            vm_url_b = (" ".join(vm_url_b))
            vm_url_c = re.sub("\D", "", vm_url_b)
            vm_id.append(vm_url_c)
        return vm_id
