import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com/news/world']
    


    le_page_details = LinkExtractor(allow=r'news/')
    rule_page_details = Rule(le_page_details, callback='parse_item', follow=False)
    rules = (
        rule_page_details
        ,
    )

    def parse_item(self, response):
        yield{
            'Link': response.url,
            'Text': " ".join(response.css('p::text').getall())
        }