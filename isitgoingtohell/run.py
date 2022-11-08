# from isitgoingtohell.sentiment_analysis.sentiment_analyser import SentimentAnalyser
from transformers import pipeline
from isitgoingtohell.bbc_scraper.spiders.bbc_spider import BbcSpider
from isitgoingtohell.utils import load_toml, load_json
from scrapy.crawler import CrawlerProcess
import pprint

def main():

    # # load config
    # config = load_toml("config.toml")

    # # set up sentiment analysis model
    # sentiment_analyser = pipeline(model=config["sentiment_analysis"]["model"])

    run_spider()

    # some random news
    # news = [
    #     """TikTok influencer cleans people's homes for free
    # TikTok influencer cleans people's homes for free

    # Auri Katariina, a cleaner from Finland, began posting videos on social media which became an instant hit. People started reaching out to her for help and she now cleans homes around the world for free.

    # Auri's videos get millions of views and the BBC went to meet her on a recent trip to the United Kingdom."""
    # ]

    
#     news = [d["text"] for d in load_json("items.json")]

# # get sentiment
#     scores = sentiment_analyser(news)
#     pprint.pprint(list(zip(news, scores)))

def run_spider():
    process = CrawlerProcess()
    process.crawl(BbcSpider)
    process.start()

if __name__ == "__main__":
    main()
    