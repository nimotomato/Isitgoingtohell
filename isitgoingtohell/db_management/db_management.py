import psycopg2
from isitgoingtohell.utils import load_json
import os

class DB():
    def __init__(self):
        hostname = 'dpg-cdjur3un6mpngruf3uag-a.oregon-postgres.render.com'
        username = 'news_db_itmr_user'
        password = 'YBIuNld32NRcYvCNQM1Md7MiYXRZ4Uem'
        database = 'news_db_itmr'

        #create connection
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()


    def upload_data_postgres(self, data, tablename="data"):

        # Get all data from json data as single string
        args = self.mogrify_data(data)

        # Get table col names
        tables = self.get_col_names_not_id(tablename)

        # Insert the goodies to db.
        query = f"insert into {tablename} ({tables}) values"
        self.cur.execute(f"""{query} """ + (args))
        print(f"Uploaded {len(data)} item(s).")
        self.connection.commit()


    def mogrify_data(self, data):
        # Turn json data into a single query string
        _values = []

        # Mogrify method nees list of tuples. We shall provide.
        for row in data:
            _values.append(tuple(row.values()))

        value_string = ','.join(self.cur.mogrify("(%s,%s,%s,%s,%s)", row).decode('utf-8') for row in _values)

        return value_string


    def get_col_names_not_id(self, tablename):
        # Get names from col except for id
        self.cur.execute(f"""select * from {tablename}""")

        # Gets all col names except for id
        column_names_list = [col[0] for col in self.cur.description if col[0] != 'id']
        column_names_string = ",".join(column_names_list)

        return column_names_string


    def verify_data(self, filename="cache.json", tablename="data"):
        # Verify all data from local file has been uploaded to database.
        self.cur.execute(f""" select headline from {tablename} """)

        bool = True
        error_counter = 0

        all_headlines = [text[0] for text in self.cur.fetchall()]

        # Compare data in local file to data in database. Count errors.
        for row in filename:
            if row['headline'] not in all_headlines:
                print(f"Item text: {row['headline']} was not found in {tablename}")
                bool = False
                error_counter += 1

        print(f"Data verification completed. {str(error_counter)} errors encountered. ")

        return bool


    def close_connection(self, message=True):
        self.cur.close()
        self.connection.close()
        if message:
            print("Connection closed. ")