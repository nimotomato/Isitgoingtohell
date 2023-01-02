from isitgoingtohell.scrapers.spiders.bbc_spider import BbcSpider
from isitgoingtohell.scrapers.spiders.reuters_spider import ReutersSpider
from isitgoingtohell.scrapers.spiders.aljazeera_spider import AlJazeeraSpider
from isitgoingtohell.utils import load_json, delete_local_file
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analysis.sentiment_analysis import Analyser
from isitgoingtohell.data_management.db_management import Database as DB
from isitgoingtohell.graph.graph import Dated_graph as DG
from isitgoingtohell.graph.graph import Undated_graph as UG
from isitgoingtohell.label_analysis.label_analysis import Dated_methods
from isitgoingtohell.label_analysis.label_analysis import Undated_methods as UM
import os

CACHE_FILENAME = 'cache.json'

def main():    
    # SCRAPE DATA
    # db = DB()
    if os.path.exists(CACHE_FILENAME):
        delete_local_file(CACHE_FILENAME)
    # Initiate webscraper
    run_spider(spider_name=BbcSpider)
    #run_spider(spider_name=ReutersSpider)
    # #run_spider(spider_name=AlJazeeraSpider)

    # # Store scraper output locally
    # raw_data = load_json(CACHE_FILENAME)

    # # Upload local files
    # upload_scraped_data(raw_data, db)

    # # Sentiment analysis from file or from database
    # analysed_data = sentiment_analysis(db, from_local=True, local_data_path=CACHE_FILENAME)
    
    # # Upload analysed data
    # upload_analysed_data(analysed_data, db)

    # # Calculate new ratios
    # mean_ratios_undated = calculate_mean_ratios_undated()
    # # Upload new ratios
    # upload_mean_ratios_undated(db, mean_ratios_undated)
    
    #Calculate label ratios from database:
    # dm = Dated_methods()
    # dated_ratio_data = dm.calculate_ratio_dated()

    # # Sort and upload label ratios and geographic data:
    # upload_label_analysis(undated_ratio_data, db, dated=False, label_analysis_object=um)
   
    # upload_label_analysis(dated_ratio_data, db, dated=True, label_analysis_object=dm)

    # # Retrieve label ratios and geographic data from database:
    # dated_data = db.get_graph_data(dated=True)

    # condition = "WHERE calculation_date = '2022-11-18'"
    # undated_data = db.get_graph_data(dated=False, condition=condition)

    # # Show graphs:
    # show_graph(dated_data, database_object=db, dated=True)
    # show_graph(undated_data, dated=False)

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



def show_graph(data, database_object=None, dated=True):
    if dated:
        column_names = database_object.get_column_names(tablename='geography')
        dg = DG(data, column_names)
        dg.draw_dated_choropleth()
    else:
        ug = UG(data)
        ug.draw_undated_choropleth()

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
    col_number = len(raw_data[0].keys())
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

def calculate_mean_ratios_undated():
    um = UM()
    ratios = um.calculate_ratio_undated()
    formatted_ratios = um.format_ratios(ratios)
    undated_mean_data = um.add_metadata(formatted_ratios)
    new_means = um.calculate_new_mean(used_ratios=um.used_ratios, formated_unused_ratios=undated_mean_data)
    um.update_used_data()
    return new_means

def upload_mean_ratios_undated(database_object, mean_ratios_undated):
    # Prepare for upload
    cols = database_object.get_column_count(tablename='geography_undated')
    mogrified_data = database_object.mogrify_data(data=mean_ratios_undated, number_of_columns=cols)
    # Upload
    database_object.upload_geography_data(mogrified_data=mogrified_data, dated=False)

# def upload_label_analysis(label_analysis_data, database_object, dated: bool, label_analysis_object):
#     if dated:
#         # Sort data
#         presorted_data = label_analysis_object.pre_sort_scores_dated(label_analysis_data)
#         # Prepare for upload
#         number_of_columns = database_object.get_column_count(tablename='geography')
#         mogrified_data = database_object.mogrify_data(data=presorted_data, number_of_columns=number_of_columns)
#         # Upload
#         database_object.upload_geography_data(mogrified_data=mogrified_data, dated=dated)
#     else:
#         # Sort data
#         sorted_data = label_analysis_object.pre_sort_scores_undated(label_analysis_data)
#         data = label_analysis_object.add_metadata(sorted_data, database_object=database_object)
#         # Prepare for upload
#         cols = database_object.get_column_count(tablename='geography_undated')
#         mogrified_data = database_object.mogrify_data(data=data, number_of_columns=cols)
#         # Upload
#         database_object.upload_geography_data(mogrified_data=mogrified_data, dated=dated)

def run_spider(spider_name, CACHE_FILENAME=CACHE_FILENAME):
    process = CrawlerProcess(settings={'FEED_FORMAT': 'json',
        'CLOSESPIDER_ITEMCOUNT': 80,
        'FEED_URI': CACHE_FILENAME,
        'ITEM_PIPELINES': {
            'isitgoingtohell.scrapers.pipelines.DuplicatesPipeline': 200,
            'isitgoingtohell.scrapers.pipelines.RegionPipeline': 300,
            'isitgoingtohell.scrapers.pipelines.RemoveUncategorized': 900
            }
        }
    )
    process.crawl(spider_name)
    process.start()
    
if __name__ == "__main__":
    main()