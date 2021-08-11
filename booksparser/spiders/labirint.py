import scrapy
from scrapy.http import HtmlResponse

from booksparser.items import BooksparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page_link = response.xpath(
            "//div[contains(@class, 'pagination-next-mobile')]/a[@class='pagination-next__text']/@href").extract_first()
        if next_page_link:
            yield response.follow(next_page_link, self.parse)

        links = response.xpath("//div[@data-position]//a[@class='product-title-link']/@href").extract()
        for link in links:
            yield response.follow(link, self.parse_book)

    def parse_book(self, response: HtmlResponse):
        book_link = response.url
        book_name = response.xpath("//div[@id='product-info']/@data-name").extract_first()
        book_authors = response.xpath("//a[@data-event-label='author']/@data-event-content").extract()
        book_price = response.xpath("//div[@id='product-info']//@data-price").extract_first()
        book_discount_price = response.xpath("//div[@id='product-info']//@data-discount-price").extract_first()
        book_rate = response.xpath("//div[@id='rate']/text()").extract_first()
        # если книги нет в продаже data_available_status = 0
        data_available_status = response.xpath("//div[@id='product-info']/@data-available-status").extract_first()

        yield BooksparserItem(book_link=book_link, book_name=book_name, book_authors=book_authors,
                              book_price=book_price, book_discount_price=book_discount_price, book_rate=book_rate,
                              data_available_status=data_available_status)
