import random

from src.abstracts.tweet_selector_interface import TweetSelectorInterface


class RandomSelector(TweetSelectorInterface):
    def rate_tweet(self, status):
        return random.random()
