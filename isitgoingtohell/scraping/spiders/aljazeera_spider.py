"""scraper for www.aljazeera.com"""

from datetime import date as date1
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from isitgoingtohell.scraping.items import NewsHeadline


class AlJazeeraSpider(CrawlSpider):
    name = "AlJazeera_crawl"
    allowed_domains = ["www.aljazeera.com"]
    start_urls = [
        "https://www.aljazeera.com/news/2022/12/8/tunisia-fails-to-protect-women-despite-law-in-place-hrw-says"
    ]

    le_page_details = LinkExtractor(allow=r"/")
    rule_page_details = Rule(le_page_details, callback="parse_item", follow=True)
    rules = (rule_page_details,)

    def parse_item(self, response):
        # Find all divs in page
        # Find most headlines and timestamps within div

        if response.css("header.article-header h1 ::text"):
            scraper_item = NewsHeadline()
            # Format text regarding quotation marks, assist in future SQL-queries
            scraper_item["headline"] = (
                response.css("header.article-header h1 ::text")
                .get()
                .replace("'", "")
                .replace("\u2018", "")
                .replace("\u2019", "")
            )

            # Make sure there is a timestamp. If not stamp of news, then stamp when scraped.
            date = (
                response.css("div.article-dates span.screen-reader-text ::text")
                .get()
                .split("On ")[1]
            )
            formatted_date = datetime.strptime(date, "%d %b %Y")
            scraper_item["date"] = formatted_date.date()
            region = response.xpath("//meta").re(
                'name=["]where["] content=["]([a-zA-Z]+\s?(?:[a-zA-Z]+)?)'
            )[0]
            scraper_item["region"] = region.lower()

            # add source
            scraper_item["source"] = "www.aljazeera.com"

            yield scraper_item
