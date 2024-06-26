import scrapy


class AudioSpiderSpider(scrapy.Spider):
    name = "audio_spider"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]


    def parse(self, response):
        pagination = response.xpath("//ul[contains(@class,'pagingElements')]/li")
        last_page = int(pagination[-2].xpath("./a/text()").get())
        current_page = 1

        while current_page <= last_page:
            
            yield scrapy.Request(url=f"https://www.audible.com/search?page={current_page}", callback=self.parse_item)
            
            current_page += 1


    def parse_item(self, response):
        items = response.xpath("//div[@id='center-3']//li[contains(@class, 'productListItem')]")

        for item in items:
            title = item.xpath(".//h3/a/text()").get()
            author = item.xpath(".//li[contains(@class, 'author')]//a/text()").get()
            length = item.xpath(".//li[contains(@class, 'runtime')]//span/text()").get().split(":")[-1].strip()

            yield {
                'title': title,
                'author': author,
                'length': length,
            }