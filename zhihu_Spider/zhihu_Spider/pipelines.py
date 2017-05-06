# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ZhihuSpiderPipeline(object):
    collection_name='user'
    def open_spider(self,spider):
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client['python']

    def close_spider(self,spider):
        self.client.close()






    def process_item(self, item, spider):
        self.db[self.collection_name].update({'url_token': item['url_token']}, {'$set': dict(item)}, True)
        return item
