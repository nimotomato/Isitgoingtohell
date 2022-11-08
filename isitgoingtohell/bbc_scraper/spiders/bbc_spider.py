import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from isitgoingtohell.bbc_scraper.items import BbcScraperItem
from datetime import date
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
    #     divs = response.css('div')
    #     for div in divs:
    #         #Find most headlines and timestamps within div.
    #         if div.css('a h3::text'):
    #             yield{
    #                 'link': response.url,
    #                 'text': div.css('a h3::text').get(),
    #                 'time': div.css('time::attr(datetime)').get()
    #             }

    #for connecting with postgreSQL. Dont forget to enable fields in items.py, the pipelines.py AS WELL AS activate ITEM_PIPELEINES in settings.py
            #Find all divs
        divs = response.css('div')
        for div in divs:
            #Find most headlines and timestamps within div.
           scraper_item = BbcScraperItem()
           if div.css('a h3::text'):
                scraper_item['link'] = response.url
                scraper_item['text'] = div.css('a h3::text').get()
                scraper_item['time'] = div.css('time::attr(datetime)').get()
                if scraper_item['time'] == None:
                    scraper_item['time'] = date.today().strftime('%Y-%m-%d')
                yield scraper_item
