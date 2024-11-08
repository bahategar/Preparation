import scrapy
from ..items import QuoteItem
from scrapy_playwright.page import PageMethod

class SpiderSpider(scrapy.Spider):
    name = "spider"
    # allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com/"]

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js/'

        config = {
            "playwright": True,
            "playwright_include_page": True,
            "playwright_page_method": [
                PageMethod("wait_for_selector", selector="div.quote")
                ],
        }
        yield scrapy.Request(url, meta=config, errback=self.errback_close_page)

    async def parse(self, response):
        # Close the current Page object first (since we want to create new Page object that represent next page)
        page = response.meta.get("playwright_page")
        await page.close()

        quoteItem = QuoteItem()

        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            quoteItem['text'] = response.xpath(".//span[@class='text']/text()").get()
            quoteItem['author'] = response.xpath(".//small[@class='author']/text()").get()
            quoteItem['tags'] = response.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()
            yield quoteItem

        # Next page
        url = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        
        if url is not None:
            config = {
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_method": [
                    PageMethod("wait_for_selector", selector="div.quote")
                    ],
            }
            yield response.follow(url, meta=config, errback=self.errback_close_page)

    async def errback_close_page(self, failure):
        page = failure.request.meta("playwright_page")
        await page.close()
