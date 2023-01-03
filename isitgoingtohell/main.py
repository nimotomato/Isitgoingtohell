import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

from isitgoingtohell.analyze_sentiment import analyze_sentiment
from isitgoingtohell.scrape_news import scrape_news


def upload_data(analysed_news_df: pd.DataFrame):
    # TODO upload dataframe to sql database https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    username = "dev"
    password = "pass"
    host = "news-db"
    port = "5432"
    db_name = "news-db"

    engine = create_engine(
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}", echo=False
    )
    with engine.connect() as conn:
        for _, row in analysed_news_df.iterrows():
            query = (
                f"INSERT INTO news (headline, date, region, scraped_at, label, score)"
                f"VALUES {tuple(row.to_dict().values())} ON CONFLICT (headline) DO NOTHING;"
            )
            conn.execute(text(query))


def main():

    output_csv = "output_news.csv"

    news_df = scrape_news(output_csv)
    print(news_df)

    sentiments_df = analyze_sentiment(news_df["headline"].to_list())
    print(sentiments_df)

    analysed_news_df = pd.concat([news_df, sentiments_df], axis=1)
    print(analysed_news_df)

    upload_data(analysed_news_df)


if __name__ == "__main__":
    main()
