from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_json, delete_local_file
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analyzer import sentiment_analysis
from isitgoingtohell.data_management.db_management import DB
from isitgoingtohell.data_management.data_analysis import Calculate_ratio_dated as CRD
from isitgoingtohell.data_management.data_analysis import Calculate_ratio_total as CRT
import os
import pandas as pd


CACHE_FILENAME = 'cache.json'

def main():
    # if os.path.exists(CACHE_FILENAME):
    #     delete_local_file(CACHE_FILENAME)
    # # Initiate webscraper
    # run_spider(CACHE_FILENAME)

    # raw_news_data = load_json(CACHE_FILENAME)

    # # Analyze data
    # analyzed_data = run_analyzer(raw_news_data)
    
    # # Db stuff
    # run_db(analyzed_data)

    crd = CRD()
    crt = CRT()

    data_dated = crd.calculate_ratio_dated()
    data_total = crt.calculate_ratio_total()
    print(data_dated, data_total)

def run_db(data):
    if data:
        db = DB()
        try:
            db.upload_data_postgres(data)
        except:
            print("Error uploading data.")

        if db.verify_data(data):
            try:
                print("Cleanup initiated...")
                delete_local_file(CACHE_FILENAME)
                print(f"{CACHE_FILENAME} deleted. ")
            except FileNotFoundError:
                pass
        db.close_connection()

    else:
        print('No new items to upload. ')
        try:
            print("Cleanup initiated...")
            delete_local_file(CACHE_FILENAME)
        except FileNotFoundError:
            pass

def run_analyzer(json_data) -> list:
    anal = sentiment_analysis.Analyzer()
    print("Analyzing data...")
    return anal.analyze_json(json_data)

def run_spider(CACHE_FILENAME):
    process = CrawlerProcess(settings={'FEED_FORMAT': 'json',
        'FEED_URI': CACHE_FILENAME,
        'ITEM_PIPELINES': {
    'isitgoingtohell.bbc_scraper.pipelines.DuplicatesPipeline': 200,
    'isitgoingtohell.bbc_scraper.pipelines.IsocodePipeline': 30
    }}
    )
    process.crawl(BbcSpider)
    process.start()
    

if __name__ == "__main__":
    main()
    