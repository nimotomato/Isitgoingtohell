import psycopg2
from isitgoingtohell.utils import load_json, stringify_list, dicts_to_tuples, list_tuple_to_dict, tuple_to_dict, number_of_keys
import os
import pandas as pd
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
from datetime import date
from isitgoingtohell import utils

TABLENAME = 'data'

class Database():
# Manage Connection
    def __init__(self):
        hostname = 'dpg-cdjur3un6mpngruf3uag-a.oregon-postgres.render.com'
        username = 'news_db_itmr_user'
        password = 'YBIuNld32NRcYvCNQM1Md7MiYXRZ4Uem'
        database = 'news_db_itmr'
        self.UniqueViolation = errors.lookup('23505')
        #create connection
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

    def close_connection(self, message=True):
        self.cur.close()
        self.connection.close()
        if message:
            print("Connection closed. ")


# Retrieve data
    def get_data(self, columns_names='*', tablename=TABLENAME, condition='') -> list[tuple]:
        # Input columns or condition as single string.
        # Include WHERE for condition.
        query = f" SELECT {columns_names} FROM {tablename} {condition}"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_item_count(self, column, tablename=TABLENAME, condition=''):
        # Input columns as single string, incluiding WHERE.
        query = f"SELECT COUNT({column}) FROM {tablename} {condition}"
        self.cur.execute(query)
        return self.cur.fetchone()

    def get_columns(self, include_id=False, tablename=TABLENAME) -> list:
        query = f"SELECT * FROM {tablename} LIMIT 1"
        self.cur.execute(query)
        if include_id:
            column_names = [col[0] for col in self.cur.description]
            return column_names
        else:
            column_names = [col[0] for col in self.cur.description if col[0] != 'id']
            return column_names

    def get_column_count(self, include_id=False, tablename=TABLENAME) -> int:
        return len(self.get_columns(include_id, tablename))

    def get_column_names(self, include_id=False, tablename=TABLENAME) -> list:
        # Get names from desired substring of columns.
        column_names = self.get_columns(include_id, tablename)
        return column_names[:len(column_names)]
        
    def in_database(self, data: dict, tablename=TABLENAME) -> bool:
        query = f" SELECT headline FROM {tablename} WHERE headline = '{data['headline']}' "
        self.cur.execute(query)
        if self.cur.fetchone():
            return True
        return False
    
    def get_unanalysed_data(self, tablename=TABLENAME):
        condition = "WHERE label is Null"
        column_names = self.get_column_names()
        column_string = stringify_list(column_names)
        data_tuples = self.get_data(column_string, tablename, condition)
        return list_tuple_to_dict(data_tuples, column_names)

    def get_geography_data(self, dated=False):
        if dated:
            tablename = 'geography'
        else:
            tablename = 'geography_undated'

        geo_data = self.get_data(tablename=tablename)
        sorted_geo_data = self.sort_geo_data(geo_data, dated=dated)

        return sorted_geo_data

#Upload data
    def insert_data(self, data: str, tablename=TABLENAME, columns_names='*', condition=''):
        # Input columns or condition as single string.
        # Include WHERE for condition.
        query = f"INSERT INTO {tablename} ({columns_names}) VALUES {data} {condition}"
        self.cur.execute(query)

    def insert_batch(self, mogrified_data: str, column_names: list, tablename=TABLENAME):
        # WARNING: Cannot deal with duplicate data.
        columns_string = ",".join(column_names)
 
        self.insert_data(mogrified_data, tablename, columns_string)

        self.connection.commit()

    def insert_series(self, data: list[dict], number_of_columns: int, tablename=TABLENAME):
        columns = self.get_column_names(tablename, number_of_columns)
        ordered_columns = self.order_column_by_keys(columns, data)
        ordered_string = ",".join(ordered_columns)
        data = dicts_to_tuples(data)
        
        counter = 0
        for nugget in data:
            headline = nugget[0].replace("'", "")    
            nugget = (headline,*nugget[1:])
            query = f"INSERT INTO {tablename} ({ordered_string}) VALUES {nugget}"
            try:
                self.cur.execute(query)
                print(f"Uploaded {nugget}.")
                counter += 1
            except errors.lookup(UNIQUE_VIOLATION) as e:
                print(f"{e}")
                self.connection.rollback()
        print(f"Uploaded {counter} item(s).")

        self.connection.commit()

    def update_one(self, data: list[dict], condition: str, tablename=TABLENAME):
        # Updates one.
        query = f"UPDATE {tablename} {condition}"
        self.cur.execute(query)

    def upload_analysed_data(self, data: list[dict]):
        for item in data:
            condition = f"SET label = '{item['label']}', score = '{item['score']}' WHERE headline = '{item['headline']}'"
            self.update_one(data, condition)

        self.connection.commit()

    def upload_geography_data(self, mogrified_data: str, dated=False):
        if dated:
            tablename='geography'
        else:
            tablename='geography_undated'
        number_of_columns = self.get_column_count(tablename=tablename)
        self.insert_batch(mogrified_data, number_of_columns=number_of_columns, tablename=tablename)
        self.connection.commit()

# Modify data
    def mogrify_data(self, data: list[dict], number_of_columns: int) -> str:
        # Turn list of dicts data into a single query string
        ## Mogrify method needs list of tuples. We shall provide.
        values = dicts_to_tuples(data)

        format = self.string_format(number_of_columns)    

        value_string = ','.join(self.cur.mogrify(f"({format})", row).decode('utf-8') for row in values)

        return value_string

    def remove_duplicates_batch(self, data: list[dict], tablename=TABLENAME)->list:
        # Probably specify name on these
        headlines = [("headline = " + "'" +data['headline']+ "'") for data in data]
        condition = " OR ".join(headlines)
        query = f" SELECT headline FROM {tablename} WHERE {condition} "
        self.cur.execute(query)
        duplicates = [headlines[0] for headlines in self.cur.fetchall()]
        uniques = [item for item in data if item['headline'] not in duplicates]
        return uniques
        
    def remove_duplicate(self, data: list[dict], tablename=TABLENAME):
        #Goes through each item in data and checks if it is already in database. Safe, but slow.
        items_not_in_database = [item for item in data if not self.in_database(item)]
        return items_not_in_database
    
    def string_format(self, number_of_columns:int) -> str:
        # Takes number of columns and strings together '%s'.
        x = 0
        format = []
        while x < number_of_columns:
            format.append('%s')
            x+=1
        return ','.join(format) 

    def in_database(self, data: dict, tablename=TABLENAME) -> bool:
        # Check if item exists in database.
        query = f" SELECT headline FROM {tablename} WHERE headline = '{data['headline']}' "
        self.cur.execute(query)
        if self.cur.fetchone():
            return True
        return False

    def order_column_by_keys(self, columns: list, data: dict) -> list:
        # Changes order if colums to match the keys of a dictionary. 
        # WARNING: Keys and columns have to match namewise.
        dict_keys = data.keys()
        ordered_keys = [key for key in dict_keys if key in columns]
        return ordered_keys

    def sort_geo_data(self, unsorted_data, dated=False) -> list[dict]:
        data = []
        for item in unsorted_data:
            new_order = {}
            if dated:
                new_order['country_code'] = item[0]
                new_order['score'] = item[1]
                new_order['date'] = item[2]
                new_order['region'] = item[3]
            else:
                new_order['country_code'] = item[0]
                new_order['region'] = item[1]
                new_order['score'] = item[2]
                new_order['calculation_date'] = item[3]
                new_order['number_of_labels'] = item[4]
            data.append(new_order)
        return data
