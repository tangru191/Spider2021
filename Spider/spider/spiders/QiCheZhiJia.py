# -*- coding: utf-8 -*-
import scrapy
import re
import urllib
import json

from scrapy.spiders import CrawlSpider
from spider.Utils import TimeHelper, CarDBHelper


"""
author:tangru
date: 2018.12.10
function:汽车之间数据爬取
"""


class QiCheZhiJiaSpider(CrawlSpider):
    name = 'qichezhijia1.0'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    def parse(self, response):
        for brandPart in response.xpath('body/dl'):
            item = dict()
            """
            爬取品牌页的品牌id，品牌名，调用DataDBHelper.save方法插入数据库
            数据库中的表名为：datau_crawler_brand'
            TimeHelper.getTime：生成时间
            callback=self.series_page跳转到车系页进行爬取
            """
            item['app_id'] = "1"
            # # app的名字
            # item['app_name'] = "汽车之家"
            # table = 'datau_crawler_app'
            # item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            # item['update_time']=TimeHelper.TimeHelper.getTime(self=None)
            # print(item)
            # CarDBHelper.DataDBHelper.save(self=None,table=table,item=item)
            # yield item
            # 品牌id
            item['brand_id'] = brandPart.xpath('@id').extract()

            # 品牌url
            # item['brand_url'] = brandPart.xpath('dt/a/@href')[0].extract()
            # 品牌名字

            """品牌id"""
            item['brand_id'] = brandPart.xpath('@id')[0].extract()
            """品牌名"""
            item['brand_name'] = brandPart.xpath('dt/div/a/text()')[0].extract()
            """
            table = 'datau_crawler_brand'
            item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
            item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
            CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
            """

            series_url = brandPart.xpath('dd/ul/li/h4/a/@href').extract()
            for i in series_url:
                series_url_one = " https: " + i

                yield scrapy.Request(series_url_one, meta={'item': item}, dont_filter=True,
                                     callback=self.series_page)

            """
            开始爬取车系页
            response.meta方法:获取上层方法中获得的item爬取
            series_name,
            series_url,
            brand_id等数据
            并插入到车系表中
            """
    def series_page(self, response):
        itemseries = response.meta['item']
        app_id = itemseries['app_id']
        brand_id = itemseries['brand_id']
        item = dict()
        item['app_id'] = app_id

        item['series_url'] = response.url

        series_name = response.xpath('//*[@class="athm-sub-nav__car__name"]/a/h1/text()').extract()
        if len(series_name) > 0:
            item['series_name'] = series_name[0]
        else:
            item['series_name'] = response.xpath('//*[@class="subnav-title-name"]/a/text()').extract()[0]

        item['series_url'] = response.url.replace("www", "m")
        """品牌id"""
        item["brand_id"] = brand_id
        """item["brand_id"] = self.get_brand_id(response)"""
        """车系id"""
        item["series_id"] = self.get_series_id(response)
        """厂商指导价min"""
        item["guide_price_min"] = self.get_guide_price_min(response)
        """厂商指导价max"""
        item["guide_price_max"] = self.get_guide_price_max(response)
        """二手车价格min(动态)"""
        item["used_car_price_min"] = self.get_used_car_price_min(response)
        """二手车价格max（动态）"""
        item["used_car_price_max"] = self.get_used_car_price_max(response)
        """用户评分"""
        item["user_score"] = self.get_user_score(response)
        """口碑数量"""
        item["evaluate_count"] = self.get_evaluate_count(response)
        """保值率"""
        item["hedge_ratio"] = self.get_hedge_ratio(response)
        """
        #向车系表插入爬取数据
        # table = 'datau_crawler_carseries'
        # item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
        # item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
        # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
        """
        yield item
        chexing_url = response.xpath('//*[@class="information-price"]/dd[1]/a[2]/@href').extract()
        for chexingurl in chexing_url:
            request_chexing_url = "https://www.autohome.com.cn" + chexingurl
            yield scrapy.Request(request_chexing_url, meta={'item': item}, dont_filter=True, callback=self.chexing_page)
    """
    车型url爬取
    爬取vm_name，vm_url,attention 等车型页的数据
    并插入到车型表中
    从车系页获取app_id
    """
    def chexing_page(self, response):

        itemchexing = response.meta['item']
        app_id = itemchexing['app_id']
        item = dict()
        item['app_id'] = app_id
        # 车型名称
        vm_name = self.get_vm_name(response)
        # 关注度
        attention = self.get_attention(response)
        # 车系id
        series_id = self.get_series_id_chexing(response)
        # 指导价
        guide_price = self.get_guide_price(response)
        # 经销商参考价
        # dealer_reference_price = self.get_dealer_reference_price(response)
        # 车型id
        vm_id = self.get_vm_id(response)
        # 车型url
        vm_url = self.get_vm_url(response)
        # 性能(待优化)
        performance = self.get_performance(response)
        # 车的类型
        car_type = self.get_car_type(response)
        # 评价评分
        item["evaluate_score"] = "待完善"
        # 百公里耗油
        item["consumption"] = "待完善"
        if vm_name is not None:
            for i in range(len(vm_name)):
                item["series_id"] = series_id
                item["car_type"] = car_type
                item['vm_name'] = vm_name[i]
                item['attention'] = attention[i]
                item['guide_price'] = guide_price[i]
                item['dealer_reference_price'] = "待爬取"
                item['vm_id'] = vm_id[i]
                item['vm_url'] = vm_url[i]
                item['performance'] = performance[i]
                item["evaluate_score"] = "待完善"
                item["consumption"] = "待完善"
                # 向数据库车型表插入数据
                # table = 'datau_crawler_vehiclemodel'
                # item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
                # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
                yield item
        """
        #进行口碑页的爬取
        # vm_url_a= response.xpath('//*[@class="related-link"]/a[1]/@href').extract()
        # for vm_url_b in vm_url_a:
        #     vm_url_c = "https:" + vm_url_b
        #     # print("-----口碑页url开始------------------------")
        #     # print(vm_url_c)
        #     yield scrapy.Request(vm_url_c,meta={'item': item},dont_filter=True,callback=self.koubei_page)
        """
    """品牌id获取方法,brand_id_one为列表格式"""
    @staticmethod
    def get_brand_id(response):
        brand_id_one = response.xpath('//*[@id="auto-brand-vr"]/iframe/@data-brandid').extract()
        brand_id = (" ".join(brand_id_one))
        if len(brand_id) > 0:
            brand_id = brand_id
        else:
            brand_id = "wei"
        return brand_id

    """获取车系id"""
    @staticmethod
    def get_series_id(response):
        brand_url_one = response.xpath('//*[@http-equiv="mobile-agent"]/@content').extract()
        series_id_one = []
        for brand_url_a in brand_url_one:
            guide_price_b = brand_url_a.strip()
            guide_price_c = re.sub("\D", "", str(guide_price_b))
            series_id_one.append(guide_price_c)
        series_id = series_id_one[1]
        if len(series_id) > 0:
            series_id = series_id
        else:
            series_id = ""
        return series_id

    @staticmethod
    def get_guide_price_min(response):
        get_guide_pricea = response.xpath('//*[@class="information-price"]/dd[1]/a[1]/text()').extract()
        # 提取数字
        get_guide_pricea_min_one = re.findall(r"\d+\.?\d*", str(get_guide_pricea))
        # 判断提取的数字个数
        lendrpo = len(get_guide_pricea_min_one)
        if lendrpo == 2:
            guide_price_min = get_guide_pricea_min_one[0]
        elif lendrpo == 1:
            guide_price_min = "暂无"
        else:
            guide_price_min = "暂无"
        return guide_price_min

    # 厂商指导价max
    @staticmethod
    def get_guide_price_max(response):
        get_guide_pricea = response.xpath('//*[@class="information-price"]/dd[1]/a[1]/text()').extract()
        # 提取数字
        get_guide_pricea_max_one = re.findall(r"\d+\.?\d*", str(get_guide_pricea))
        # 判断提取的数字个数
        lendrpo = len(get_guide_pricea_max_one)
        if lendrpo == 2:
            guide_price_max = get_guide_pricea_max_one[1]
        elif lendrpo == 1:
            guide_price_max = get_guide_pricea_max_one[0]
        else:
            guide_price_max = "暂无"
        return guide_price_max

    """二手车价格min"""
    @staticmethod
    def get_used_car_price_min(response):
        brand_url_one = response.xpath('//*[@http-equiv="mobile-agent"]/@content').extract()
        series_id_one = []
        for brand_url_a in brand_url_one:
            guide_price_b = brand_url_a.strip()
            guide_price_c = re.sub("\D", "", str(guide_price_b))
            series_id_one.append(guide_price_c)
        series_id = series_id_one[1]
        # 通过urllib模块中的urlopen的方法打开url
        priceminhtml = urllib.request.urlopen(
            'https://api.che168.com/auto/ForAutoCarPCInterval.ashx?callback=che168CallBack''&_appid=cms&sid='
            + str(series_id) + '&yid=0&pid=110000&cid=110100')
        # 通过read方法获取返回数据
        priceminhtmlone = priceminhtml.read()
        priceminhtmltwo = str(priceminhtmlone).replace('(', '').replace(')', '').\
            replace('che168CallBack', '').replace('b', '').replace('\'', '').replace('\\', '')
        # 将返回的json格式的数据转化为python对象，json数据转化成了python中的字典，按照字典方法读取数据
        priceminhtmlt = json.loads(priceminhtmltwo)
        if len(priceminhtmlt['message']) > 0:
            used_car_price_min = "暂无"
        else:
            used_car_price_min = priceminhtmlt['result']['minPrice']
        return used_car_price_min

    # 二手车价格max（待优化）
    @staticmethod
    def get_used_car_price_max(response):
        brand_url_one = response.xpath('//*[@http-equiv="mobile-agent"]/@content').extract()
        series_id_one = []
        for brand_url_a in brand_url_one:
            guide_price_b = brand_url_a.strip()
            guide_price_c = re.sub("\D", "", str(guide_price_b))
            series_id_one.append(guide_price_c)
        series_id = series_id_one[1]
        # 通过urllib模块中的urlopen的方法打开url
        pricemaxhtml = urllib.request.urlopen(
            'https://api.che168.com/auto/ForAutoCarPCInterval.ashx?callback=che168CallBack&_appid=cms&sid=' + str(
                series_id) + '&yid=0&pid=110000&cid=110100')
        # 通过read方法获取返回数据
        pricemaxhtmlone = pricemaxhtml.read()
        pricemaxhtmltwo = str(pricemaxhtmlone).replace('(', '').replace(')', '').\
            replace('che168CallBack', '').replace('b', '').replace('\'', '').replace('\\', '')
        # 将返回的json格式的数据转化为python对象，json数据转化成了python中的字典，按照字典方法读取数据
        pricemaxweb = json.loads(pricemaxhtmltwo)
        if len(pricemaxweb['message']) > 0:
            used_car_price_max = "暂无"
        else:
            used_car_price_max = pricemaxweb['result']['maxPrice']
        return used_car_price_max

    """用户评分"""
    @staticmethod
    def get_user_score(response):
        user_score = response.xpath('//*[@class="koubei-data"]/dd/a[1]/em/text()').extract()
        if len(user_score) > 0:
            user_score = user_score[0]
        else:
            user_score = ""
        return user_score.strip()

    # 口碑数量
    @staticmethod
    def get_evaluate_count(response):
        evaluate_count_one = response.xpath('//*[@class="koubei-data"]/dd/a[2]/text()').extract()
        evaluate_count_two = re.sub("\D", "", str(evaluate_count_one))
        evaluate_count = evaluate_count_two
        if len(evaluate_count) > 0:
            evaluate_count = evaluate_count[0]
        else:
            evaluate_count = ""
        return evaluate_count.strip()

    # 保值率（待优化）
    @staticmethod
    def get_hedge_ratio(response):
        brand_url_one = response.xpath('//*[@http-equiv="mobile-agent"]/@content').extract()
        series_id_one = []
        for brand_url_a in brand_url_one:
            guide_price_b = brand_url_a.strip()
            guide_price_c = re.sub("\D", "", str(guide_price_b))
            series_id_one.append(guide_price_c)
        series_id = series_id_one[1]

        """通过urllib模块中的urlopen的方法打开url"""
        ratehtml = urllib.request.urlopen(
            'https://pinguapi.che168.com/v1/auto/keeprateofsid.ashx?callback=keepvalueCallBack&_appid=cms&seriesid='
            + str(series_id))
        ratehtmlone = ratehtml.read()
        ratehtmltwo = str(ratehtmlone).replace('(', '').replace(')', '').\
            replace('keepvalueCallBack', '').replace('b', '').replace(
            '\'', '')
        """将返回的json格式的数据转化为python对象，json数据转化成了python中的字典，按照字典方法读取数据"""
        rateweb = json.loads(ratehtmltwo)
        if rateweb.__contains__('result'):
            hedge_ratio = (rateweb['result']['rate'])
        else:
            hedge_ratio = "暂无"
        return hedge_ratio

    """车系id"""
    @staticmethod
    def get_series_id_chexing(response):
        brand_url_one = response.xpath('//*[@http-equiv="mobile-agent"]/@content').extract()
        series_id_one = []
        for brand_url_a in brand_url_one:
            guide_price_b = brand_url_a.strip()
            guide_price_c = re.sub("\D", "", str(guide_price_b))
            series_id_one.append(guide_price_c)
        series_id = series_id_one[0]
        if len(series_id) > 0:
            series_id = series_id
        else:
            series_id = ""
        return series_id

    """车型名称"""
    @staticmethod
    def get_vm_name(response):
        vm_name = response.xpath('//*[@class="interval01-list-cars"]/div/p[1]/a/text()').extract()
        return vm_name

    """关注度"""
    @staticmethod
    def get_attention(response):
        attention_one = response.xpath('//*[@class="attention-value"]/@style').extract()
        # 提取**.**%的数字
        attention = re.findall(r"\d+\.?\d*%", str(attention_one))
        return attention

    """指导价"""
    @staticmethod
    def get_guide_price(response):
        gp = []
        guide = response.xpath('//*[@class="interval01-list-guidance"]/div/text()').extract()
        guide_price = []
        guide_one = response.xpath('//*[@class="interval01-list-guidance"]/div/span/text()').extract()
        for a in guide_one:
            aa = (" ".join(a))
            gp.append(aa)
        for nicknamea in guide:
            nicknameb = nicknamea.strip()
            dealer_reference_price_one = re.findall(r"\d+\.?\d*", str(nicknameb))
            guide_price.append(dealer_reference_price_one)
        while [] in guide_price:
            guide_price.remove([])
        for i in guide_price:
            bb = (" ".join(i))
            gp.append(bb)
        guide_price = (" ".join(gp))
        return guide_price

    # 经销商参考价
    @staticmethod
    def get_dealer_reference_price(response):
        guide_pricee = []
        guidee = response.xpath('//*[@class="interval01-list-lowest"]/div/a[1]/text()').extract()
        for nicknameaa in guidee:
            nicknamebb = nicknameaa.strip()
            dealer_reference_price_onee = re.findall(r"\d+\.?\d*", str(nicknamebb))
            guide_pricee.append(dealer_reference_price_onee)
        while [] in guide_pricee:
            guide_pricee.remove([])
        guide_price = guide_pricee
        return guide_price

    """车型页车型id"""
    @staticmethod
    def get_vm_id(response):
        vm_id_one = response.xpath('//*[@class="interval01-list-cars"]/div/p[1]/a/@href').extract()
        vm_id = []
        for vm_id_a in vm_id_one:
            vm_id_b = re.findall(r"/\d*/", str(vm_id_a))
            vm_id_c = re.sub("\D", "", str(vm_id_b))
            vm_id.append(vm_id_c)
        return vm_id

    # 车型url
    @staticmethod
    def get_vm_url(response):
        vm_url_one = response.xpath('//*[@class="interval01-list"]/li/div/div/p[1]/a/@href').extract()
        vm_url = []
        for url_one in vm_url_one:
            url_two = "https://m.autohome.com.cn" + url_one
            vm_url.append(url_two)
        return vm_url

    # 性能(发动机)
    @staticmethod
    def get_performance(response):

        vm_name = response.xpath('//*[@class="interval01-list-cars"]/div/p[1]/a/text()').extract()
        performance_one = response.xpath('//*[@class="tab-content"]/div[3]/div/ul/li/div/div/p[3]/span[1]/text()').\
            extract()
        performance = []
        for i in range(0, len(vm_name)-len(performance_one)):
            performance.append("暂无")
        for i in performance_one:
            performance.append(i)
        return performance

    # 车型名称
    @staticmethod
    def get_car_type(response):
        car_type = response.xpath('//*[@class="breadnav fn-left"]/a[2]/text()').extract()
        car_type = (" ".join(car_type))
        return car_type
    """
    # 口碑页的方法
    # 爬取口碑=页
    def koubei_page(self, response):

        itemkoubei = response.meta['item']
        app_id = itemkoubei['app_id']
        item = dict()
        item['app_id'] = app_id
        # 车型id
        item["vm_id"] = self.get_vm_id_koubei(response)
        # 用户ID
        user_id = self.get_user_id(response)
        # 用户昵称
        user_nickname = self.get_user_nickname(response)
        # 裸车购买价
        buy_price = self.get_buy_price(response)
        # 购车地点
        address = self.get_address(response)
        # 发表时间
        publish_date = self.get_publish_date(response)
        # 评论标题
        title = self.get_title(response)
        # 评论内容
        content = self.get_content(response)
        # 经销商
        # dealer= self.get_dealer(response)
        if user_id is not None:
            for i in range(len(user_id)):
                item['user_id'] = user_id[i]
                item['user_nickname'] = user_nickname[i]
                item['buy_price'] = buy_price[i]
                item['address'] = address[i]
                item['publish_date'] = publish_date[i]
                item['title'] = title[i]
                item['content'] = content[i]
                item['dealer'] = "带爬取"
                print("口碑页item")
                print(item)
                yield item
        table = 'datau_crawler_evaluate'
        item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
        item['update_time'] = TimeHelper.TimeHelper.getTime(self=None)
        # CarDBHelper.DataDBHelper.save(self=None, table=table, item=item)
        yield item
    """
    """
    # 车型id
    def get_vm_id_koubei(self, response):
        vm_id_one = response.xpath('//*[@http-equiv="mobile-agent"]/@content').extract()
        # print(vm_id_one[1])
        # vm_id = dict()
        for vm_id_a in vm_id_one:
            vm_id_b = vm_id_a.strip()
            vm_id_c = re.sub("\D", "", str(vm_id_b))
            vm_id_one.append(vm_id_c)
        # print("---口碑车型id---")
        vm_id = vm_id_one
        if len(vm_id) > 0:
            vm_id = vm_id
        else:
            vm_id = ""
        return vm_id
        """


