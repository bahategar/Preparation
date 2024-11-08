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
            "playwright":True,
            "playwright_include_page":True,
            # NOTES: The Page object from playwright that was used to download the request will be 
            #          available in the callback at response.meta['playwright_page']. 
            #          If False (or unset) the page will be closed immediately after processing the request.
            "playwright_page_methods":[PageMethod("wait_for_selector", selector='div.quote')],
            # NOTES: A list of PageMethod object ==> PageMethod is object for call method of Page object.
             #   documentation Page object: https://playwright.dev/python/docs/api/class-page
            }
        yield scrapy.Request(url, meta=config, errback=self.errback_close_page)
            # NOTES: When passing playwright_include_page=True, make sure pages are always closed when they are no longer used. 
            #          It's recommended to set a Request errback to make sure pages are closed even if a request fails 
            #          (if playwright_include_page=False pages are automatically closed upon encountering an exception).

    def parse(self, response):
        quoteItem = QuoteItem()

        quotes = response.xpath("//div[@class='quote']")
        if len(quotes) > 0:
            for quote in quotes:
                quoteItem['text'] = response.xpath(".//span[@class='text']/text()").get()
                quoteItem['author'] = response.xpath(".//small[@class='author']/text()").get()
                quoteItem['tags'] = response.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()
                yield quoteItem
        else:
            print("FAIL")

    async def errback_close_page(self, failure):
        # If error, callback this function to close the Page object.
        page = failure.request.meta("playwright_page")
        await page.close()