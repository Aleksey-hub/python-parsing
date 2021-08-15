'''
1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
● название;
● все фото;
● параметры товара в объявлении;
● ссылка;
● цена.

Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.
'''

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from goodsparser import settings
from goodsparser.spiders.leroymerlin import LeroymerlinSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider)

    process.start()
