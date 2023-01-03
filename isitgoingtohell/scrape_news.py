import datetime
import os
from typing import List

import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider

from isitgoingtohell.scrapers.spiders.aljazeera_spider import AlJazeeraSpider
from isitgoingtohell.scrapers.spiders.bbc_spider import BbcSpider
from isitgoingtohell.scrapers.spiders.reuters_spider import ReutersSpider


def run_spiders(spiders: List[CrawlSpider], output_csv: str) -> None:

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


def load_data(output_csv: str) -> pd.DataFrame:
    news_df = pd.read_csv(output_csv, delimiter="\t")
    print(news_df)
    news_df.drop_duplicates(subset=["headline"], inplace=True)
    print(news_df)
    news_df.reset_index(inplace=True, drop=True)
    return news_df


def scrape_news(output_csv: str) -> pd.DataFrame:

    # scrape news
    spiders = [BbcSpider]  # , AlJazeeraSpider  # ReutersSpider,
    run_spiders(spiders, output_csv)

    # load data, remove dupicates etc
    news_df = load_data(output_csv)

    # add scraping date
    news_df["scraped_at"] = datetime.datetime.now().isoformat()

    # remove csv file
    os.remove(output_csv)

    return news_df
