# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper

"""
author:tangru
date: 2018.12.14
function:太平洋数据爬取
"""


class TaipingyangcarSpider(CrawlSpider):
    name = 'taipingyangcar'
    allowed_domains = ['pcauto.com.cn']
    start_urls = ['https://price.pcauto.com.cn/cars/']
    # start_urls = ['https://price.pcauto.com.cn/cars/#%s' % chr(ord('A') + i) for i in range(26)]

    def parse(self, response):
        item = dict()
        item['app_id'] = "2"
        brand_name = response.xpath('//*[@class="braRow-inner clearfix"]/div/div/a/p/text()').extract()
        # print(bland_name)
        # print(type(bland_name))
        brand_id = self.get_brand_id(response)
        if brand_name is not None:
            for i in range(len(brand_name)):
                item['brand_name'] = brand_name[i]
                item['brand_id'] = brand_id
                # table = 'datau_crawler_brand'
                # item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item
                # print('我是--------------')
    #             # print(item)
        series_url = response.xpath('//*[@class="txtList txtListA clearfix"]/li/p[1]/a/@href').extract()
        for i in series_url:
            series_url_one = "https://price.pcauto.com.cn"+i
            # series_id= re.findall(r"sg\d*", str(series_url_one))
            yield scrapy.Request(series_url_one, meta={'item': item}, dont_filter=True, callback=self.series_page)

    """开始爬取车系页"""
    def series_page(self, response):
        itemseries = response.meta['item']
        app_id = itemseries['app_id']
        # brand_name =itemseries['brand_name']
        # brand_id = itemseries['brand_id']
        item = dict()
        # series_name = response.xpath('//*[@class="dTitW"]/div/h1/@title').extract()
        # series_urla = response.url
        # series_url = str(series_urla).replace('price','m')
        series_id = self.get_series_id(response)
        vm_url = response.xpath('//*[@class="con"]/dl/dd/div/p[1]/a/@href').extract()
        vm_name = self.get_vm_name(response)
        vm_id = self.get_vm_id(response)
        if len(vm_name) == 0:
            item['app_id'] = app_id
            # item['brand_id'] = brand_id
            item['series_id'] = series_id
            # table = 'datau_crawler_vehiclemodel'
            # item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
            yield item
        else:
            for i in range(len(vm_name)):
                item['app_id'] = app_id
                # item['brand_id'] = brand_id
                item['series_id'] = series_id
                # item['series_name'] = series_name
                # item['series_url'] = series_url
                # table = 'datau_crawler_carseries'
                # item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                """
                item['vm_id'] = vm_id[i]
                item['vm_name'] = vm_name[i]
                item['vm_url'] = "https://m.pcauto.com.cn" + vm_url[i]
                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                """
                yield item

    @staticmethod
    def get_brand_id(response):
        brand_id_a = response.xpath('//*[@class="braRow-inner clearfix"]/div/div/a/@href').extract()
        for brand_id_a in brand_id_a:
            brand_id_one = re.findall(r"nb\d*", str(brand_id_a))
            brand_id = (" ".join(brand_id_one))

            return brand_id

    @staticmethod
    def get_series_id(response):
        series_id_a = response.xpath('//*[@name="mobile-agent"]/@content').extract()
        series_id_one = []
        for brand_url_a in series_id_a:
            guide_price_b = brand_url_a.strip()
            guide_price_c = re.findall(r"sg\d*", str(guide_price_b))
            series_id_one.append(guide_price_c)
        series_id_two = series_id_one[0]
        series_id = (" ".join(series_id_two))
        return series_id

    @staticmethod
    def get_vm_name(response):
        vm_name = response.xpath('//*[@class="con"]/dl/dd/div/p[1]/a/text()').extract()
        return vm_name

    @staticmethod
    def get_vm_id(response):
        vm_url = response.xpath('//*[@class="con"]/dl/dd/div/p[1]/a/@href').extract()
        vm_id = []
        for vm_urla in vm_url:
            vm_urlb = vm_urla.strip()
            vm_ida = re.findall(r"m\d*", str(vm_urlb))
            vm_id_c = (" ".join(vm_ida))
            vm_id.append(vm_id_c)
        return vm_id
