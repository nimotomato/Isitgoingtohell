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

    def calculate_ratio_scores(self):
        # Calculates ratios for labels.
        groupings = ['region','date']
        ratios = (
            self.df.replace('POSITIVE', 1)
            .replace('NEGATIVE', 0)
            .groupby(groupings)
            .agg(sentiment_ratio=('label', 'mean'))
        )

        return ratios

    def format_ratios(self, ratios) -> dict:
        # Format ratios into a nice dictionary.
        ratios = ratios.to_dict()['sentiment_ratio']

        return [{'ratio': j, 'date': i[1], 'region': i[0]} for i, j in ratios.items()]
        
    def add_country_codes(self, formated_ratios, region):
        # Add country codes for a region.
        ratios_with_country_codes = []

        for country in self.country_codes:
            if country['region'].lower() == region:
                for score in formated_ratios:
                    if score['region'] == region:
                        item = {}
                        item['country_code'] = country['code']
                        item['score'] = score['score']
                        item['date'] = score['date']
                        item['region'] = score['region']
                        ratios_with_country_codes.append(item)

        return ratios_with_country_codes 

    def add_codes_all_regions(self, presorted_scores_dated, regions=REGIONS) -> list:
        # Adds country codes for all regions.
        regions = []
        for region in regions:
            regions.extend(self.sort_by_country_code(presorted_scores_dated, region))

        return regions