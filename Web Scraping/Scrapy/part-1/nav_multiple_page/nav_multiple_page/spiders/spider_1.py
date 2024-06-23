import scrapy

# CASES:
#   - Scraping multiple page

class Spider1Spider(scrapy.Spider):
    name = "spider_1"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # Title: //article[@class='product_pod']//h3//a/text()
        # Price: //article[@class='product_pod']//p[@class='price_color']
        # URL: //article[@class='product_pod']//h3//a/@href
        # Next button: //li[@class='next']/a/@href

        books = response.xpath("//article[@class='product_pod']")
        
        for book in books:
            yield {
                'name': book.xpath(".//h3//a/text()").get(),
                'price': book.xpath(".//p[@class='price_color']").get(),
                'url': book.xpath(".//h3//a/@href").get()
            }
        
        next_page_url = response.xpath("//li[@class='next']/a/@href").get()
        
        # Using relative path
        # if next_page_url is not None:
        #     yield response.follow(next_page_url, callback=self.parse)

        # Alternative using absolute path
        if next_page_url is not None:
            if 'catalogue/' not in next_page_url:
                next_page_url = 'catalogue/' + next_page_url
            
            yield response.follow("https://books.toscrape.com/" + next_page_url, callback=self.parse)