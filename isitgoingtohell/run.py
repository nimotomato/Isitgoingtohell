from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_json, delete_local_file, load_csv, write_csv, tuple_to_dict
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analyzer import sentiment_analysis
from isitgoingtohell.data_management.db_management import DB
from isitgoingtohell.data_management.data_analysis import Dated_methods as DM
import os
import pandas as pd
from isitgoingtohell.graph.graph import Dated_graph as DG
from isitgoingtohell.graph.graph import Undated_graph as UG

CACHE_FILENAME = 'cache.json'

def main():
    db = DB()
    dm = DM()
    # SCRAPE DATA
    if os.path.exists(CACHE_FILENAME):
        delete_local_file(CACHE_FILENAME)
    # Initiate webscraper
    run_spider(CACHE_FILENAME)

    # LOAD SCRAPED DATA
    data = load_json(CACHE_FILENAME)

    # UPLOAD TO DB
    run_db(data, db)
    
    # # LOAD DATA FROM DATABASE, OR JUST COMMENT OUT TO LOAD FROM FILE
    # scraped_data = db.get_unanalysed_data()
    # keys = db.get_col_names_not_id("data", 5).split(",")
    # data = [tuple_to_dict(item, keys) for item in scraped_data]
    
    # # AND ANALYZE DATA
    # analyzed_data = run_analyzer(data)

    # # UPLOAD TO DB
    # db.upload_analysed_data(analyzed_data)

    # # CALCULATE SENTIMENT RATIO FOR DATA
    # region_scores = dm.calculate_ratio_dated()

    # #EXTRACT DATA NEEDED FOR GRAPH 
    # geography_data = dm.populate_regions(region_scores)

    # AND UPLOAD TO DB
    # #upload_geography_data(region_scores, geography_data) #THIS UPLOADS DPLCIATES FUCK

    # #DRAW GRAPH
    # run_graph()
    # db.close_connection()
    # try:
    #     print("Cleanup initiated...")
    #     delete_local_file(CACHE_FILENAME)
    #     print(f"{CACHE_FILENAME} deleted. ")
    # except FileNotFoundError:
    #     pass

def upload_geography_data(region_scores, geography_data):
    dm = DM()
    db = DB()
    tables = db.get_col_names_not_id('geography', 4)
    dm.upload_populated_regions(tables, geography_data)
    db.close_connection()


def run_graph():
    # ug = UG()
    # ug.draw_undated_choropleth()
    dg = DG()
    dg.draw_dated_choropleth()

def run_db(data, db):
    if data:
        # We need number of columns for mogrification
        number_of_columns = len(data[0].keys())

        print("checking data for duplicates")
        data = db.remove_duplicates_batch(data)

        print("mogrifying data")
        data = db.mogrify_data(data, number_of_columns)

        if data:
            print("upload data")
            db.upload_data_postgres_mogrify(data, number_of_columns)
        else:
            print("No data to upload")


def run_analyzer(data) -> list:
    anal = sentiment_analysis.Analyzer()
    print("Analyzing data...")
    return anal.analyze_json(data)

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
    