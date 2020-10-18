import logging
import threading
import time
from queue import Queue

import tweepy

from twitterbot.abstracts.storage_handler_interface import StorageHandlerInterface
from twitterbot.abstracts.tweet_selector_interface import TweetSelectorInterface
from twitterbot.telegram.telegram import Telegram
from twitterbot.utils.config import Config


class TweetListener(tweepy.StreamListener):
    def __init__(self, selector: TweetSelectorInterface, api,
                 storage_handler: StorageHandlerInterface = None):
        super().__init__()
        self.selector = selector
        self.storage_handler = storage_handler
        self.fifo = Queue()
        self.executor = Executor(self.fifo, selector, storage_handler, api)

    def on_status(self, status):
        self.fifo.put_nowait(status)

    def on_error(self, status_code):
        logging.error('an error return by twitter, error code :' + str(status_code))

    def on_connect(self):
        self.executor.start()

    def on_disconnect(self, notice):
        logging.warning(notice)
        self.executor.killer = True
        self.executor.join()

    def on_exception(self, exception):
        self.executor.killer = True
        self.executor.join()
        raise exception

    def on_limit(self, track):
        logging.warning('a limit message was return by twitter, ' + str(track))


class Executor(threading.Thread):
    def __init__(self, fifo: Queue, selector: TweetSelectorInterface,
                 storage_handler: StorageHandlerInterface, api):
        super().__init__()
        self.fifo = fifo
        self.selector = selector
        self.storage_handler = storage_handler
        self.killer = False
        self.tweet_counter = 0
        self.api = api

    def run(self):
        while True:
            if self.fifo.qsize() == 0:
                if self.killer:
                    return
                time.sleep(1)
            else:
                self.handle_tweets()

    def handle_tweets(self):
        status: tweepy.Status = self.fifo.get()
        rating: float = self.selector.rate_tweet(status)  # get rating from selector

        # put tweets on queue for main telegram channel and twitter
        if rating > 0.61:  # only add tweets with rating above 0.61
            retweet(status, self.api)


def retweet(status, api):
    succeeded = True
    config = Config()
    try:
        api.retweet(status.id)
    except tweepy.error.TweepError:
        succeeded = False
    if config.TELEGRAM and succeeded:
        try:
            Telegram.post_tweet_link(status, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHANNEL_ID)
        except Exception:
            logging.error("Can't post on telegram")
