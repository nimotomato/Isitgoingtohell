# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from isitgoingtohell.utils import load_toml
from transformers import pipeline
import numpy as np
from scrapy.exceptions import DropItem


filename = 'items'

class DuplicatesPipeline:

    def __init__(self):
        # Keep track of seen items
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Text is unique in database, so item is identified by text
        if adapter['text'] in self.ids_seen:
            raise DropItem("Duplicate item found: %r" % item)
        else:
            self.ids_seen.add(adapter['text'])
            return item



class CompositePipeline:
    # This pipeline can do it all; connect to database, analyze data with sentiment analyzer and upload data. It is however very slow.
    def __init__(self):
        hostname = 'dpg-cdjur3un6mpngruf3uag-a.oregon-postgres.render.com'
        username = 'news_db_itmr_user'
        password = 'YBIuNld32NRcYvCNQM1Md7MiYXRZ4Uem'
        database = 'news_db_itmr'

        #create connection
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        # load config
        config = load_toml("config.toml")

        # set up sentiment analysis model
        self.sentiment_analyser = pipeline(model=config["sentiment_analysis"]["model"])
    
    def process_item(self, item, spider):
        self.cur.execute(f""" select * from news where text = '{item['text']}' """)
        check_empty = self.cur.fetchone()

        if check_empty:
            spider.logger.warn("Item already in database.")
        else:
            try:
                # Define insert statements        

                # News table 
                self.cur.execute(""" insert into news (text, datetime, region) values (%s,%s,%s)""", (
                    item['text'],
                    item['time'],
                    item['region']
                ))
                # Sentiment_analysis table
                analysis = self.sentiment_analyser(item['text'])[0]

                item['label'] = analysis['label']
                item['score'] = np.round(analysis['score'],4)

                self.cur.execute(""" insert into analysis (sentiment, confidence, text) values (%s,%s,%s)""", (
                    item['label'], 
                    item['score'], 
                    item['text']
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