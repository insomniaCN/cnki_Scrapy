# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.exceptions import DropItem

#pipeline控制，对爬取目标进一步处理
class dropPipeline(object):
    #对没有包含author的item进行丢弃处理
    def process_item(self, item, spider):
        if item['author']:
            return item
        else:
            raise DropItem("Missing author in %s" % item)

#爬取的item保存为json格式    
class CnkispiderPipeline(object):
    def __init__(self):  
        self.file = codecs.open('data_information.json', 'wb', encoding='utf-8')  

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        #print line
        self.file.write(line.decode('unicode_escape'))
        return item

