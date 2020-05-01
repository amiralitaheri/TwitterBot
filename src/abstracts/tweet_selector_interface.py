import abc


class TweetSelectorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'rate_tweet') and
                callable(subclass.rate_tweet) or
                NotImplemented)

    @abc.abstractmethod
    def rate_tweet(self, status):
        raise NotImplementedError
