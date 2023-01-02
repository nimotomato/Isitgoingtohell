import os

import pandas as pd
from scrapy.crawler import CrawlerProcess

from isitgoingtohell.scrapers.spiders.aljazeera_spider import AlJazeeraSpider
from isitgoingtohell.scrapers.spiders.bbc_spider import BbcSpider
from isitgoingtohell.scrapers.spiders.reuters_spider import ReutersSpider


def run_spiders(spiders, output_csv):

    process = CrawlerProcess(
        settings={
            "CLOSESPIDER_ITEMCOUNT": 80,
            "OUTPUT_CSV": output_csv,
            "ITEM_PIPELINES": {
                "isitgoingtohell.scrapers.pipelines.RegionPipeline": 300,
                "isitgoingtohell.scrapers.pipelines.RemoveUncategorized": 800,
                "isitgoingtohell.scrapers.pipelines.CsvWriterPipeline": 900,
            },
        }
    )

    for spider in spiders:
        process.crawl(spider)

    process.start()


def load_data(output_csv):
    news_df = pd.read_csv(output_csv, delimiter="\t")
    news_df.drop_duplicates(subset=["headline"], inplace=True)
    news_df.reset_index(inplace=True)
    return news_df


def scrape_news(output_csv):

    # scrape news
    spiders = [BbcSpider, AlJazeeraSpider]  # ReutersSpider,
    run_spiders(spiders, output_csv)

    # load data, remove dupicates etc
    news_df = load_data(output_csv)

    # remove csv file
    os.remove(output_csv)

    return news_df
