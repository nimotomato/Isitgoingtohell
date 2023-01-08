import os

import pandas as pd
from sqlalchemy import create_engine, text


def upload_data(analysed_news_df: pd.DataFrame) -> int:
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

    n_uploads = 0
    with engine.connect() as conn:
        for _, row in analysed_news_df.iterrows():
            query = (
                f"INSERT INTO news (headline, date, region, source, label, score)"
                f"VALUES {tuple(row.to_dict().values())} ON CONFLICT (headline) DO NOTHING;"
            )
            r = conn.execute(text(query))

            # if we add an item rowcount is 1, if its a dupliacte its 0
            n_uploads += r.rowcount

    return n_uploads
