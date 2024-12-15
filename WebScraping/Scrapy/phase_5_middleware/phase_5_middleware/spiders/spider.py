import scrapy
from phase_5_middleware.items import BookItem

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

    def parse_info_book(self, response):        

        book_item = BookItem()

        book_item['url'] = response.url
        book_item['title'] = response.xpath("//div[contains(@class, 'product')]/h1/text()").get()
        book_item['upc'] = response.xpath("//table//tr[1]/td/text()").get()
        book_item['product_type'] = response.xpath("//table//tr[2]/td/text()").get()
        book_item['price_excl_tax'] = response.xpath("//table//tr[3]/td/text()").get()
        book_item['price_incl_tax'] = response.xpath("//table//tr[4]/td/text()").get()
        book_item['tax'] = response.xpath("//table//tr[5]/td/text()").get()
        book_item['availability'] = response.xpath("//table//tr[6]/td/text()").get()
        book_item['num_reviews'] = response.xpath("//table//tr[7]/td/text()").get()
        book_item['stars'] = response.xpath("//div[contains(@class, 'product')]/p[contains(@class, 'star')]/@class").get()
        book_item['category'] = response.xpath("//ul/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::*[1]/text()").get()
        book_item['price'] = response.xpath("//div[contains(@class, 'product')]/p[contains(@class, 'price')]/text()").get()

        yield book_item
