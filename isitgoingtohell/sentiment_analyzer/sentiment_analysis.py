from isitgoingtohell.utils import load_toml, load_json
from transformers import pipeline
import numpy as np

class Analyzer():
    def __init__(self):
        # load config
        config = load_toml("config.toml")

        # set up sentiment analysis model
        self.sentiment_analyser = pipeline(model=config["sentiment_analysis"]["model"])

    
    def analyze_json(self, filename="result.json"):
        raw_data = load_json(filename)

        # Store list of dictionaries
        j_list = []

        for row in raw_data:
            # Apply sentiment analysis on raw data
            analyzed_data = self.sentiment_analyser(row['text'])

            # Go through data from each headline/text-item and append to main list.
            for item in analyzed_data:
                item['text'] = row['text']
                item['date'] = row['time']
                item['region'] = row['region']
                item['score'] = np.round(item['score'], 4)
                j_list.append(item)
                
        return j_list          