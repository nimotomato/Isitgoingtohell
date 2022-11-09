# from isitgoingtohell.sentiment_analysis.sentiment_analyser import SentimentAnalyser
from transformers import pipeline
from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_toml, load_json
from scrapy.crawler import CrawlerProcess
from isitgoingtohell.bbc_scraper import settings
import pprint

def main():

    # # load config
    # config = load_toml("config.toml")

    # # set up sentiment analysis model
    # sentiment_analyser = pipeline(model=config["sentiment_analysis"]["model"])
    run_spider()
    
#     news = [d["text"] for d in load_json("items.json")]

# # get sentiment
#     scores = sentiment_analyser(news)
#     pprint.pprint(list(zip(news, scores)))

def run_spider():
    process = CrawlerProcess(settings={
        'ITEM_PIPELINES': {
   'isitgoingtohell.bbc_scraper.pipelines.BbcScraperPipeline': 300}
    })
    process.crawl(BbcSpider)
    process.start()

if __name__ == "__main__":
    main()
    