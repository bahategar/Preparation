import scrapy
import random
from proxy_api.items import BookItem
from urllib.parse import urlencode


class Part9Spider(scrapy.Spider):
    name = "part_9"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def start_requests(self):
        # If this function exist, scrapy will run this function.
        #  if it is not it will work of the link inside 'start_urls' variable
        yield scrapy.Request(url=book_url, callback=self.parse_book_page)

    def parse(self, response):
        books = response.xpath("//article[@class='product_pod']")

        for book in books:
            relative_url = book.xpath(".//h3//a/@href").get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
    
           yield scrapy.Request(url=next_page_url, callback=self.parse)
                
        next_page_url = response.xpath("//li[@class='next']/a/@href").get()

        if next_page_url is not None:
            if 'catalogue/' in next_page_url:
                next_page_url = 'https://books.toscrape.com/' + next_page_url
            else:
                next_page_url = 'https://books.toscrape.com/catalogue' + next_page_url
            
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        book_item = BookItem()

        book_item['url'] = response.url
        book_item['title'] = response.xpath("//div[contains(@class, 'product_main')]/h1/text()").get()
        book_item['stars'] = response.xpath("//div[contains(@class, 'product_main')]/p[contains(@class, 'star')]/@class").get()
        book_item['category'] = response.xpath("//ul/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['upc'] = response.xpath("(//table//td)[1]/text()").get()
        book_item['product_type'] = response.xpath("(//table//td)[2]/text()").get()
        book_item['price_excl_tax'] = response.xpath("(//table//td)[3]/text()").get()
        book_item['price_incl_tax'] = response.xpath("(//table//td)[4]/text()").get()
        book_item['tax'] = response.xpath("(//table//td)[5]/text()").get()
        book_item['availability'] = response.xpath("(//table//td)[6]/text()").get()
        book_item['num_reviews'] = response.xpath("(//table//td)[7]/text()").get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['price'] = response.xpath("//p[@class='price_color']/text()").get()

        yield book_item