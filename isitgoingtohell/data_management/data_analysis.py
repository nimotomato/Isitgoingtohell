import pandas as pd
from isitgoingtohell.data_management.db_management import DB
from isitgoingtohell.data_management.settings import tablename,columns


class Data_Analysis:
    def __init__(self):
        db = DB()
        data = db.get_all_data(tablename=tablename)
        self.df = pd.DataFrame(data, columns=columns)

class Dated_methods(Data_Analysis):      
    def __init__(self):
        super().__init__()

    def calculate_ratio_dated(self):
        groupings=['region','date']
        return self.calculate_ratio(groupings)

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

    def calculate_ratio(self, groupings: list) -> dict:
        # Calculates ratio sorted by selected columns in the list.
        ratio = (
            self.df.replace('POSITIVE', 1)
            .replace('NEGATIVE', 0)
            .replace('australia', 'oceania')
            .replace('latin_america', 'south america')
            .replace('us_and_canada', 'north america')
            .replace('middle_east', 'asia')
            .groupby(groupings)
            .agg(sentiment_ratio=('label', 'mean'))
            .sort_values(by=['date'])
        )
        dict = ratio.to_dict()
        return dict['sentiment_ratio']
    
    def populate_countries(self, country_codes, date_score_region, region):
        # Injects data for a region (date_score_region) into country codes within a region.
        # Needed for ISO-locations in graph 
        populated_countries = []

        for country in country_codes:
            if country['region'].lower() == region:
                for score in date_score_region:
                    if score['region'] == region:
                        populated_country = {}
                        populated_country['country_code'] = country['code']
                        populated_country['dated_region_score'] = score['score']
                        populated_country['date'] = score['date']
                        populated_country['region'] = score['region']
                        populated_countries.append(populated_country)
        return populated_countries 
    
    def populate_regions(self, country_codes, region_scores) -> list:
        # Runs populate_countries for all regions
        regions = [
        'africa',
        'asia',
        'europe',
        'oceania',
        'north america',
        'south america'
        ]

        populated_regions = []
        for region in regions:
            populated_regions.extend(self.populate_countries(country_codes, region_scores, region))

        return populated_regions

class Undated_methods(Data_Analysis):
    def __init__(self):
        super().__init__()

    def calculate_ratio_total(self):
        groupings=['region']
        return self.calculate_ratio(groupings)

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

    def calculate_ratio(self, groupings: list) -> dict:
        # Calculates ratio sorted by selected columns in the list.
        ratio = (
            self.df.replace('POSITIVE', 1)
            .replace('NEGATIVE', 0)
            .replace('australia', 'oceania')
            .replace('latin_america', 'south america')
            .replace('us_and_canada', 'north america')
            .replace('middle_east', 'asia')
            .groupby(groupings)
            .agg(sentiment_ratio=('label', 'mean'))
        )
        dict = ratio.to_dict()
        return dict['sentiment_ratio']

    def populate_countries(self, country_codes, region_score, region):
        # Injects data for a region (date_score_region) into country codes within a region.
        # Needed for ISO-locations in graph 
        populated_countries = []

        for country in country_codes:
            if country['region'].lower() == region:
                for score in region_score:
                    if score['region'] == region:
                        populated_country = {}
                        populated_country['country_code'] = country['code']
                        populated_country['region_score'] = score['score']
                        populated_country['region'] = score['region']
                        populated_countries.append(populated_country)
        return populated_countries 

    def populate_regions(self, country_codes, region_scores) -> list:
        # Runs populate_countries for all regions
        regions = [
        'africa',
        'asia',
        'europe',
        'oceania',
        'north america',
        'south america'
        ]

        populated_regions = []
        for region in regions:
            populated_regions.extend(self.populate_countries(country_codes, region_scores, region))

        return populated_regions