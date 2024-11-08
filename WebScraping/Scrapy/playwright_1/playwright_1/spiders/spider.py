import scrapy
from ..items import QuoteItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    # allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com/"]


    def start_requests(self):
        url = 'https://quotes.toscrape.com/js/'
        yield scrapy.Request(url, meta={'playwright': True})

    def parse(self, response):
        quoteItem = QuoteItem()

        quotes = response.xpath("//div[@class='quote']")
        if len(quotes)> 0:
            for quote in quotes:
                quoteItem['text'] = response.xpath(".//span[@class='text']/text()").get()
                quoteItem['author'] = response.xpath(".//small[@class='author']/text()").get()
                quoteItem['tags'] = response.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()
                yield quoteItem
        else:
            print("FAIL")
