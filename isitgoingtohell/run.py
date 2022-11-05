# from isitgoingtohell.sentiment_analysis.sentiment_analyser import SentimentAnalyser
from transformers import pipeline

from isitgoingtohell.utils import load_toml


def main():

    # load config
    config = load_toml("config.toml")

    # set up sentiment analysis model
    sentiment_analyser = pipeline(model=config["sentiment_analysis"]["model"])

    # some random news
    news = [
        """TikTok influencer cleans people's homes for free
    TikTok influencer cleans people's homes for free

    Auri Katariina, a cleaner from Finland, began posting videos on social media which became an instant hit. People started reaching out to her for help and she now cleans homes around the world for free.

    Auri's videos get millions of views and the BBC went to meet her on a recent trip to the United Kingdom."""
    ]

    # get sentiment
    print(sentiment_analyser(news))


if __name__ == "__main__":
    main()
