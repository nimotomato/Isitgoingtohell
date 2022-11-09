# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class BbcScraperPipeline:
    def __init__(self):
        hostname = 'dpg-cdjur3un6mpngruf3uag-a.oregon-postgres.render.com'
        username = 'news_db_itmr_user'
        password = 'YBIuNld32NRcYvCNQM1Md7MiYXRZ4Uem'
        database = 'news_db_itmr'

        #create connection
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()
    
    def process_item(self, item, spider):
        #problematic when there is ' in text
        self.cur.execute(f""" select * from news where text = '{item['text']}' """)
        check_empty = self.cur.fetchone()

        if check_empty:
            spider.logger.warn("Item already in database.")
        else:
            try:
                # Define insert statement
                self.cur.execute(""" insert into news (link, text, datetime, region) values (%s,%s,%s,%s)""", (
                    item['text'],
                    item['time'],
                    item['region']
                ))
            except:
                self.connection.rollback()

            ## Execute insert of data into database
            self.connection.commit()
        return item
    

    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()