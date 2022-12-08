import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from isitgoingtohell.scrapers.items import AljazeeraScraperItem
from datetime import date
import re

class AlJazeeraSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['www.aljazeera.com']
    start_urls = ['https://www.aljazeera.com/news/']
    

    le_page_details = LinkExtractor(allow=r'/')
    rule_page_details = Rule(le_page_details, callback='parse_item', follow=False)
    rules = (
        rule_page_details
    )

    def parse_item(self, response):
        # Find all divs in page
        divs = response.css('div')

        for div in divs:
           # Find most headlines and timestamps within div
           scraper_item = AljazeeraScraperItem()
           if div.css('h3::text'):
                # Format text regarding quotation marks, assist in future SQL-queries
                scraper_item['headline'] = div.css('a h3::text').get().replace("\xad", "")

                # # Make sure there is a timestamp. If not stamp of news, then stamp when scraped.
                # try:
                #     scraper_item['date'] = div.css('time::attr(datetime)').get().split('T')[0]
                #     if scraper_item['date'] == "P":
                #         scraper_item['date'] = str(date.today().isoformat())     
                # except:
                #     scraper_item['date'] = str(date.today().isoformat())  
                # region = re.search(r"/world/([a-z]+_?[a-z]+?[a-z]+_?[a-z]+)", response.url)
                # scraper_item['region'] = region.group(1)

                yield scraper_item