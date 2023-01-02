import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from isitgoingtohell.scrapers.items import ReutersScraperItem
from datetime import datetime
from datetime import date as date1
import re

class ReutersSpider(CrawlSpider):
    name = 'reuters_crawl'
    allowed_domains = ['www.reuters.com']
    start_urls = ['https://www.reuters.com/world/']
    

    le_page_details = LinkExtractor(allow=r'world/')
    rule_page_details = Rule(le_page_details, callback='parse_item', follow=True)
    rules = (
        rule_page_details,

    )

    def parse_item(self, response):  
        scraper_item = ReutersScraperItem()
        scraper_item['headline'] = response.css('h1 ::text').get().replace("'", "")
        #Date
        date = response.css('span.date-line__date__23Ge- ::text').getall()[1]
        formatted_date = datetime.strptime(date, '%B %d, %Y')
        scraper_item['date'] = formatted_date.date()   
        
        region = response.css('nav.article-header__tags__3-jcV ::text').get()
        scraper_item['region'] = region.lower()
        yield scraper_item