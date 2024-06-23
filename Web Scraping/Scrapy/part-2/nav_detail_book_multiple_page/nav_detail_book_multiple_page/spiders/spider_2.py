import scrapy


class Spider2Spider(scrapy.Spider):
    name = "spider_2"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.xpath("//article[@class='product_pod']")

        for book in books:
            url_book_page = book.xpath(".//h3//a/@href").get()


            yield response.follow(url_book_page, callback=self.parse_book_page)
                
        next_page_url = response.xpath("//li[@class='next']/a/@href").get()
        # Using relative path
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        # title: //div[contains(@class, 'product_main')]/h1/text()
        # stars: //div[contains(@class, 'product_main')]/p[contains(@class, 'star')]/@class
        # Product-type: (//table//td)[2]/text()
        # price_excl_tax: (//table//td)[3]/text()
        # price_incl_tax: (//table//td)[4]/text()
        # tax: (//table//td)[5]/text()
        # availability: (//table//td)[6]/text()
        # num_reviews: (//table//td)[7]/text()
        # description: //div[@id='product_description']/following-sibling::p/text()
        # price: //p[@class='price_color']
        yield {
            'url': response.url,
            'title': response.xpath("//div[contains(@class, 'product_main')]/h1/text()").get(),
            'stars': response.xpath("//div[contains(@class, 'product_main')]/p[contains(@class, 'star')]/@class").get(),
            'product_type': response.xpath("(//table//td)[2]/text()").get(),
            'price_excl_tax': response.xpath("(//table//td)[3]/text()").get(),
            'price_incl_tax': response.xpath("(//table//td)[4]/text()").get(),
            'tax': response.xpath("(//table//td)[5]/text()").get(),
            'availability': response.xpath("(//table//td)[6]/text()").get(),
            'num_reviews': response.xpath("(//table//td)[7]/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': response.xpath("//p[@class='price_color']").get(),
        }

