import scrapy
from manipulation_user_agent.items import BookItem
import random

USER_AGENT_LIST = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
]

class Spider5Spider(scrapy.Spider):
    name = "spider_5"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        'FEEDS': {
            'booksdata.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4
            }
        }
    }

    def parse(self, response):
        print("################# SELECTED USER AGENT ##########################")
        print(response.request.headers.get('User-Agent').decode('utf-8'))

        books = response.xpath("//article[@class='product_pod']")

        for book in books:
            url_book_page = book.xpath(".//h3//a/@href").get()

            user_agent = USER_AGENT_LIST[random.randint(0, len(USER_AGENT_LIST) - 1)]
            yield response.follow(url_book_page, callback=self.parse_book_page, headers={'User-Agent': user_agent})
                
        next_page_url = response.xpath("//li[@class='next']/a/@href").get()
        user_agent = USER_AGENT_LIST[random.randint(0, len(USER_AGENT_LIST) - 1)]

        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse, headers={'User-Agent': user_agent})
    
    def parse_book_page(self, response):
        print("################# SELECTED USER AGENT ##########################")
        print(response.request.headers.get('User-Agent').decode('utf-8'))
        
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
