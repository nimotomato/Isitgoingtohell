from logging import getLogger

import pandas as pd

from isitgoingtohell.analyze_sentiment import analyze_sentiment
from isitgoingtohell.db_management import upload_data
from isitgoingtohell.scraping.scrape_news import scrape_news

log = getLogger("MAIN")


def main():

    log.info("Scraping news ...")
    news_df = scrape_news()
    n_news = len(news_df)
    log.info(f"Scraped {n_news} news")

    log.info("Analyzing sentiment ...")
    sentiments_df = analyze_sentiment(news_df["headline"].to_list())

    analysed_news_df = pd.concat([news_df, sentiments_df], axis=1)

    log.info("Uploading data ...")
    result = upload_data(analysed_news_df)

    log.info(
        f"REPORT: \nScraped news: {n_news} \nUploaded news: {result} \nNumber duplicates: {n_news-result}"
    )


if __name__ == "__main__":
    main()
