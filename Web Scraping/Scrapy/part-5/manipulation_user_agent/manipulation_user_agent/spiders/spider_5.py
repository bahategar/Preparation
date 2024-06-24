import scrapy


class Spider5Spider(scrapy.Spider):
    name = "spider_5"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        pass
