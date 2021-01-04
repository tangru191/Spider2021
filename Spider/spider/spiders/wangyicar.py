# -*- coding: utf-8 -*-
import scrapy
from spider.Utils import TimeHelper, CarDBHelper


class WangyicarSpider(scrapy.Spider):
    name = 'wangyicar'
    allowed_domains = ['163.com']
    start_urls = ['http://product.auto.163.com']

    def parse(self, response):
        item = dict()
        item['app_id'] = '4'
        # 品牌id
        brand_id = response.xpath('//*[@id="brandCont"]/*/h2/a/@id').extract()
        # 品牌名字
        brand_name = response.xpath('//*[@id="brandCont"]/*/h2/a/@title').extract()
        # 品牌页url
        brand_url_list = response.xpath('//*[@id="brandCont"]/*/h2/a/@href').extract()
        if len(brand_name) > 0:
            for i in range(len(brand_name)):
                item['brand_id'] = brand_id[i]
                item['brand_name'] = brand_name[i]

                table = 'datau_crawler_brand'
                item['create_time'] = TimeHelper.TimeHelper.getTime()
                item['update_time'] = TimeHelper.TimeHelper.getTime()
                CarDBHelper.DataDBHelper.save(table=table, item=item)

                brand_url = 'http://product.auto.163.com'+brand_url_list[i]
                yield scrapy.Request(brand_url, meta={'item': item}, dont_filter=True, callback=self.brand_page)

    def brand_page(self, response):
        itembrand = response.meta['item']
        brand_id = itembrand['brand_id']
        item = dict()
        item['app_id'] = '4'
        # 车系id
        series_id = response.xpath('//*/div[@class="item-cont cur"]//*/p[@class="title"]/a/@data-series-id').extract()
        # 车系名字
        series_name = response.xpath('//*/div[@class="item-cont cur"]//*/p[@class="title"]/a/text()').extract()
        # 车系url
        series_url_list = self.get_series_url(response)
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
        item['app_id'] = '4'
        # 车型id
        vm_id = self.get_vm_id(response)
        # 车型名字
        vm_name = response.xpath('//*/div[@class="table_car_sells"]/div/div/div[1]/a/text()').extract()
        # 车型url
        vm_url_list = self.get_vm_url(response)
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
    def get_series_url(response):
        series_url_list = response.xpath('//*/div[@class="item-cont cur"]//*/p[@class="title"]/a/@href').extract()
        for i in range(len(series_url_list)):
            series_url_list[i] = 'http://product.auto.163.com'+series_url_list[i]
        return series_url_list

    @staticmethod
    def get_vm_id(response):
        vm_id = response.xpath('//*/div[@class="table_car_sells"]/div/div/div[1]/a/@href').extract()
        for i in range(len(vm_id)):
            vm_id[i] = vm_id[i].replace('/product/', '')
            vm_id[i] = vm_id[i].replace('.html#ncx00020', '')
        return vm_id

    @staticmethod
    def get_vm_url(response):
        vm_url_list = response.xpath('//*/div[@class="table_car_sells"]/div/div/div[1]/a/@href').extract()
        for i in range(len(vm_url_list)):
            vm_url_list[i] = 'http://product.auto.163.com'+vm_url_list[i]
        return vm_url_list
