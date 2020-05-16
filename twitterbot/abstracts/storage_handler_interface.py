import abc

import tweepy


class StorageHandlerInterface(metaclass=abc.ABCMeta):
    def __init__(self, path):
        self.FILEPATH = path

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'rate_tweet') and
                callable(subclass.rate_tweet) or
                NotImplemented)

    @abc.abstractmethod
    def store_tweet(self, tweet: tweepy.Status):
        raise NotImplementedError

    @abc.abstractmethod
    def export_tweets_as_jsons(self):
        raise NotImplementedError
