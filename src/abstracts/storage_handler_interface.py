import abc


class StorageHandlerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'rate_tweet') and
                callable(subclass.rate_tweet) or
                NotImplemented)

    @abc.abstractmethod
    def store_tweet(self, tweet):
        raise NotImplementedError

    @abc.abstractmethod
    def export_tweets_as_jsons(self, path):
        raise NotImplementedError
