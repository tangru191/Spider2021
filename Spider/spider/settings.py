# -*- coding: utf-8 -*-

# Scrapy settings for spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# 使用的是scrapy-redis的去重组件，不使用scrapy默认的去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用的是scrapy-redis的调度器组件，不使用scrapy默认的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 允许暂停操作，redis请求记录不会清空
# SCHEDULER_PERSIST = True

# 下面三个是scrapy-redis的三种请求方式
# 默认的scrapy-redis请求队列形式
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# 队列形式，请求先进先出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# 栈的形式，请求先进后出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_TIMEOUT = 300
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25  # 250 ms of delay
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'User-Agent': '',
# 'Referer': 'https://movie.douban.com/top250'
#  }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'spider.middlewares.SpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'spider.middlewares.SpiderDownloaderMiddleware': 543,
    # 'spider.middlewares.ProxyMiddleware': 543,
    # 'spider.middlewares.ProxyMiddleware': 100,
    # 'spider.middlewares.ProxyMiddleware': 100,
    # 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'spider.middlewares.RandomUserAgentMiddleware': 400,
    # 'spider.middlewares.SeleniumMiddleware': None, #键为中间件类的路径，值为中间件的顺序
    'spider.middlewares.SeleniumMiddleware': 100 #键为中间件类的路径，值为中间件的顺序
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'spider.pipelines.SpiderPipeline': 500,
    'scrapy_redis.pipelines.RedisPipeline': 400,
    'spider.pipelines.QiCheZhiJiaPipeline': 350,
    'spider.pipelines.KafkaProducerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False
# 数据库配置###########################################################################################
# REDIS数据库配置#########################################################################
REDIS_HOST = "10.199.10.2"
# REDIS_HOST = "192.168.163.128"
# 指定数据库的端口号
REDIS_PORT = 6379
REDIS_PARAMS = {
    'db': 1,
    'password': "dy1479",
}
# REDIS_PASSWD = 123456
# REDIS_DB = 3

'''kafka相关配置'''
KAFAKA_HOST = "10.199.10.2"
KAFAKA_PORT = 6667
KAFAKA_TOPIC = "data201901031"
KAFKA_KEY = "spiders"
GROUP_ID = "201901031"

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

"""MYSQL数据库配置 这里是标签验证系统的数据库配置（为了将爬虫数据同步标签验证系统数据库"""
MYSQL_HOST = '10.199.10.5'
MYSQL_DBNAME = 'TagVerification'
MYSQL_USER = 'dytag_test'
MYSQL_PASSWD = 'Dytag@test11'
MYSQL_PORT = 3306

# 添加mongodb的配置
# MONGODB 主机名
MONGODB_HOST = "10.199.10.2"
# MONGODB 端口号
MONGODB_PORT = 27017
# 数据库名称
MONGODB_DBNAME = "qichezhijia"
# 存放数据的表名称
MONGODB_SHEETNAME = "qichezhijia001"
"""数据库配置结束"""
DOWNLOAD_FAIL_ON_DATALOSS = False
# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
"""
解决爬虫空跑的设置
"""
# redis 空跑时间 秒
# IDLE_TIME= 60
# # 同时扩展里面加入这个
# EXTENSIONS = {
#     'spider.scrapy_redis_extension.RedisSpiderClosedExensions': 500,
# }
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    'spider.Utils.exensions.RedisSpiderSmartIdleClosedExensions': 500,
}
MYEXT_ENABLED = True  # 开启扩展
IDLE_NUMBER = 20  # 配置空闲持续时间单位为20个 ，一个时间单位为5s
# 代理池
# PROXIES = ['http://183.207.95.27:80', 'http://111.6.100.99:80', 'http://122.72.99.103:80',
#            'http://106.46.132.2:80', 'http://112.16.4.99:81', 'http://123.58.166.113:9000',
#            'http://118.178.124.33:3128', 'http://116.62.11.138:3128', 'http://121.42.176.133:3128',
#            'http://111.13.2.131:80', 'http://111.13.7.117:80', 'http://121.248.112.20:3128',
#            'http://112.5.56.108:3128', 'http://42.51.26.79:3128', 'http://183.232.65.201:3128',
#            'http://118.190.14.150:3128', 'http://123.57.221.41:3128', 'http://183.232.65.203:3128',
#            'http://166.111.77.32:3128', 'http://42.202.130.246:3128', 'http://122.228.25.97:8101',
#            'http://61.136.163.245:3128', 'http://121.40.23.227:3128', 'http://123.96.6.216:808',
#            'http://59.61.72.202:8080', 'http://114.141.166.242:80', 'http://61.136.163.246:3128',
#            'http://60.31.239.166:3128', 'http://114.55.31.115:3128', 'http://202.85.213.220:3128']
