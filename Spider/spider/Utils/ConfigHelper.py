# -*- coding:utf-8 -*-
import os
import configparser

"""
#@Time:2018
#@Author:tangru
本部分为读取配置文件的工具，为爬虫模块化部分的配置文件读取
"""
# 项目路径
rootDir = os.path.split(os.path.realpath(__file__))[0]
# config.ini文件路径
configFilePath = os.path.join(rootDir, 'ConfigData\config.ini')


def get_config_values(key, value):
    """
    根据传入的key获取对应的value
    :param key: ini配置文件中用[]标识的内容
    :param value: 配置文件中key对应的值
    :return:
    """
    config = configparser.ConfigParser()
    config.read(configFilePath)
    # return config.items(section=section)
    return config.get(section=key, option=value)