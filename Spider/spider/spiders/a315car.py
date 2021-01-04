# -*- coding: utf-8 -*-
import scrapy
from spider.Utils import TimeHelper, CarDBHelper


class A315carSpider(scrapy.Spider):
    name = 'a315car'
    allowed_domains = ['315che.com']
    start_urls = ['http://auto.315che.com/']

    def parse(self, response):

        item = dict()
        item['app_id'] = '8'
        # 品牌id
        brand_id = self.get_brand_id(response)
        # 品牌名字
        brand_name = response.xpath('//*/dl/dt/a/div/text()').extract()
        # 品牌页url
        brand_url = response.url
        brand_id = response.url
        for i in range(len(brand_name)):
            item['brand_id'] = brand_id[i]
            item['brand_name'] = brand_name[i]

            table = 'datau_crawler_brand'
            item['create_time'] = TimeHelper.TimeHelper.getTime()
            item['update_time'] = TimeHelper.TimeHelper.getTime()
            CarDBHelper.DataDBHelper.save(table=table, item=item)

        yield scrapy.Request(brand_url, dont_filter=True, callback=self.brand_page)

    def brand_page(self, response):
        item = dict()
        item['app_id'] = '8'
        # 品牌块
        brand_block = response.xpath('//*[@class="uibox-con auto-library "]/dl')
        for part in brand_block:
            # 品牌id
            brand_id = self.get_brand_id_2(part)
            # 车系id
            series_id = self.get_series_id(part)
            # 车系名字
            series_name = part.xpath('dd/div/ul/li/a/text()').extract()
            # 车系url
            series_url_list = part.xpath('dd/div/ul/li/a/@href').extract()
            if len(series_name) > 0:
                for i in range(len(series_name)):
                    item['brand_id'] = brand_id
                    item['series_id'] = series_id[i]
                    item['series_name'] = series_name[i]
                    item['series_url'] = series_url_list[i]

                    table = 'datau_crawler_carseries'
                    item['create_time'] = TimeHelper.TimeHelper.getTime()
                    item['update_time'] = TimeHelper.TimeHelper.getTime()
                    CarDBHelper.DataDBHelper.save(table=table, item=item)

                    series_url = series_url_list[i]
                    yield scrapy.Request(series_url, meta={'item': item}, dont_filter=True, callback=self.series_page)

    def series_page(self, response):
        itemseries = response.meta['item']
        series_id = itemseries['series_id']
        item = dict()
        item['app_id'] = '8'
        # 车型id
        vm_id = self.get_vm_id(response)
        # 车型名字
        vm_name = response.xpath('//*[@id="onsale"]/dl/dd/div[1]/span/a/text()').extract()
        # 车型url
        vm_url_list = response.xpath('//*[@id="onsale"]/dl/dd/div[1]/span/a/@href').extract()
        if len(vm_name) > 0:
            for i in range(len(vm_name)):
                item['series_id'] = series_id
                item['vm_id'] = vm_id[i]
                item['vm_name'] = vm_name[i]
                item['vm_url'] = vm_url_list[i]

                table = 'datau_crawler_vehiclemodel'
                item['create_time'] = TimeHelper.TimeHelper.getTime()
                item['update_time'] = TimeHelper.TimeHelper.getTime()
                CarDBHelper.DataDBHelper.save(table=table, item=item)

    @staticmethod
    def get_brand_id(response):
        brand_id = response.xpath('//*/dl/dt/a/@href').extract()
        for i in range(len(brand_id)):
            brand_id[i] = brand_id[i].replace('http://che.315che.com/', '')
            brand_id[i] = brand_id[i].replace('/', '')
        return brand_id

    @staticmethod
    def get_brand_id_2(response):
        brand_id = response.xpath('dt/a/@href').extract()
        for i in range(len(brand_id)):
            brand_id[i] = brand_id[i].replace('http://che.315che.com/', '')
            brand_id[i] = brand_id[i].replace('/', '')
        return brand_id[0]

    @staticmethod
    def get_series_id(response):
        series_id = response.xpath('dd/div/ul/li/a/@href').extract()
        for i in range(len(series_id)):
            series_id[i] = series_id[i].replace('http://auto.315che.com/', '')
            series_id[i] = series_id[i].replace('/', '')
        return series_id

    @staticmethod
    def get_vm_id(response):
        vm_id = response.xpath('//*[@id="onsale"]/dl/dd/div[1]/span/a/@href').extract()
        for i in range(len(vm_id)):
            vm_id[i] = vm_id[i].replace('http://che.315che.com/', '')
            vm_id[i] = vm_id[i].replace('/', '')
        return vm_id
