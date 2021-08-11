# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BooksparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_db = client['books']

    def process_item(self, item, spider):
        item['book_price'] = float(item['book_price'])
        item['book_discount_price'] = float(item['book_discount_price'])
        item['book_rate'] = float(item['book_rate'])

        collection = self.mongo_db[spider.name]
        collection.insert_one(item)

        return item
