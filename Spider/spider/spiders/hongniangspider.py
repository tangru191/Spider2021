# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_redis.spiders import RedisCrawlSpider
import scrapy


class HongniangspiderSpider(RedisCrawlSpider):
    name = 'hongniangSpider'
    # allowed_domains = ['hongniang.com']
    # start_urls = ['http://www.hongniang.com/index/search?sort=0&wh=0&sex=2&starage=0&province=0&
    # city=0&marriage=0&edu=0&income=0&height=0&pro=0&house=0&child=0&xz=0&sx=0&mz=0&hometownprovince=0']
    redis_key = 'hongniang:start_urls'
    # 中国红娘index页面的分页
    # lpush hongniang:start_urls http://www.hongniang.com/index/search?sort=0&wh=0&sex=2&starage=0
    # &province=0&city=0&marriage=0&edu=0&income=0&height=0&pro=0&house=0&child=0&xz=0&sx=0&mz=0&hometownprovince=0
    page_lx = LinkExtractor(allow='index/search\?.*&page=\d+')
    # 个人详细的信息
    self_lx = LinkExtractor(allow='user/member/id/\d+')
    # 规则
    rules = (
        Rule(page_lx, follow=True),
        Rule(self_lx, callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        item = dict()
        # 用户名称
        item['nickname'] = self.get_nickname(response)
        # 用户id
        item['loveid'] = self.get_loveid(response)
        # 用户的照片
        item['photos'] = self.get_photos(response)
        # 用户年龄
        item['age'] = self.get_age(response)
        # 用户的身高
        item['height'] = self.get_height(response)
        # 用户是否已婚
        item['ismarried'] = self.get_ismarried(response)
        # # 用户年收入
        item['yearincome'] = self.get_yearincome(response)
        # # 用户的学历
        item['education'] = self.get_education(response)
        # # 用户的地址
        item['workaddress'] = self.get_workaddress(response)
        # 用户的内心独白
        item['soliloquy'] = self.get_soliloquy(response)
        # 用户的性别
        item['gender'] = self.get_gender(response)
        print(item)
        yield item

    @staticmethod
    def get_nickname(response):
        nickname = response.xpath('//div[@class="info1"]/div[@class="name nickname"]/text()').extract()[0]
        if len(nickname) > 0:
            nickname = nickname.strip()
        else:
            nickname = "NULL"
        return nickname

    @staticmethod
    def get_loveid(response):
        loveid = response.xpath('//div[@class="info1"]/div[@class="loveid"]/text()').extract()[0]
        if len(loveid) > 0:
            loveid = loveid.strip()
        else:
            loveid = "NULL"
        return loveid

    @staticmethod
    def get_photos(response):
        photos = response.xpath('//div[@id="tFocus-btn"]/ul/li/img/@src').extract()
        if len(photos) > 0:
            pass
        else:
            photos = "NULL"
        return photos

    @staticmethod
    def get_age(response):
        age = response.xpath('//div[@class="info2"]/div/ul/li/text()').extract()[0]
        if len(age) > 0:
            age = age.strip()
        else:
            age = "NULL"
        return age

    @staticmethod
    def get_height(response):
        height = response.xpath('//div[@class="info2"]/div/ul/li/text()').extract()[2]
        if len(height) > 0:
            height = height.strip()
        else:
            height = "NULL"
        return height

    @staticmethod
    def get_ismarried(response):
        ismarried = response.xpath('//div[@class="info2"]/div/ul/li/text()').extract()[1]
        if len(ismarried) > 0:
            ismarried = ismarried.strip()
        else:
            ismarried = "NULL"
        return ismarried

    @staticmethod
    def get_yearincome(response):
        yearincome = response.xpath('//div[@class="info2"]/div/ul/li/text()').extract()[4]
        if len(yearincome) > 0:
            yearincome = yearincome.strip()
        else:
            yearincome = "NULL"
        return yearincome

    @staticmethod
    def get_education(response):
        education = response.xpath('//div[@class="info2"]/div/ul/li/text()').extract()[3]
        if len(education) > 0:
            education = education.strip()
        else:
            education = "NULL"
        return education

    @staticmethod
    def get_workaddress(response):
        workaddress = response.xpath('//div[@class="info2"]/div/ul/li/text()').extract()[5]
        if len(workaddress) > 0:
            workaddress = workaddress.strip()
        else:
            workaddress = "NULL"
        return workaddress

    @staticmethod
    def get_soliloquy(response):
        soliloquy = response.xpath('//div[@class="info5"]/div[@class="text"]/text()').extract()[0]
        if len(soliloquy) > 0:
            soliloquy = soliloquy.strip()
        else:
            soliloquy = "NULL"
        return soliloquy

    @staticmethod
    def get_gender(response):
        return "女"
