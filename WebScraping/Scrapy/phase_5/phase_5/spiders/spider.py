import scrapy
from phase_5.items import BookItem
from ..user_agents import USER_AGENTS
import random

class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # Tracking user-agent
        print("User-Agent used to fetch start page:", response.request.headers.get('User-Agent').decode())
        bases = response.xpath("//article[@class='product_pod']")
        for base in bases:
            url_base = base.xpath("./h3/a/@href").get()
            user_agent = random.choice(USER_AGENTS)
            # Tracking user-agent
            print("Selected User-Agent for next request:", user_agent)
            yield response.follow(url_base, callback=self.parse_info_book,
                                    headers={'User-Agent': user_agent},
                                    meta={'selected_user_agent': user_agent})
        
        next_url = response.xpath("//li[@class='next']/a/@href").get()
        # Using relative url
        yield response.follow(next_url, callback=self.parse)
    
    def parse_info_book(self, response):
        # Retrieve the User-Agent from response headers
        response_user_agent = response.request.headers.get('User-Agent').decode()

        # Retrieve the User-Agent that was set for this request from meta
        selected_user_agent = response.meta['selected_user_agent']

        # Print both for comparison
        print("Selected User-Agent:", selected_user_agent)
        print("User-Agent received in response:", response_user_agent)

        # Check if the User-Agent matches the selected one
        if response_user_agent == selected_user_agent:
            print("User-Agent successfully applied.")
        else:
            print("Warning: User-Agent in response does not match the selected one.")


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