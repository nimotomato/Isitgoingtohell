# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class BbcScraperPipeline:
    def __init__(self):
        #hostname = 
        #username = 
        #password =
        #database = 

        #create connection
        # self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        ## Create cursor, used to execute commands
        #self.cur = self.connection.cursor()

        pass
    
    def process_item(self, item, spider):
        ## Check to see if text is already in database 
        # self.cur.execute("select * from quotes where content = %s", (item['text'],))
        # result = self.cur.fetchone()

        # ## If it is in DB, create log message
        # if result:
        #     spider.logger.warn("Item already in database: %s" % item['text'])


        # ## If text isn't in the DB, insert data
        # else:

            # ## Define insert statement
            # self.cur.execute(""" insert into DB_NAME (COL, COL, COL) values (%s,%s,%s)""", (
            #     item['link'],
            #     item['text'],
            #     item['time']
            # ))

            # ## Execute insert of data into database
            # self.connection.commit()
        # return item
        pass

    # def close_spider(self, spider):

    #     ## Close cursor & connection to database 
    #     self.cur.close()
    #     self.connection.close()