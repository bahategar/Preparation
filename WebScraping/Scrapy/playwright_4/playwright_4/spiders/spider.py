import scrapy
from ..items import QuoteItem
from scrapy_playwright.page import PageMethod

class SpiderSpider(scrapy.Spider):
    name = "spider"
    # allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com/"]

    def start_requests(self):
        url = 'https://quotes.toscrape.com/scroll'

        config = {
            "playwright": True,
            "playwright_include_page": True,
            "playwright_page_method": [
                PageMethod("wait_for_selector", selector="div.quote"),
                # PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                # PageMethod("wait_for_selector", selector="div.quote:nth-child(11)")
                ],
        }
        yield scrapy.Request(url, meta=config, errback=self.errback_close_page)


    async def parse(self, response):
        # Get the current page object
        page = response.meta.get("playwright_page")
        quoteItem = QuoteItem()

        # await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        # await page.wait_for_selector(f"div.quote:nth-child(11)")
        
        # Scroll down 10 times
        for i in range(10):
            # Scroll down and wait for new quotes to load
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_selector(f"div.quote:nth-child({10 * (i + 1)})")

        # Re-download / update the page content inside the response
        html = await page.content()
        response = scrapy.Selector(text=html)
        # NOTE: The response is "feedback" from our previous request. 
        # Close the current Page object
        await page.close()

        # Extract quotes after all scrolling is done
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            quoteItem['text'] = quote.xpath(".//span[@class='text']/text()").get()
            quoteItem['author'] = quote.xpath(".//small[@class='author']/text()").get()
            quoteItem['tags'] = quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()
            yield quoteItem



    async def errback_close_page(self, failure):
        page = failure.request.meta.get("playwright_page")
        await page.close()

