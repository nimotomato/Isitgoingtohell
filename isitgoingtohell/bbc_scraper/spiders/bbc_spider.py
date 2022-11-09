import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from isitgoingtohell.bbc_scraper.items import BbcScraperItem
from datetime import date
import re

class BbcSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com/news/world']
    

    le_page_details = LinkExtractor(allow=r'world/')
    rule_page_details = Rule(le_page_details, callback='parse_item', follow=False)
    rules = (
        rule_page_details
        ,
    )

    def parse_item(self, response):
    #     #Find all divs
        divs = response.css('div')
        for div in divs:
            #Find most headlines and timestamps within div.
           scraper_item = BbcScraperItem()
           if div.css('a h3::text'):
                scraper_item['text'] = div.css('a h3::text').get().replace("'", "''")
                try:
                    scraper_item['time'] = div.css('time::attr(datetime)').get().split('T')[0]
                except:
                    scraper_item['time'] = str(date.today().isoformat())     
                region = re.search(r"/world/([a-z]+_?[a-z]+?[a-z]+_?[a-z]+)", response.url)
                scraper_item['region'] = region.group(1)

                yield scraper_item