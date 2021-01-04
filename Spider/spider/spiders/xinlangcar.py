# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper


class XinlangcarSpider(CrawlSpider):
    name = "xinlangcar"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://db.auto.sina.com.cn/b%d.html' % i for i in range(230)]

    def parse(self, response):
        item = dict()
        item['app_id'] = '3'
        # 品牌id
        brand_id = self.get_brand_id(response)
        # 品牌名字
        brand_name = self.get_brand_name(response)
        # 品牌url
        brand_url = response.url
        if len(brand_name) > 0:
            item['brand_name'] = brand_name
            item['brand_id'] = brand_id

            table = 'datau_crawler_brand'
            item['create_time'] = TimeHelper.TimeHelper.getTime()
            item['update_time'] = TimeHelper.TimeHelper.getTime()
            CarDBHelper.DataDBHelper.save(table=table, item=item)

            yield scrapy.Request(brand_url, dont_filter=True, callback=self.brand_page)

    def brand_page(self, response):
        item = dict()
        item['app_id'] = '3'
        # 品牌id
        brand_id = self.get_brand_id(response)
        # 车系id
        series_id = self.get_series_id(response)
        # 车系名字
        series_name = response.xpath('//*[@class="like235 clearfix"]/li/p[1]/a/text()').extract()
        # 车系url
        series_url_list = response.xpath('//*[@class="like235 clearfix"]/li/p[1]/a/@href').extract()
        if len(series_name) > 0:
            for i in range(len(series_name)):
                item['brand_id'] = brand_id
                item['series_id'] = series_id[i]
                item['series_name'] = series_name[i]
                item['series_url'] = 'http:'+series_url_list[i]

                table = 'datau_crawler_carseries'
                item['create_time'] = TimeHelper.TimeHelper.getTime()
                item['update_time'] = TimeHelper.TimeHelper.getTime()
                CarDBHelper.DataDBHelper.save(table=table, item=item)

                series_url = "http:"+series_url_list[i]
                yield scrapy.Request(series_url, meta={'item': item}, dont_filter=True, callback=self.series_page)

    @staticmethod
    def series_page(response):
        itemseries = response.meta['item']
        series_id = itemseries['series_id']
        item = dict()
        item['app_id'] = '3'
        # 车型id
        vm_id = response.xpath('//*[@class="cartype_list lump"]/table/tbody/tr/td[5]/div/@carid').extract()
        # 车型名称
        vm_name = response.xpath('//*[@class="cartype_list lump"]/table/tbody/tr/td[1]/a/span/text()').extract()
        # 车型url
        vm_url = response.xpath('//*[@class="cartype_list lump"]/table/tbody/tr/td[1]/a/@href').extract()
        if len(vm_name) > 0:
            for i in range(len(vm_name)):
                item['series_id'] = series_id
                item['vm_id'] = vm_id[i]
                item['vm_name'] = vm_name[i]
                item['vm_url'] = vm_url[i]

                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime()
                item['update_time'] = TimeHelper.TimeHelper.getTime()
                CarDBHelper.DataDBHelper.save(table=table, item=item)

    @staticmethod
    def get_brand_id(response):
        brand_id_a = response.xpath('//*[@class="current"]/a/@data-id').extract()
        if len(brand_id_a) > 0:
            brand_id = brand_id_a[0]
        else:
            brand_id = ''
        return brand_id

    @staticmethod
    def get_brand_name(response):
        brand_name_one = response.xpath('//*[@class="h1-bar clearfix"]/div/h1/text()').extract()
        if len(brand_name_one) > 0:
            brand_name = brand_name_one[0]
        else:
            brand_name = ''
        return brand_name

    @staticmethod
    def get_series_id(response):
        series_url = response.xpath('//*[@class="like235 clearfix"]/li/p[1]/a/@href').extract()
        series_id = []
        for series_urla in series_url:
            series_urlb = re.sub("\D", "", str(series_urla))
            series_id.append(series_urlb)
        return series_id
