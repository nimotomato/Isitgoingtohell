import psycopg2
from isitgoingtohell.utils import load_json

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

    def upload_data(self, filename, tablename="analysis"):
        data = load_json(filename)
        # for row in data:
        #     self.cur.execute(f""" insert into {tablename} values('{row}')) """)
        self.connection.commit()
        self.connection.close()


    def verify_data(self, filename):
        pass

    def delete_local_files(self, filename):
        pass

    def close_connection(self):
        self.connection.close()