import scrapy


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):

        bases = response.xpath("//article[@class='product_pod']")
        for base in bases:
            url_base = base.xpath("./h3/a/@href").get()
            yield response.follow(url_base, callback=self.parse_info_book)


        next_url = response.xpath("//li[@class='next']/a/@href").get()
        # Using relative url
        yield response.follow(next_url, callback=self.parse)
        # Using absolute url
        # if next_url is not None:
        #     if 'catalogue/' in next_url:
        #         next_url = 'https://books.toscrape.com/' + next_url
        #     else:
        #         next_url = 'https://books.toscrape.com/catalogue/' + next_url
        #     yield response.follow(next_url, callback=self.parse)

    def parse_info_book(self, response):
        yield {
            'url': response.url,
            'title': response.xpath("//div[contains(@class, 'product')]/h1/text()").get(),
            'product_type': response.xpath("//table//tr[2]/td"),
            'price_excl_tax': response.xpath("//table//tr[3]/td"),
            'price_incl_tax': response.xpath("//table//tr[4]/td"),
            'tax': response.xpath("//table//tr[5]/td"),
            'availability': response.xpath("//table//tr[6]/td"),
            'num_reviews': response.xpath("//table//tr[7]/td"),
            'stars': response.xpath("//div[contains(@class, 'product')]/p[contains(@class, 'star')]/@class").get(),
            'category': response.xpath("//ul/li[@class='active']/preceding-sibling::li[1]/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::*[1]/text()").get(),
            'price': response.xpath("//div[contains(@class, 'product')]/p[contains(@class, 'price')]/text()").get(),
        }
