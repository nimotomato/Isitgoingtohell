import pandas as pd
from isitgoingtohell.data_management.db_management import Database as DB
from isitgoingtohell.utils import load_csv
from isitgoingtohell.scrapers.pipelines import REGIONS

TABLENAME = 'data'
class Statistics():
    def __init__(self):
        # Connect to database and get retreival methods.
        db = DB()
        columns = ['date','region','label']
        query = f'SELECT {",".join(columns)} FROM {TABLENAME} WHERE label is not Null'
        db.cur.execute(query)
        sentiment_data = db.cur.fetchall()
        db.close_connection(message=False)
        
        # Set up dataframe.
        self.df = pd.DataFrame(sentiment_data, columns=columns)

        # Load list of country codes corresponding to region.
        self.country_codes = load_csv("only_codes.csv")

    def calculate_ratio_scores(self) -> dict:
        groupings = ['region','date']
        ratios = (
            self.df.replace('POSITIVE', 1)
            .replace('NEGATIVE', 0)
            .groupby(groupings)
            .agg(sentiment_ratio=('label', 'mean'))
        )

        return ratios

    def format_ratios(self, ratios):
        ratios = ratios.to_dict()['sentiment_ratio']

        return [{'ratio': j, 'date': i[1], 'region': i[0]} for i, j in ratios.items()]