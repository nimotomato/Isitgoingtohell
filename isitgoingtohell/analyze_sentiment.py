import os
from typing import List

import pandas as pd
from transformers import pipeline


def analyze_sentiment(news: List[str], batch_size: int = 64) -> pd.DataFrame:
    """analyze sentiment"""
    sentiment_analyser = pipeline(model=os.environ["SENTIMENT_MODEL"])

    results = []
    for i in range(0, len(news), batch_size):
        results.extend(sentiment_analyser(news[i : i + batch_size]))

    return pd.DataFrame(results)
