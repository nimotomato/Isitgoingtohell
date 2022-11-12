# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BbcScraperItem(scrapy.Item):
    text = scrapy.Field()
    time = scrapy.Field()
    region = scrapy.Field()
    label = scrapy.Field()
    score = scrapy.Field()


