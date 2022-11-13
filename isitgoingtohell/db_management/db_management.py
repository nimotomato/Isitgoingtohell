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
        args = self.mogrify_data(data)

        self.cur.execute(f"""insert into {tablename} values """ + (args))

        self.connection.commit()
        self.connection.close()


    def mogrify_data(self, data):
        # Turn json data into a single query string
        _values = []

        # Mogrify method nees list of tuples. We shall provide.
        for row in data:
            _values.append(tuple(row.values()))

        value_string = ','.join(self.cur.mogrify("(%s,%s,%s,%s,%s)", row).decode('utf-8') for row in _values)

        return value_string


    def verify_data(self, filename="result.json", tablename="data"):
        self.cur.execute(f""" select text from {tablename}) """)

        bool = True
        error_counter = 0

        # Compare data in local file to data in database. Count errors.
        for row in filename:
            if row['text'] not in self.cur.fetchall():
                print(f"Item text: {row['text']} was not found in {tablename}")
                bool = False
                error_counter += 1

        print(f"Data verification completed. {str(error_counter)} errors encountered. ")
        return bool


    def delete_local_file(self, file_path):
        print("Cleanup initiated...")
        # Verify that the file exists.
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} deleted. ")
            return True

        print(f"{file_path} does not exist. ")
        return False


    def close_connection(self):
        self.connection.close()