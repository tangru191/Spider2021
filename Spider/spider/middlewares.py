# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import random
import sys
import time

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings

PY3 = sys.version_info[0] >= 3


class SpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class RandomUserAgentMiddlware(object):
#     def process_request(self, request, spider):
#         agent = random.choice(agents)
#         #print(agent)
#         request.headers["User-Agent"] = agent


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, settings, user_agent='Scrapy'):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent
        # 项目路径
        rootDir = os.path.split(os.path.realpath(__file__))[0]
        # config.ini文件路径
        configFilePath = os.path.join(rootDir, 'File/useragents.txt')
        # user_agent_list_file = settings.get('USER_AGENT_LIST')
        user_agent_list_file = configFilePath
        if not user_agent_list_file:
            # If USER_AGENT_LIST_FILE settings is not set,
            # Use the default USER_AGENT or whatever was
            # passed to the middleware.
            ua = settings.get('USER_AGENT', user_agent)
            self.user_agent_list = [ua]
        else:
            with open(user_agent_list_file, 'r') as f:
                self.user_agent_list = [line.strip() for line in f.readlines()]

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)


# def base64ify(bytes_or_str):
#     if PY3 and isinstance(bytes_or_str, str):
#         input_bytes = bytes_or_str.encode('utf8')
#     else:
#         input_bytes = bytes_or_str
#
#     output_bytes = base64.urlsafe_b64encode(input_bytes)
#     if PY3:
#         return output_bytes.decode('ascii')
#     else:
#         return output_bytes

# 此部分为使用亿牛云代理池的代理中间件
# class ProxyMiddleware(object):
#     def process_request(self, request, spider):
#         # 代理服务器
#         proxyHost = "n5.t.16yun.cn"
#         proxyPort = "6441"
#
#         # 代理隧道验证信息
#         proxyUser = "16OLRDEK"
#         proxyPass = "599909"

#         request.meta['proxy'] = "http://{0}:{1}".format(proxyHost, proxyPort)

#         # 添加验证头
#         encoded_user_pass = base64ify(proxyUser + ":" + proxyPass)
#         request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
#
#         # 设置IP切换头(根据需求)
#         tunnel = random.randint(1, 10000)
#         request.headers['Proxy-Tunnel'] = str(tunnel)


class ProxyMiddleware(object):
    """
    设置Proxy,一次请求随机切换一次ip
   """

    def __init__(self, ip):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        # 通过配置文件获取代理ip
        return cls(ip=crawler.settings.get('PROXIES'))

    def process_request(self, request, spider):
        # 随机切换ip
        ip = random.choice(self.ip)
        request.meta['proxy'] = ip


# class SeleniumMiddleware(object):
#     '''
#     本部分为集成seleunim可解决大部分通过js加载的网页，需要时可以启用
#     '''
#     def __init__(self):
#         self.browser = webdriver.Chrome()
#         # 以获取上一级父类基类的，__init__方法里的对象封装值
#         super(SeleniumMiddleware, self).__init__()
#         # 绑定信号量，当spider关闭时调用我们的函数
#         # dispatcher.connect()信号分发器，第一个参数信号触发函数，第二个参数是触发信号，signals.spider_closed是爬虫结束信号
#         dispatcher.connect(self.spider_closed, signals.spider_closed)
#
#     def process_request(self, request, spider):
#         # if spider.name == "jd":
#         if spider.name == 'imooc':
#             print ("Chrome is starting...")
#             driver = webdriver.Chrome() #指定使用的浏览器
#             driver.get(request.url)
#             time.sleep(1)
#             js = "var q=document.documentElement.scrollTop=10000"
#             driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
#             time.sleep(1)
#             body = driver.page_source
#             print ("访问"+request.url)
#             return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
#
#     def spider_closed(self, spider):
#         # 当爬虫请求结束以后发送结束爬虫信息，则打开的浏览器关闭
#         print('spider closed')
#         self.browser.quit()

class SeleniumMiddleware(object):
    '''
    本部分为集成seleunim可解决大部分通过js加载的网页，需要时可以启用
    '''

    def __init__(self):
        # 实例化一个启动参数对象
        chrome_options = Options()
        # 设置浏览器以无界面方式运行
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        # 以获取上一级父类基类的，__init__方法里的对象封装值
        super(SeleniumMiddleware, self).__init__()
        # 绑定信号量，当spider关闭时调用我们的函数
        # dispatcher.connect()信号分发器，第一个参数信号触发函数，第二个参数是触发信号，signals.spider_closed是爬虫结束信号
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_request(self, request, spider):
        # if spider.name == "jd":
        if spider.name == 'qqtext':
            print("Chrome is starting...")
            # 实例化一个启动参数对象
            chrome_options = Options()
            # 设置浏览器以无界面方式运行
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=chrome_options)  # 指定使用的浏览器
            driver.get(request.url)
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=1000000"
            driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(1)
            body = driver.page_source
            print("访问" + request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

    def spider_closed(self, spider):
        # 当爬虫请求结束以后发送结束爬虫信息，则打开的浏览器关闭
        print('spider closed')
        self.browser.quit()
