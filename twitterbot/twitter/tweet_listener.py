import logging
import threading
import time
from queue import Queue, PriorityQueue

import tweepy
from twitterbot.abstracts.storage_handler_interface import StorageHandlerInterface
from twitterbot.abstracts.tweet_selector_interface import TweetSelectorInterface
from twitterbot.telegram.telegram import Telegram
from twitterbot.utils.config import Config
from twitterbot.utils.status_rate_wrapper import StatusRateWrapper


class TweetListener(tweepy.StreamListener):
    def __init__(self, queue: PriorityQueue, selector: TweetSelectorInterface,
                 storage_handler: StorageHandlerInterface = None):
        super().__init__()
        self.queue = queue
        self.selector = selector
        self.storage_handler = storage_handler
        self.fifo = Queue()
        self.executor = Executor(self.fifo, queue, selector, storage_handler)

    def on_status(self, status):
        self.fifo.put_nowait(status)

    def on_error(self, status_code):
        logging.warning('an error return by twitter, error code :' + str(status_code))

    def on_connect(self):
        self.executor.start()

    def on_disconnect(self, notice):
        logging.warning(notice)
        self.executor.killer = True
        self.executor.join()

    def on_exception(self, exception):
        logging.critical(exception)

    def on_limit(self, track):
        logging.warning('a limit message was return by twitter, ' + str(track))


class Executor(threading.Thread):
    def __init__(self, fifo: Queue, queue: PriorityQueue, selector: TweetSelectorInterface,
                 storage_handler: StorageHandlerInterface):
        super().__init__()
        self.fifo = fifo
        self.queue = queue
        self.selector = selector
        self.storage_handler = storage_handler
        self.killer = False
        self.tweet_counter = 0

    def run(self):
        while True:
            if self.fifo.qsize() == 0:
                if self.killer:
                    return
                time.sleep(5)
            else:
                self.handle_tweets()

    def handle_tweets(self):
        status: tweepy.Status = self.fifo.get()
        rating: float = self.selector.rate_tweet(status)  # get rating from selector

        # share tweet to voting channel
        config = Config()
        if config.TELEGRAM_BOT_TOKEN != '' and config.TELEGRAM_VOTE_CHANNEL_ID != '' and self.tweet_counter % config.VOTE_SKIP_FACTOR == 0:
            Telegram.post_tweet_link(status, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_VOTE_CHANNEL_ID)
            Telegram.send_poll(status.id_str, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_VOTE_CHANNEL_ID,
                               ['funny', 'useful', 'offensive'])

        # put tweets on queue for main telegram channel and twitter
        if rating > 0.6:  # only add tweets with rating above 0.6
            wrapper = StatusRateWrapper()
            wrapper.status = status
            wrapper.rate = -1 * rating  # (-1 * rating) because python PQ uses min-heap(min value will pop first)
            self.queue.put(wrapper)

        if self.storage_handler is not None:
            self.storage_handler.store_tweet(status)  # save tweets
