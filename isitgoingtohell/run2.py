from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_json, delete_local_file, tuple_to_dict, number_of_keys, stringify_list
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analyzer.sentiment_analysis import Analyser
from isitgoingtohell.data_management.db_management2 import Database as DB
from isitgoingtohell.graph.graph2 import Dated_graph
import os
import pandas as pd
from sys import argv

CACHE_FILENAME = 'cache.json'
COMMAND_LIST = [
    '-full_script',
    '-scraper',
    '-scraper-upload',
    '-sentiment_from_file',
    '-sentiment_from_file-upload',
    '-sentiment_from_db',
    '-dated_graph',
    '-undated_graph',
    '-sentiment_from_db-upload',
    '-calculate_graph_data-upload'
    ]


def main():    
    # SCRAPE DATA
    db = DB()
    # if os.path.exists(CACHE_FILENAME):
    #     delete_local_file(CACHE_FILENAME)
    # # Initiate webscraper
    # run_spider(CACHE_FILENAME)

    # Store scraper output locally
    raw_data = load_json(CACHE_FILENAME)

    # Upload local files
    db = DB()
    # upload_scraped_data(raw_data, db)

    # Sentiment analysis from file or from database
    # analysed_data = sentiment_analysis(db, from_local=True)

    # # Upload analysed data
    # upload_analysed_data(analysed_data, db)
    # ug = UG()
    # graph_calculations(ug)


    # Retrieve geo data 
    data = db.get_geography_data()
    column_names = db.get_column_names('geography')
    dated_graph = Dated_graph(data, column_names)

    # Show graph
    show_graph(dated_graph, db, dated=True)

    # try:
    #     db.close_connection()
    # except:
    #     pass
    # try:
    #     print("Cleanup initiated...")
    #     delete_local_file(CACHE_FILENAME)
    #     print(f"{CACHE_FILENAME} deleted. ")
    # except FileNotFoundError:
    #     pass


def show_graph(graph_object, database_object, dated=False):
    if dated:
        data = database_object.get_geography_data(dated=True)
        column_names = data[0].keys()
        database_object.draw_dated_choropleth()
    else:
        pass

def sentiment_analysis(db, from_local=False, local_data_path=CACHE_FILENAME) -> list[dict]:
    if from_local:
        data = load_json(local_data_path)
    else:
        data = db.get_unanalysed_data()
    anal = Analyser()
    print("analyzing data...")
    return anal.analyze_data(data)

def upload_scraped_data(raw_data, db):
    print("checking data for duplicates")
    data = db.remove_duplicates_batch(raw_data)
    print("mogrifying data")
    col_number = db.get_column_count()
    data = db.mogrify_data(data, col_number)
    if data:
        print("uploading data")
        columns = db.get_column_names()[:3]
        db.insert_batch(data, columns)
    else:
        print("no data to upload")

def upload_analysed_data(analysed_data, db):
    print("uploading analysed data")
    db.upload_analysed_data(analysed_data)


def run_spider(CACHE_FILENAME):
    process = CrawlerProcess(settings={'FEED_FORMAT': 'json',
        'FEED_URI': CACHE_FILENAME,
        'ITEM_PIPELINES': {
    'isitgoingtohell.bbc_scraper.pipelines.DuplicatesPipeline': 200,
    #MAYBE THIS SHOULD BE LESS THAN 200
    'isitgoingtohell.bbc_scraper.pipelines.RegionPipeline': 300
    }}
    )
    process.crawl(BbcSpider)
    process.start()
    

if __name__ == "__main__":
    main()