"""scraper for https://www.bbc.com/news/world"""
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from isitgoingtohell.scraping.items import NewsHeadline


class BbcSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['www.bbc.com']
    start_urls = [
        'https://www.bbc.com/news/', 
        'https://www.bbc.com/news/world',
        'https://www.bbc.com/news/world/africa',
        'https://www.bbc.com/news/world/asia',
        'https://www.bbc.com/news/world/australia',
        'https://www.bbc.com/news/world/europe',
        'https://www.bbc.com/news/world/latin_america',
        'https://www.bbc.com/news/world/middle_east',
        'https://www.bbc.com/news/world/us_and_canada'
        ]
    

    le_page_details = LinkExtractor(allow=r'news')
    rule_page_details = Rule(le_page_details, callback='parse_item', follow=False)
    rules = (
        rule_page_details
        ,
    )

    def parse_item(self, response):
        scraper_item = NewsHeadline()
        if response.css('h1[id="main-heading"] ::text').get():
            scraper_item['headline'] = response.css('h1[id="main-heading"] ::text').get().replace("'", "")
            scraper_item['date'] = response.css('time::attr(datetime)').get().split('T')[0]
            if scraper_item['date'] == "P":
                scraper_item['date'] = None     
            region = re.search(r"\/world\/?-?([a-z]+_?[a-z]+?[a-z]+_?[a-z]+)", response.url)
            scraper_item['region'] = region.group(1)
            yield scraper_item