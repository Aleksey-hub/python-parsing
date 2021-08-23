# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramParserItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    user_id_foll = scrapy.Field()
    user_name_foll = scrapy.Field()
    user_pic_link_foll = scrapy.Field()
    is_follower = scrapy.Field()
    is_following = scrapy.Field()
