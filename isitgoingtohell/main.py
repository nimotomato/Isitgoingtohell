import pandas as pd
from sqlalchemy import create_engine
from transformers import pipeline

from isitgoingtohell.scrapers.scrape_news import scrape_news
from isitgoingtohell.utils import load_toml


def analyze_sentiment(news, batch_size=64):
    # TODO CHANGE THIS MODEL?
    sentiment_analyser = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

    results = []
    for i in range(0, len(news), batch_size):
        results.extend(sentiment_analyser(news[i : i + batch_size]))

    return pd.DataFrame(results)


def main():

    output_csv = "output_news.csv"

    news_df = scrape_news(output_csv)
    print(news_df)

    sentiments_df = analyze_sentiment(news_df["headline"].to_list())
    print(sentiments_df)

    analysed_news_df = pd.concat([news_df, sentiments_df], axis=1)
    print(analysed_news_df)

    # TODO upload dataframe to sql database https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    # engine = create_engine("<CONNECTION INFO>", echo=False)
    # analysed_news_df.to_sql("news", con=engine, if_exists="replace", index_label="id")

    # TODO calculate statistics


if __name__ == "__main__":
    main()
