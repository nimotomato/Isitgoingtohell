import pandas as pd
from isitgoingtohell.data_management.db_management import Database as DB
from isitgoingtohell.utils import load_csv, stringify_list
from datetime import date
from isitgoingtohell.scrapers.pipelines import REGIONS

TABLENAME = 'data'

class Load_data():
    def __init__(self):
        # Connect to database and get retreival methods.
        db = DB()
        columns_list = db.get_column_names()

        # Get data that has not yet been analysed.
        columns_string = stringify_list(columns_list)
        condition = 'WHERE label is not Null'
        sentiment_data = db.get_data(columns_names=columns_string, condition=condition)
        db.close_connection(message=False)
        
        # Set up dataframe.
        self.df = pd.DataFrame(sentiment_data, columns=columns_list)

        # Load list of country codes corresponding to region.
        self.country_codes = load_csv("only_codes.csv")

    
class General_methods(Load_data):
    def __init__(self):
        super().__init__()

    def calculate_ratio_scores(self, groupings: list) -> dict:
        # Calculates negative sentiment/positive sentiment sorted by selected columns in the list.
        # Returns a dict where key = ('region', 'date'), value = 'score'.
        ratio = (
            self.df.replace('POSITIVE', 1)
            .replace('NEGATIVE', 0)
            .groupby(groupings)
            .agg(sentiment_ratio=('label', 'mean'))
        )
        dict = ratio.to_dict()
        return dict['sentiment_ratio']
    
    def sort_ratio_scores(self, ratio_scores, dated: bool, not_null=False):
    # Sorts output from calculate_ratio into a dictionary we can use. 
        list = []
        for i, j in ratio_scores.items():
            if not_null:
                if j != 0:
                    item={}
                    item['score'] = j
                    if dated:
                        item['date'] = i[1]
                        item['region'] = i[0]
                    else:
                        item['region'] = i
                    list.append(item)
            else:
                item={}
                item['score'] = j
                if dated:
                    item['date'] = i[1]
                    item['region'] = i[0]
                else:
                    item['region'] = i

                list.append(item)

        return list

    def sort_by_country_code(self, sorted_scores, region, dated=False):
        # Spreads data from specified region to each country code within region.
        sorted_data = []

        for country in self.country_codes:
            if country['region'].lower() == region:
                for score in sorted_scores:
                    if score['region'] == region:
                        item = {}
                        item['country_code'] = country['code']
                        item['score'] = score['score']
                        if dated:
                            item['date'] = score['date']
                        item['region'] = score['region']
                        sorted_data.append(item)

        return sorted_data 


class Dated_methods(General_methods):
    def __init__(self):
        super().__init__()
    
    def calculate_ratio_dated(self)->list[dict]:
        # Returns a list of dict data sorted by region and date.
        groupings = ['region','date']
        ratio_scores = self.calculate_ratio_scores(groupings)
        return ratio_scores

    def pre_sort_scores_dated(self, ratio):
        return self.sort_ratio_scores(ratio, dated=True)

    def map_all_regions_dated(self, presorted_scores_dated, regions=REGIONS) -> list:
        # Sorts scores for all regions.
        populated_regions = []
        for region in regions:
            populated_regions.extend(self.sort_by_country_code(presorted_scores_dated, region, dated=True))

        return populated_regions


class Undated_methods(General_methods):
    def __init__(self):
        super().__init__()

    def calculate_ratio_undated(self)->dict:
        # Returns a dict of data sorted by region.
        # TO IMPLEMENT: make this use already calculated data in table geography to save time
        groupings = ['region']
        return self.calculate_ratio_scores(groupings)

    def pre_sort_scores_undated(self, ratio):
        return self.sort_ratio_scores(ratio, dated=False)

    def map_all_regions_undated(self, ratio_scores, regions=REGIONS) -> list:
        # Maps regional scores to all countries. 
        populated_regions = []
        for region in regions:
            populated_regions.extend(self.sort_by_country_code(ratio_scores, region))

        return populated_regions

    def add_metadata(self, data: list[dict], database_object) -> list[dict]:
        # This contains final data for upload.
        calculation_date = str(date.today().isoformat())

        new_order = []
        for item in data:
            new_item = {}
            new_item['region'] = item['region']
            new_item['score'] = item['score']
            new_item['calculation_date'] = calculation_date
            condition =  f"WHERE region = '{item['region']}'"
            new_item['number_of_labels'] = database_object.get_item_count('score', tablename=TABLENAME, condition=condition)[0]
            new_order.append(new_item)
        
        return new_order