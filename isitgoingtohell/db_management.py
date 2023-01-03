import os

import pandas as pd
from sqlalchemy import create_engine, text

# from sqlalchemy.exc import IntegrityError


def upload_data(analysed_news_df: pd.DataFrame):
    """uploads all data to postgres db

    see schema in schema/news"""
    url = (
        f"postgresql+psycopg2://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )
    engine = create_engine(
        url,
        echo=False,
    )
    with engine.connect() as conn:
        for _, row in analysed_news_df.iterrows():
            query = (
                f"INSERT INTO news (headline, date, region, scraped_at, label, score)"
                f"VALUES {tuple(row.to_dict().values())} ON CONFLICT (headline) DO NOTHING;"
            )
            r = conn.execute(text(query))
            print(r)
