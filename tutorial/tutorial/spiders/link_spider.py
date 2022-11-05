import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


#https://www.bbc.com/news/world/africa

class LinkSpider(CrawlSpider):
    name = 'links'
    start_urls = [
        'https://www.bbc.com/news/world',
    ]
    
    rules = (
        Rule(LinkExtractor(allow='world'), callback='parse_item')
    )

    def parse_item(self, response):
        yield{
            'text': " ".join(response.css("p::text").getall())
        }
