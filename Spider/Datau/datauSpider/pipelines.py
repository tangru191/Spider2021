# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class ScrapyuniversalPipeline(object):
    def process_item(self, item, spider):
        return item

class DatauSpiderPipleline(object):
    def process_item(self,item,spider):
        base_dir = os.getcwd()
        fiename = base_dir + '/imooc.txt'
        # 从内存以追加的方式打开文件，并写入对应的数据
        with open(fiename, 'a') as f:
            f.write(item['title'] + '|')
            f.write(item['url'] + '|')
            # f.write(item['text'] + '|')
            f.write(item['website']+'\n')
            return item