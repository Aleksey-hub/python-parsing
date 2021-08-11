'''
1) Создать двух пауков по сбору данных о книгах с сайта labirint.ru и/или book24.ru (book24 по желанию)
2) Каждый паук должен собирать:
* Ссылку на книгу
* Наименование книги
* Автор(ы)
* Основную цену
* Цену со скидкой
* Рейтинг книги
3) Собранная информация дожна складываться в базу данных
'''

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from booksparser import settings
from booksparser.spiders.labirint import LabirintSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider)

    process.start()
