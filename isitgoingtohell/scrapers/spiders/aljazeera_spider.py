import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from isitgoingtohell.scrapers.items import AljazeeraScraperItem
from datetime import datetime
from datetime import date as date1
import re

class AlJazeeraSpider(CrawlSpider):
    name = 'AlJazeera_crawl'
    allowed_domains = ['www.aljazeera.com']
    start_urls = ['https://www.aljazeera.com/news/2022/12/8/tunisia-fails-to-protect-women-despite-law-in-place-hrw-says']
    

    le_page_details = LinkExtractor(allow=r'/')
    rule_page_details = Rule(le_page_details, callback='parse_item', follow=True)
    rules = (
        rule_page_details,

    )

    def parse_item(self, response):
        # Find all divs in page
        # Find most headlines and timestamps within div
        
        if response.css('header.article-header h1 ::text'):
            scraper_item = AljazeeraScraperItem()
            # Format text regarding quotation marks, assist in future SQL-queries
            scraper_item['headline'] = response.css('header.article-header h1 ::text').get().replace("'", "").replace("\u2018","").replace("\u2019", "")

            # Make sure there is a timestamp. If not stamp of news, then stamp when scraped.
            try:
                date = response.css('div.article-dates span.screen-reader-text ::text').get().split('On ')[1]
                formatted_date = datetime.strptime(date, '%d %b %Y')
                scraper_item['date'] = formatted_date.date()   
            except:
                scraper_item['date'] = str(date1.today().isoformat())  
            region = response.xpath('//meta').re('name=[\"]where[\"] content=[\"]([a-zA-Z]+\s?(?:[a-zA-Z]+)?)')[0]
            scraper_item['region'] = region.lower()
            
            yield scraper_item