import psycopg2
from isitgoingtohell.utils import load_json, dicts_to_tuples, tuple_to_dict
import os
import pandas as pd
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION

TABLENAME = 'data'
class DB():
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
    
    def get_item_count(self, column, table, condition):
        query = f"SELECT COUNT({column}) FROM {table} WHERE {condition}"
        self.cur.execute(f"""{query} """)
        return self.cur.fetchone()

    def upload_data_postgres_mogrify(self, mogrified_data, number_of_columns: int, tablename=TABLENAME):
        # Insert the goodies to db. Cannot deal with duplicate data...
        columns = self.get_col_names_not_id(tablename, number_of_columns)
        query = f"insert into {tablename} ({columns}) values {mogrified_data}"
        self.cur.execute(query)

        self.connection.commit()

    def upload_data_postgres(self, data, number_of_columns: int, tablename=TABLENAME):
        columns = self.get_col_names_not_id(tablename, number_of_columns)
        ordered_columns = self.order_column_by_values(columns, data)
        ordered_string = ",".join(ordered_columns)

        data = dicts_to_tuples(data)
        # Insert the goodies to db.
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

    def get_unanalysed_data(self, tablename=TABLENAME):
        query=f"SELECT headline,date,region,label,score FROM {tablename} WHERE label is Null"
        self.cur.execute(query)
        return self.cur.fetchall()

    def upload_analysed_data(self, data, tablename=TABLENAME):
        for item in data:
            query = f"UPDATE {tablename} SET label = '{item['label']}', score = '{item['score']}' WHERE headline = '{item['headline']}'"
            self.cur.execute(query)

        self.connection.commit()

    def order_column_by_values(self, columns, data) -> list:
        # Implement a method that aligns the order of column and value 
        # Warning: Keys and cols have to match.
        dict_keys = data[0].keys()
        ordered_keys = [key for key in dict_keys if key in columns]
        return ordered_keys

    def mogrify_data(self, data, columns):
        # Turn list of dicts data into a single query string
        values = []

        # Mogrify method needs list of tuples. We shall provide.
        for row in data:
            values.append(tuple(row.values()))
        x = 0
        format = []
        while x < columns:
            format.append('%s')
            x+=1
        format = ','.join(format)    

        value_string = ','.join(self.cur.mogrify(f"({format})", row).decode('utf-8') for row in values)

        return value_string

    def get_col_names_not_id(self, tablename, number_of_columns: int, outbound=False) -> str:
        # Get names from col except for id
        self.cur.execute(f"""select * from {tablename}""")

        # Gets all col names except for id, stopping at columns
        column_names_list = [col[0] for col in self.cur.description if col[0] != 'id']
        column_names_string = ",".join(column_names_list[:number_of_columns])

        if outbound:
            self.close_connection(message=False)

        return column_names_string

    def get_col_data(self, tablename, column_name, outbound=False) -> list:
        # Create list of all headlines in database. Probably doesn't scale great, but is quick.
        self.cur.execute(f""" select {column_name} from {tablename} """)
        col_names = [i[0] for i in self.cur.fetchall()]

        if outbound:
            self.close_connection(message=False)

        return col_names

    def remove_duplicates_batch(self, data, tablename=TABLENAME):
        headlines = [("headline = " + "'" +data['headline']+ "'") for data in data]
        condition = " OR ".join(headlines)
        query = f" SELECT headline FROM {tablename} WHERE {condition} "
        self.cur.execute(query)
        duplicates = [headlines[0] for headlines in self.cur.fetchall()]
        uniques = [item for item in data if item['headline'] not in duplicates]
        return uniques

    def remove_duplicates_one_by_one(self, data, tablename=TABLENAME):
        #Goes through each item in data and checks if it is already in database. Safe, but slow.
        items_not_in_database = [item for item in data if not self.in_database(item)]
        return items_not_in_database

    def in_database(self, data: dict, tablename=TABLENAME) -> bool:
        # Check if item exists in database.
        query = f" SELECT headline FROM {tablename} WHERE headline = '{data['headline']}' "
        self.cur.execute(query)
        if self.cur.fetchone():
            return True
        return False

    # def verify_data(self, filename="cache.json", tablename="data"):
    #     # Verify all data from local file has been uploaded to database. Scales poorly, gets all data every time.
    #     self.cur.execute(f""" select headline from {tablename} """)

    #     bool = True
    #     error_counter = 0

    #     all_headlines = [text[0] for text in self.cur.fetchall()]

    #     # Compare data in local file to data in database. Count errors.
    #     for row in filename:
    #         if row['headline'] not in all_headlines:
    #             print(f"Item text: {row['headline']} was not found in {tablename}")
    #             bool = False
    #             error_counter += 1

    #     print(f"Data verification completed. {str(error_counter)} errors encountered. ")

    #     return bool
        
    def get_geography_data(self):
        raw_data = self.get_all_data("geography")
        data = []
        for x in raw_data:
            d = {}
            d['country_code'] = x[0]
            d['dated_region_score'] = x[1]
            d['date'] = x[2]
            d['region'] = x[3]
            data.append(d)
        return data

    def get_geography_data_undated(self):
        raw_data = self.get_all_data("geograpy_undated")
        data = []
        for x in raw_data:
            d = {}
            d['country_code'] = x[0]
            d['region'] = x[1]
            d['score'] = x[2]
            d['calculation_date'] = x[3]
            d['number_of_labels'] = x[4]
            data.append(d)
        return data

    def get_all_data(self, tablename:str):
        self.cur.execute(f""" select * from {tablename} """)
        return self.cur.fetchall()

    def get_analysed_data(self, tablename:str):
        query=f"SELECT headline,date,region,label,score FROM {tablename} WHERE label is not Null"
        self.cur.execute(query)
        return self.cur.fetchall()

    def close_connection(self, message=True):
        self.cur.close()
        self.connection.close()
        if message:
            print("Connection closed. ")