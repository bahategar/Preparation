# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Playwright1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QuoteItem(scrapy.Item):
    text = scrapy.Field(serializer=lambda x : x.replace("“", "").replace("”", ""))
    author = scrapy.Field()
    tags = scrapy.Field()