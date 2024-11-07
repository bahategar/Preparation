import scrapy


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):

        bases = response.xpath("//article[@class='product_pod']")
        for base in bases:
            yield {
                'name': base.xpath(".//h3/a/@title").get() or base.xpath(".//h3//text()").get(),
                'price': base.xpath(".//p[@class='price_color']/text()").get(),
                'url': base.xpath(".//h3/a/@href").get(),
            }
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        # Using Absolure URL Approach
        if next_url is not None:
            if 'catalogue/' in next_url:
                next_url = 'https://books.toscrape.com/' + next_url
            else:
                next_url = 'https://books.toscrape.com/catalogue/' + next_url
            yield response.follow(next_url, callback=self.parse)

        # # Using Relative URL
        # yield response.follow(next_url, callback=self.parse)

