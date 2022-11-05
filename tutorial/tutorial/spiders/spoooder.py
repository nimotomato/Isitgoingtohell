import scrapy

class SpooderSpider(scrapy.Spider):
    name = 'spood'
    allowed_domains = ['bbc.com/']
    start_urls = ['https://www.bbc.com/news/world']

    def parse(self, response):
        for link in response.css('ol.gs-u-m0.gs-u-p0.lx-stream__feed.qa-stream a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_articles)

    def parse_articles(self, response):
        for article in response.css('p::text').getall():
            yield {
                'text': article
            }
