import tweepy
import logging


class TweetListener(tweepy.StreamListener):
    def __init__(self, queue, selector, storage_handler=None):
        super().__init__()
        self.queue = queue
        self.selector = selector
        self.storage_handler = storage_handler

    def on_status(self, status):
        rating = self.selector.rate_tweet(status)
        if rating > 0.7:
            self.queue.put((-1 * rating, status))
        if self.storage_handler is not None:
            self.storage_handler.store_tweet(status)
        logging.info(status)

    def on_error(self, status_code):
        logging.warning('an error return by twitter, error code :'+status_code)

    def on_disconnect(self, notice):
        logging.warning(notice)

    def on_exception(self, exception):
        logging.critical(exception)

    def on_limit(self, track):
        logging.warning('a limit message was return by twitter, ' + track)
