import random

from abstracts.tweet_selector_interface import TweetSelectorInterface


# RandomSelector will rate tweets randomly
class RandomSelector(TweetSelectorInterface):
    def rate_tweet(self, status):
        return random.random()
