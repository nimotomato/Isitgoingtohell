from isitgoingtohell.utils import load_toml, load_json
from isitgoingtohell.db_management.db_management import DB
from transformers import pipeline
import numpy as np
from psycopg2 import errorcodes, errors

class Analyzer():
    def __init__(self):
        # load config
        config = load_toml("config.toml")

        # set up sentiment analysis model
        self.sentiment_analyser = pipeline(model=config["sentiment_analysis"]["model"])

    
    def analyze_json(self, raw_json_data):
        # Filename dictates output filename.
        # Non_duplicates ignores headlines already in database. 

        # Store list of dictionaries
        analyzed_data = []

        db = DB()
        db.cur.execute(f""" select headline from data """)
        # Create list of all headlines in database. Probably doesn't scale great, but is quick.
        check_empty = [i[0] for i in db.cur.fetchall()]

        for row in raw_json_data:
            # Check for duplicates in DB
            if row['headline'] in check_empty:
                print("Item already in database.")
            else:
                # Apply sentiment analysis on raw data
                analyzed_data_nuggets = self.sentiment_analyser(row['headline'])
                # Go through data from each headline/text-item and append to main list.
                for item in analyzed_data_nuggets:
                        analyzed_data.append(self.clean_data_nugget(row, item))

        return analyzed_data


    def clean_data_nugget(self, row, item):
        # Necessary for analyze_json method.
        # Cleans analyzed data.
        output = {}
        output['headline'] = row['headline']
        output['date'] = row['date']
        output['region'] = row['region']
        output['label'] = item['label']
        output['score'] = np.round(item['score'], 4)

        return output