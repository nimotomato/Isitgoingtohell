import pandas as pd
from isitgoingtohell.data_management.db_management import DB
from isitgoingtohell.utils import load_csv, dicts_to_tuples
from datetime import date
REGIONS = [
    'africa',
    'asia',
    'europe',
    'oceania',
    'north america',
    'south america'
    ]
TABLENAME = 'data'

class Data_Analysis:
    def __init__(self):
        self.db = DB()
        # This data cannot be all data, change it to be data not uploaded into geography. 
        data = self.db.get_analysed_data(tablename=TABLENAME)
        columns = self.db.get_col_names_not_id(TABLENAME, 5)
        data_columns = columns.split(",")
        self.df = pd.DataFrame(data, columns=data_columns)
        self.country_codes = load_csv("only_codes.csv")

    def calculate_ratio(self, groupings: list) -> dict:
            # Calculates ratio sorted by selected columns in the list.
            ratio = (
                self.df.replace('POSITIVE', 1)
                .replace('NEGATIVE', 0)
                .groupby(groupings)
                .agg(sentiment_ratio=('label', 'mean'))
            )
            dict = ratio.to_dict()
            return dict['sentiment_ratio']
        
class Dated_methods(Data_Analysis):      
    def __init__(self):
        super().__init__()
        
    def calculate_ratio_dated(self):
        groupings=['region','date']
        return self.to_dict(self.calculate_ratio(groupings))

    def to_dict(self, ratio, not_null=False):
        list = []
        for i, j in ratio.items():
            if not_null:
                if j != 0:
                    item={}
                    item['region'] = i[0]
                    item['date'] = i[1]
                    item['score'] = j
                    list.append(item)
            else:
                item={}
                item['region'] = i[0]
                item['date'] = i[1]
                item['score'] = j
                list.append(item)

        return list
    
    def populate_countries(self, date_score_region, region):
        # Injects data for a region (date_score_region) into country codes within a region.
        # Needed for ISO-locations in graph 
        populated_countries = []

        for country in self.country_codes:
            if country['region'].lower() == region:
                for score in date_score_region:
                    if score['region'] == region:
                        populated_country = {}
                        populated_country['country_code'] = country['code']
                        populated_country['score'] = score['score']
                        populated_country['date'] = score['date']
                        populated_country['region'] = score['region']
                        populated_countries.append(populated_country)
        return populated_countries 
    
    def populate_regions(self, region_scores, regions=REGIONS) -> list:
        # Runs populate_countries for all regions

        populated_regions = []
        for region in regions:
            populated_regions.extend(self.populate_countries(region_scores, region))

        return populated_regions



class Undated_methods(Data_Analysis):
    def __init__(self):
        super().__init__()

    def calculate_ratio_total(self):
        groupings=['region']
        return self.to_dict(self.calculate_ratio(groupings))

    def to_dict(self, ratio, not_null=False):
        list = []
        for i, j in ratio.items():
            if not_null:
                if j != 0:
                    item={}
                    item['region'] = i
                    item['score'] = j
                    list.append(item)
            else:
                item={}
                item['region'] = i
                item['score'] = j
                list.append(item)

        return list

    def populate_countries(self, region_score, region):
        # Injects data for a region (date_score_region) into country codes within a region.
        # Needed for ISO-locations in graph 
        populated_countries = []

        for country in self.country_codes:
            if country['region'].lower() == region:
                for score in region_score:
                    if score['region'] == region:
                        populated_country = {}
                        populated_country['country_code'] = country['code']
                        populated_country['score'] = score['score']
                        populated_country['region'] = score['region']
                        populated_countries.append(populated_country)
        return populated_countries 

    def populate_regions(self, region_scores, regions=REGIONS) -> list:
        # Runs populate_countries for all regions
        populated_regions = []
        for region in regions:
            populated_regions.extend(self.populate_countries(region_scores, region))

        return populated_regions