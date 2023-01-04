# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsHeadline(scrapy.Item):
    headline = scrapy.Field()
    date = scrapy.Field()
    region = scrapy.Field()
