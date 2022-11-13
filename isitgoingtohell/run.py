from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import write_json, load_json
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.sentiment_analyzer import sentiment_analysis
from isitgoingtohell.db_management import db_management

def main():
    # # Initiates webscraper
    # run_spider('result.json')

    # # Analyzes data
    # data = analyze_data('result.json')

    # # Save data locally
    # write_json(data)

    db = db_management.DB()
    data=load_json("result.json")

    # TO DO: fix this shit
    # db.upload_data_postgres(data)

    # if db.verify_data(data):
    #     db.delete_local_file()


def analyze_data(json_file) -> list:
    anal = sentiment_analysis.Analyzer()
    return anal.analyze_json(filename=json_file)


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
    