"""
    # 用户ID
    def get_user_id(self, response):
        user_id = response.xpath('//*[@class="name-text"]/p/a/@id').extract()
        user_id = (" ".join(user_id))
        return user_id

    # 用户昵称
    def get_user_nickname(self, response):
        nickname = response.xpath('//*[@class="name-text"]/p/a/text()').extract()
        # 去除/r/n空格
        user_nickname = []
        for nicknamea in nickname:
            nicknameb = nicknamea.strip()
            user_nickname.append(nicknameb)
        user_nickname = (" ".join(user_nickname))
        return user_nickname

    # 裸车购买价
    def get_buy_price(self, response):
        buy_price_one = response.xpath('//*[@class="choose-con mt-10"]/dl[5]/dd/text()').extract()
        buy_price = []
        for buy_price_c in buy_price_one:
            buy_price_d = buy_price_c.strip()
            buy_price_e = re.findall(r"\d+\.?\d*", str(buy_price_d))
            buy_price.append(buy_price_e)
        # print(guide_price)
        while [] in buy_price:
            buy_price.remove([])
        # buy_price = response.xpath('//*[@class="choose-con mt-10"]/dl[5]/dd/text()').extract()
        buy_price = (" ".join(buy_price))
        # print("-----口碑页裸车购买价-------")
        # print(type(buy_price))
        # print(buy_price)
        return buy_price

    # # 购车地点
    def get_address(self, response):
        address_one = response.xpath('//*[@class="choose-con mt-10"]/dl[2]/dd/text()').extract()
        address = []
        for address_two in address_one:
            address_s = address_two.strip()
            address.append(address_s)
            address = [i for i in address if i != '']

        address = (" ".join(address))
        # print("------------购车地址--------------")
        # print(type(address))
        # print(address)
        return address

    # # 发表时间
    def get_publish_date(self, response):
        publish = response.xpath('//*[@class="title-name name-width-01"]/b/a/text()').extract()
        publish_date = []
        for publishone in publish:
            publishtwo = time.strptime(publishone, "%Y-%m-%d")
            # 转换为时间戳:
            timestamp = int(time.mktime(publishtwo))
            # print(timeStamp)
            publish_date.append(timestamp)
        publish_date = (" ".join(publish_date))
        # print("-------口碑页发表时间------")
        # print(type(publish_date))
        # print(publish_date)
        # if len(publish_date) > 0:
        #     publish_date = publish_date[0]
        # else:
        #     publish_date = ""
        return publish_date

    # # 评论标题
    def get_title(self, response):
        title = response.xpath('//*[@class="title-name name-width-01"]/a/text()').extract()
        title = (" ".join(title))
        # print("--------口碑页评论标题------------")
        # print(type(title))
        # print(title)
        return title

    # # 评论内容
    def get_content(self, response):
        content = response.xpath('//*[@class="text-con "]/div/text()').extract()
        # print("_______口碑页评论内容________")

        content = (" ".join(content))
        # print(type(content))
        return content

    # 经销商()(待优化)
    def get_dealer(self, response):
        # 另一个xpath//*[@class="mouthcon"]/div[1]/div[1]/div[2]/dl[3]/dd/a/text()
        dealer = response.xpath('//*[@class="choose-con mt-10"]/dl[3]/dd/a/text()').extract()
        # print(dealer)
        # if len(dealer) > 0:
        #     dealer = dealer[0]
        # else:
        #     dealer = ""
        return dealer
        """
