import scrapy
from ..items import QuoteItem
from scrapy_playwright.page import PageMethod


class SpiderSpider(scrapy.Spider):
    name = "spider"
    # allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com"]

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js'

        config = {
            "playwright": True,
            "playwright_include_page": True,
            "playwright_page_method": [
                PageMethod("wait_for_selector", selector="div.quote"),
            ]
        }

        yield scrapy.Request(url, meta=config, errback=self.errback_close_page)

    async def parse(self, response):
        # Get the page object
        page = response.meta.get('playwright_page')
        # Take the screenshot
        screenshot = await page.screenshot(path='example.png', full_page=True)
        # Close the page object
        await page.close()

    async def errback_close_page(self, failure):
        page = failure.request.meta.get("playwright_page")
        await page.close()