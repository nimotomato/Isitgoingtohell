import pandas as pd
from isitgoingtohell.data_management.db_management import Database as DB
from isitgoingtohell.utils import load_csv
from sqlalchemy import Table, Column, Float, String, Date, MetaData, create_engine

TABLENAME = 'data'
COLUMNS = ['date','region','label']

class Statistics():
    # Get data
    def __init__(self, data):
        # Load list of country codes corresponding to region.
        self.country_codes = load_csv("only_codes.csv")
        self.dataframe = pd.DataFrame(data, columns=COLUMNS)

    # Calculate data
    def calculate_ratio_scores(self):
        # Calculates ratios for labels.
        ratios = (
            self.dataframe.replace('POSITIVE', 1)
            .replace('NEGATIVE', 0)
            .groupby('region','date')
            .agg(sentiment_ratio=('label', 'mean'))
        )

        return ratios

    # Format data before upload
    def format_ratios(self, ratios) -> dict:
        # Format ratios into a nice dictionary.
        ratios = ratios.to_dict()['sentiment_ratio']

        return [{'ratio': j, 'date': i[1], 'region': i[0]} for i, j in ratios.items()]
        
    # Upload data
    def upload_analysed_data(self, data):
        url = 'postgresql://news_db_itmr_user:YBIuNld32NRcYvCNQM1Md7MiYXRZ4Uem@dpg-cdjur3un6mpngruf3uag-a.oregon-postgres.render.com/news_db_itmr'
        engine = create_engine(
        url,
        echo=False,
        )
        meta = MetaData()
        meta.create_all(engine)

        table_data = Table(
            'geography', meta,
            Column('ratio', Float),
            Column('date', Date),
            Column('region', String)
        )
        conn = engine.connect()
        conn.execute(table_data.insert(), data)