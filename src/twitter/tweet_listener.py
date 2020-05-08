import logging

import tweepy

from src.utils.status_rate_wrapper import StatusRateWrapper


class TweetListener(tweepy.StreamListener):
    def __init__(self, queue, selector, storage_handler=None):
        super().__init__()
        self.queue = queue
        self.selector = selector
        self.storage_handler = storage_handler

    def on_status(self, status):
        rating = self.selector.rate_tweet(status)  # get rating from selector
        if rating > 0.7:  # only add tweets with rating above 0.7
            # (-1 * rating) because python PQ uses min-heap(min value will pop first)
            wrapper = StatusRateWrapper()
            wrapper.status = status
            wrapper.rate = -1 * rating
            self.queue.put(wrapper)
        if self.storage_handler is not None:
            self.storage_handler.store_tweet(status)  # save tweets
        logging.info(status)

    def on_error(self, status_code):
        logging.warning('an error return by twitter, error code :' + status_code)

    def on_disconnect(self, notice):
        logging.warning(notice)

    def on_exception(self, exception):
        logging.critical(exception)

    def on_limit(self, track):
        logging.warning('a limit message was return by twitter, ' + track)
