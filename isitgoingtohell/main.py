import pandas as pd

from isitgoingtohell.analyze_sentiment import analyze_sentiment
from isitgoingtohell.db_management import upload_data
from isitgoingtohell.scraping.scrape_news import scrape_news


def main():

    news_df = scrape_news()
    print(news_df)

    sentiments_df = analyze_sentiment(news_df["headline"].to_list())
    print(sentiments_df)

    analysed_news_df = pd.concat([news_df, sentiments_df], axis=1)
    print(analysed_news_df)

    upload_data(analysed_news_df)


if __name__ == "__main__":
    main()
