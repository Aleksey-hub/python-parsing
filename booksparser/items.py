# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksparserItem(scrapy.Item):
    _id = scrapy.Field()
    book_link = scrapy.Field()
    book_name = scrapy.Field()
    book_authors = scrapy.Field()
    book_price = scrapy.Field()
    book_discount_price = scrapy.Field()
    book_rate = scrapy.Field()
    data_available_status = scrapy.Field()
