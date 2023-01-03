import pandas as pd
from transformers import pipeline


def analyze_sentiment(news, batch_size=64):
    # TODO CHANGE THIS MODEL?
    sentiment_analyser = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

    results = []
    for i in range(0, len(news), batch_size):
        results.extend(sentiment_analyser(news[i : i + batch_size]))

    return pd.DataFrame(results)
