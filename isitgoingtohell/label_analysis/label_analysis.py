import pandas as pd
from isitgoingtohell.data_management.db_management import Database as DB
from isitgoingtohell.utils import load_csv, stringify_list, tuple_to_dict
from datetime import date
from isitgoingtohell.scrapers.pipelines import REGIONS

TABLENAME = 'data'
GEO_UNDATED = 'geography_undated'

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
        ratio = (
            self.df.replace('POSITIVE', 1)
            .replace('NEGATIVE', 0)
            .groupby(groupings)
            .agg(sentiment_ratio=('label', 'mean'))
        )
        dict = ratio.to_dict()
        return dict['sentiment_ratio']

    def format_ratios(self, ratios):
        return [{'ratio': j, 'date': i[1], 'region': i[0]} for i, j in ratios.items()]
        
# class General_methods(Load_data):
#     def __init__(self):
#         super().__init__()

#     def calculate_ratio_scores(self, groupings: list) -> dict:
#         # Calculates negative sentiment/positive sentiment sorted by selected columns in the list.
#         # Returns a dict where key = ('region', 'date'), value = 'score'.
#         ratio = (
#             self.df.replace('POSITIVE', 1)
#             .replace('NEGATIVE', 0)
#             .groupby(groupings)
#             .agg(sentiment_ratio=('label', 'mean'))
#         )
#         dict = ratio.to_dict()
#         return dict['sentiment_ratio']
    
#     def sort_ratio_scores(self, ratio_scores, dated: bool, not_null=False):
#     # Sorts output from calculate_ratio into a dictionary we can use. 
#         list = []
#         for i, j in ratio_scores.items():
#             if not_null:
#                 if j != 0:
#                     item={}
#                     item['score'] = j
#                     if dated:
#                         item['date'] = i[1]
#                         item['region'] = i[0]
#                     else:
#                         item['region'] = i
#                     list.append(item)
#             else:
#                 item={}
#                 item['score'] = j
#                 if dated:
#                     item['date'] = i[1]
#                     item['region'] = i[0]
#                 else:
#                     item['region'] = i

#                 list.append(item)

#         return list

#     def sort_by_country_code(self, sorted_scores, region, dated=False):
#         # Spreads data from specified region to each country code within region.
#         sorted_data = []

#         for country in self.country_codes:
#             if country['region'].lower() == region:
#                 for score in sorted_scores:
#                     if score['region'] == region:
#                         item = {}
#                         item['country_code'] = country['code']
#                         item['score'] = score['score']
#                         if dated:
#                             item['date'] = score['date']
#                         item['region'] = score['region']
#                         sorted_data.append(item)

#         return sorted_data 


# class Dated_methods(General_methods):
#     def __init__(self):
#         super().__init__()
    
#     def calculate_ratio_dated(self)->list[dict]:
#         # Returns a list of dict data sorted by region and date.
#         groupings = ['region','date']
#         ratio_scores = self.calculate_ratio_scores(groupings)
#         return ratio_scores

#     def pre_sort_scores_dated(self, ratio):
#         return self.sort_ratio_scores(ratio, dated=True)

#     def map_all_regions_dated(self, presorted_scores_dated, regions=REGIONS) -> list:
#         # Sorts scores for all regions.
#         populated_regions = []
#         for region in regions:
#             populated_regions.extend(self.sort_by_country_code(presorted_scores_dated, region, dated=True))

#         return populated_regions


# class Undated_methods(General_methods):
#     def __init__(self):
#         super().__init__()

#         db = DB()
#         self.columns_list = db.get_column_names()

#         # Get data that has not yet been analysed. 
#         columns_string = stringify_list(self.columns_list)
#         condition = 'WHERE used is false'
#         unused_labels = db.get_data(columns_names=columns_string, condition=condition)
#         keys = db.get_column_names(tablename=TABLENAME)
#         self.unused_data = [tuple_to_dict(row, keys) for row in unused_labels]

#         # Get data that has been analysed.
#         selection = 'distinct * '
#         condition = 'order by calculation_date desc, region desc limit 6'
#         previous_data = db.get_data(columns_names=selection, tablename=GEO_UNDATED, condition=condition)
#         keys = db.get_column_names(tablename=GEO_UNDATED)
#         self.used_ratios = [tuple_to_dict(item,keys) for item in previous_data]

#         db.close_connection(message=False)

#     def calculate_ratio_undated(self):
#         unused_df = pd.DataFrame(self.unused_data, columns=self.columns_list)
#         groupings = ['region']
#         ratio = (
#             unused_df.replace('POSITIVE', 1)
#             .replace('NEGATIVE', 0)
#             .groupby(groupings)
#             .agg(sentiment_ratio=('label', 'mean'))
#             )
#         return ratio.to_dict()['sentiment_ratio']
    
#     def format_ratios(self, ratios):
#         return [{'score': j, 'region': i} for i, j in ratios.items()]

#     def add_metadata(self, formated_unused_ratios):
#         db=DB()
#         unused_data_ordered = []
#         calculation_date = str(date.today().isoformat())
#         for item in formated_unused_ratios:
#             new_item = {}
#             new_item['region'] = item['region']
#             new_item['score'] = item['score']
#             new_item['calculation_date'] = calculation_date
#             condition = f"WHERE region = '{item['region']}' AND used = false"
#             new_item['number_of_labels'] = db.get_item_count(column='label', tablename=TABLENAME, condition=condition)[0]
#             unused_data_ordered.append(new_item)
#         db.close_connection(message=False)
#         return unused_data_ordered
    
#     def calculate_new_mean(self, used_ratios, formated_unused_ratios):
#         new_ratios=[]
#         for used_data in used_ratios:
#             for unused_data in formated_unused_ratios:
#                 if used_data['region'] == unused_data['region']:
#                     new_item={}
#                     new_item['region']=used_data['region']
#                     score = (unused_data['score']*unused_data['number_of_labels'])+(used_data['score']*used_data['number_of_labels'])
#                     count= unused_data['number_of_labels']+used_data['number_of_labels']
#                     new_item['score']=score/count
#                     new_ratios.append(new_item)
#         return new_ratios

#     def update_used_data(self):
#         db = DB()
#         query = "update data set used = true where used = false"
#         db.cur.execute(query)
#         db.connection.commit()
#         db.close_connection(message=False)
