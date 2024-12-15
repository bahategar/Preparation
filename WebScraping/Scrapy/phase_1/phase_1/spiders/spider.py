import scrapy


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    ### CSS VERSION ###
    def parse(self, response):
        # Select product pods using CSS selector
        bases = response.css("article.product_pod")
        for base in bases:
            yield {
                # Select the book name using the 'title' attribute of the <a> tag inside <h3>
                # 'name': base.css("h3 a::attr(title)").get() or base.css("h3 *::text").get(),
                # Select the price using the 'price_color' class
                'price': base.css("p.price_color::text").get(),
                # Select the relative URL of the book using the 'href' attribute
                'url': base.css("h3 a::attr(href)").get(),
            }

        # Select the next page URL using the 'next' class
        next_url = response.css("li.next a::attr(href)").get()
        # Using absolute URL approach
        if next_url is not None:
            if 'catalogue/' in next_url:
                next_url = 'https://books.toscrape.com/' + next_url
            else:
                next_url = 'https://books.toscrape.com/catalogue/' + next_url
            yield response.follow(next_url, callback=self.parse)

    ### XPATH VERSION ###
    # def parse(self, response):

    #     bases = response.xpath("//article[@class='product_pod']")
    #     for base in bases:
    #         yield {
    #             'name': base.xpath(".//h3/a/@title").get() or base.xpath(".//h3//text()").get(),
    #             'price': base.xpath(".//p[@class='price_color']/text()").get(),
    #             'url': base.xpath(".//h3/a/@href").get(),
    #         }
    #     next_url = response.xpath("//li[@class='next']/a/@href").get()
    #     # Using Absolure URL Approach
    #     if next_url is not None:
    #         if 'catalogue/' in next_url:
    #             next_url = 'https://books.toscrape.com/' + next_url
    #         else:
    #             next_url = 'https://books.toscrape.com/catalogue/' + next_url
    #         yield response.follow(next_url, callback=self.parse)

    #     # # Using Relative URL
    #     # yield response.follow(next_url, callback=self.parse)

