from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_json, delete_local_file
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analyzer import sentiment_analysis
from isitgoingtohell.db_management.db_management import DB
from json import JSONDecodeError
import sys

cache_filename = 'cache.json'

def main():
    # Initiate webscraper
    run_spider(cache_filename)

    try:
        raw_json = load_json(cache_filename)
    except JSONDecodeError:
        delete_local_file(cache_filename)
        sys.exit("JSONDecodeError found. Probably faulty cache. \n Cache reset. Try again...")
    except FileNotFoundError:
        sys.exit("FileNotFoundError. Confirm cache_filename.")

    # Analyze data
    data = run_analyzer(raw_json)
    
    # Db stuff
    run_db(data)


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
                delete_local_file(cache_filename)
                print(f"{cache_filename} deleted. ")
            except FileNotFoundError:
                pass
        db.close_connection()

    else:
        print('No new items to upload. ')
        try:
            print("Cleanup initiated...")
            delete_local_file(cache_filename)
        except FileNotFoundError:
            pass

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
    