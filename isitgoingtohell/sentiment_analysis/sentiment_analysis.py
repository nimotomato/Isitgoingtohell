from isitgoingtohell.utils import load_toml, load_json
from isitgoingtohell.data_management.db_management import DB
from transformers import pipeline
import numpy as np

class Analyser():
    def __init__(self):
        # load config
        config = load_toml("config.toml")

        # set up sentiment analysis model
        self.sentiment_analyser = pipeline(model=config["sentiment_analysis"]["model"])

    def analyze_data(self, raw_data):
        # Analyses a list of dicts
        analyzed_data = []
        for scraped_data_nugget in raw_data:
            # Apply sentiment analysis on raw data
            analyzed_data_nuggets = self.sentiment_analyser(scraped_data_nugget['headline'])
            # Go through scraped data, analyze each headline and append to main list.
            for analyzed_data_nugget in analyzed_data_nuggets:
                    analyzed_data.append(self.clean_data_nuggets(scraped_data_nugget, analyzed_data_nugget))

        return analyzed_data

    def get_headlines(self):
        db = DB()
        return db.get_col_data('data', 'headline', outbound=True)

    def clean_data_nuggets(self, scraped_data_nugget, analyzed_data_nugget):
        # Necessary for analyze_json method.
        # Cleans analyzed data.
        output = {}
        output['headline'] = scraped_data_nugget['headline']
        output['date'] = scraped_data_nugget['date']
        output['region'] = scraped_data_nugget['region']
        output['label'] = analyzed_data_nugget['label']
        output['score'] = np.round(analyzed_data_nugget['score'], 4)

        return output