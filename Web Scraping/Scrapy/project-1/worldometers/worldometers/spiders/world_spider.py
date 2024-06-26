import scrapy


class WorldSpiderSpider(scrapy.Spider):
    name = "world_spider"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//table//tr/td[2]")
        
        for country in countries:
            country_name = country.xpath("./a/text()").get()
            url_country = country.xpath("./a/@href").get()
            print("COUNTRY NAME", country_name)
            print("URL COUNTRY", url_country)
            # yield { 'country_name': country_name, 'url_country': url_country}
            yield response.follow(url=url_country, callback=self.parse_country, meta={'country': country_name})

    def parse_country(self, response):
        country = response.request.meta['country']
        rows = response.xpath("(//div[@class='table-responsive']/table)[1]/tbody/tr")

        for row in rows:
            year = row.xpath("./td[1]/text()").get()
            population = row.xpath("./td[2]/text()").get()

            yield {
                'country': country,
                'year': year,
                'population': population,
            }