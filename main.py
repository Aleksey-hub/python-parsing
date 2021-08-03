# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru,
#    lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
#       название источника;
#       наименование новости;
#       ссылку на новость;
#       дата публикации.
# 2. Сложить собранные данные в БД
from pprint import pprint

import requests
from lxml import html

from pymongo import MongoClient

# 1.
url = 'https://news.mail.ru'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'
}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

links = dom.xpath("//div[contains(@class, 'daynews__item')]//@href|"
                  "//div[contains(@class, 'daynews ')]/following-sibling::ul/li[@class='list__item']//@href")
# pprint(links)

news = []
for link in links:
    response_ = requests.get(link, headers=headers)
    dom_ = html.fromstring(response_.text)

    source_name = dom_.xpath("//span[text()[contains(., 'источник')]]/following-sibling::a/span/text()")[0]
    title_news = dom_.xpath("//div[contains(@class, 'article')]//h1[@class='hdr__inner']/text()")[0]
    date_publication = dom_.xpath("//div[contains(@class, 'article')]//span[@datetime]/@datetime")[0]

    one_news = {
        'source_name': source_name,
        'title_news': title_news,
        'link': link,
        'date_publication': date_publication
    }
    news.append(one_news)

pprint(news)

# 2.
client = MongoClient('127.0.0.1', 27017)

db = client['news']

db.news.insert_many(news)