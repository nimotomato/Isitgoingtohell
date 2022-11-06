import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NewsCrawlSpider(CrawlSpider):
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
        #We could use this which gets every paragraph;
        # 'Text': " ".join(response.css('p::text').getall())

        #This css-selector gets text from most headers.

        #TO DO: 
        # Add timestamp, probably easiest to use CSS-selector time class
        # headlines = response.css('a h3::text')
        
        # for headline in headlines:
        #     if headline:
        #         yield{               
        #             'link': response.url,           
        #             'text': headline.get()
        #         }

        divs = response.css('div')
        for div in divs:
            if div.css('a h3::text'):
                yield{
                    'link': response.url,
                    'text': div.css('a h3::text').get(),
                    'time': div.css('time::attr(datetime)').get()
                }
