from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_json, delete_local_file, tuple_to_dict, number_of_keys
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analysis.sentiment_analysis import Analyser
from isitgoingtohell.data_management.db_management import DB
from isitgoingtohell.data_management.data_analysis import Dated_methods as DM
import os
import pandas as pd
from isitgoingtohell.graph.graph import Dated_graph as DG
from isitgoingtohell.graph.graph import Undated_graph as UG
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
    main_input = argv[1:]
    if not validate_args(main_input):
        print("Usage: ")
        for command in COMMAND_LIST:
            print(command)
        exit()

    if '-full_script' in main_input:
        main_input = " ".join(COMMAND_LIST[1:])

    if '-scraper' in main_input:
        # SCRAPE DATA
        if os.path.exists(CACHE_FILENAME):
            delete_local_file(CACHE_FILENAME)
        # Initiate webscraper
        run_spider(CACHE_FILENAME)
        if '-scraper-upload' in main_input:
            db = DB()
            run_db(load_json(CACHE_FILENAME), db)

    if '-sentiment_from_file' in main_input:
        # LOAD SCRAPED DATA
        data = load_json(CACHE_FILENAME)
        # ANALYZE DATA
        analyzed_data = run_analyzer(data)
        if '-sentiment_from_file-upload' in main_input:
            db = DB()
            # UPLOAD TO DB
            run_db(analyzed_data, db)
            db.close_connection()

    if '-sentiment_from_db' in main_input:
        db = DB()
        # LOAD DATA FROM DATABASE
        scraped_data = db.get_unanalysed_data()
        keys = db.get_col_names_not_id("data", 5).split(",")
        data = [tuple_to_dict(item, keys) for item in scraped_data]
        analyzed_data = run_analyzer(data)
        if '-sentiment_from_db-upload' in main_input:
            db = DB()
            # UPLOAD TO DB
            run_db(analyzed_data, db)
            db.close_connection()

    if '-calculate_graph_data' in main_input:
        dm = DM()
        # CALCULATE SENTIMENT RATIO FOR DATA
        region_scores = dm.calculate_ratio_dated()
        #EXTRACT DATA NEEDED FOR GRAPH 
        geography_data = dm.populate_regions(region_scores)
        # UPLOAD TO DB
        #upload_geography_data(geography_data) #THIS UPLOADS DPLCIATES FUCK
        if '-calculate_graph_data-upload' in main_input:
            upload_geography_data(geography_data)

    if '-dated_graph' in main_input:
        dg = DG()
        dg.draw_dated_choropleth()

    if '-undated_graph' in main_input:
        ug = UG()
        ug.draw_undated_choropleth()   
    
    try:
        db.close_connection()
    except:
        pass

    try:
        print("Cleanup initiated...")
        delete_local_file(CACHE_FILENAME)
        print(f"{CACHE_FILENAME} deleted. ")
    except FileNotFoundError:
        pass


def validate_args(main_input):
    if not main_input:
        return False
    for input in main_input:
        if input not in COMMAND_LIST:
            return False
    return True

def upload_geography_data(geography_data):
    db = DB()
    columns = db.get_col_names_not_id('geography', number_of_keys(geography_data))
    db.upload_populated_regions(columns, geography_data)

def run_graph():
    ug = UG()
    ug.draw_undated_choropleth()

def run_db(data, db):
    if data:
        print("checking data for duplicates")
        data = db.remove_duplicates_batch(data)
        print("mogrifying data")
        data = db.mogrify_data(data, number_of_keys(data))

        if data:
            print("upload data")
            db.upload_data_postgres_mogrify(data, number_of_keys(data))
        else:
            print("No data to upload")

def run_analyzer(data) -> list:
    anal = sentiment_analysis.Analyzer()
    print("Analyzing data...")
    return anal.analyze_data(data)

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