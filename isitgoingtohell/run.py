from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_json, delete_local_file
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analyzer import sentiment_analysis
from isitgoingtohell.db_management import db_management

def main():
    cache_filename = 'cache.json'

    # Initiate webscraper
    run_spider(cache_filename)

    raw_json = load_json(cache_filename)

    # Analyze data
    data = run_analyzer(raw_json)
    
    # Db stuff
    run_db(data)


def run_db(data):
    if data:
        db = db_management.DB()
        db.upload_data_postgres(data)

        if db.verify_data(data):
            delete_local_file('cache.json')

        db.close_connection()

    else:
        print("No new items to upload. ")
        delete_local_file('cache.json')

def run_analyzer(json_data) -> list:
    anal = sentiment_analysis.Analyzer()
    print("Analyzing data...")
    return anal.analyze_json(json_data)

def run_spider(output_filename):
    process = CrawlerProcess(settings={'FEED_FORMAT': 'json',
        'FEED_URI': output_filename,
        'ITEM_PIPELINES': {
    'isitgoingtohell.bbc_scraper.pipelines.DuplicatesPipeline': 200
    }}
    )
    process.crawl(BbcSpider)
    process.start()
    

if __name__ == "__main__":
    main()
    