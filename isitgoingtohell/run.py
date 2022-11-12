from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import write_json
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analyzer import sentiment_analysis
from isitgoingtohell.db_management import db_management

def main():
    # Initiates webscraper
    run_spider()

    # Analyzes data
    data = analyze_data()

    # Save data locally
    write_json(data)

    # # TO DO: upload data to postgres @ render
    # db = db_management.DB()
    # db.upload_data(filename="anal_result.json")

def analyze_data() -> list:
    anal = sentiment_analysis.Analyzer()
    return anal.analyze_json()

def run_spider():
    process = CrawlerProcess(settings={'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json',
        'ITEM_PIPELINES': {
    'isitgoingtohell.bbc_scraper.pipelines.DuplicatesPipeline': 200
    }}
    )
    process.crawl(BbcSpider)
    process.start()

if __name__ == "__main__":
    main()
    