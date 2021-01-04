# -*- coding: utf-8 -*-
import scrapy
import re
import json
import urllib
from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper

"""
author:tangru
date: 2018.12.21
function:车讯汽车网站数据爬取
"""


class ChexuncarSpider(CrawlSpider):
    name = "chexuncar"
    allowed_domains = ["chexun.com"]
    start_urls = ['http://auto.chexun.com/']

    def parse(self, response):
        item = dict()
        """
        品牌名，品牌id的爬取和插入
        ratehtml = urllib.request.urlopen('http://auto.chexun.com/api/car/brand.do')
        # print(ratehtml)
        # 通过read方法获取返回数据
        priceminhtmlone = ratehtml.read()
        # 将返回的json格式的数据转化为python对象，json数据转化成了python中的字典，按照字典方法读取数据
        priceminhtmlt = json.loads(priceminhtmlone)
        prione = str(priceminhtmlt)
        jsonblandid = re.findall(r" \'brandId\':([^\:]\d*)", prione)
        jsonblandname = re.findall(r"brandName\':([^\:]*)\',", prione)
        blandname = []
        for blandnameone in jsonblandname:
            blandnametwo = blandnameone.replace('\'', '')
            blandname.append(blandnametwo)
        for i in range(len(jsonblandid)):
            item['app_id'] = "11"
            item['brand_id'] = jsonblandid[i]
            item['brand_name'] = blandname[i]
            table = 'datau_crawler_brand'
            item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
          """
        seriesurl = ['http://auto.chexun.com/api/car/seriesByLetter.do?letter=%s'
                     % chr(ord('A') + i) for i in range(26)]
        for seriesurla in seriesurl:
            serieshtml = urllib.request.urlopen(seriesurla)
            # 通过read方法获取返回数据
            serieshtmlone = serieshtml.read()
            # 将返回的json格式的数据转化为python对象，json数据转化成了python中的字典，按照字典方法读取数据
            serieshtmltwo = json.loads(serieshtmlone)
            seriesa = str(serieshtmltwo['seriesMap'])
            # print(seriesa)
            jsonblandseriesid = re.findall(r" \'brandId\':([^:]\d*)", seriesa)
            jsonseriesid = re.findall(r"seriesId\':([^:]\d*)", seriesa)
            jsonseriesname = re.findall(r"seriesName\':([^:]*)\',", seriesa)
            englishname = re.findall(r"englishName\':([^:]*)\',", seriesa)
            print(jsonblandseriesid)
            seriesname = []
            for jsonseriesnamea in jsonseriesname:
                jsonseriesnameb = jsonseriesnamea.replace('\'', '')
                seriesname.append(jsonseriesnameb)
            englishnamea = []
            for englishnameb in englishname:
                englishnamec = englishnameb.replace('\'', '')
                englishnamea.append(englishnamec)
            for i in range(len(seriesname)):
                item['series_id'] = jsonseriesid[i].strip()
                series_url = "http://auto.chexun.com/" + englishnamea[i].strip() + "/"
                yield scrapy.Request(series_url, meta={'item': item}, dont_filter=True,
                                     callback=self.vm_page)

    @staticmethod
    def vm_page(response):
        item = dict()
        itemseries = response.meta['item']
        series_id = itemseries['series_id']
        # series_url = response.url
        vm_name = response.xpath('//*[@class="car-list-bd"]/dd/div[1]/a/text()').extract()
        vm_id = response.xpath('//*[@class="car-list-bd"]/dd/@tabindex').extract()
        vm_url = response.xpath('//*[@class="car-list-bd"]/dd/div[1]/a/@href').extract()
        if vm_name is not None:
            for i in range(len(vm_name)):
                item["app_id"] = "11"
                item["series_id"] = series_id
                item['vm_id'] = vm_id[i]
                item['vm_name'] = vm_name[i]
                item['vm_url'] = vm_url[i]
                # 向车型表插入爬取数据
                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item
        """  
            车系爬取及插入
            for i in range(len(seriesname)):
                item['app_id'] = "11"
                item['brand_id'] = jsonblandseriesid[i].strip()
                item['series_id'] = jsonseriesid[i].strip()
                item['series_name'] = seriesname[i].strip()
                item['series_url'] = "http://auto.chexun.com/" + englishnamea[i].strip() + "/"
                # # 向车系表插入爬取数据
                table = 'datau_crawler_carseries'
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)               
        """
