import logging
import signal
import sys
import time
import traceback
from datetime import datetime

import tweepy
from apscheduler.schedulers.background import BackgroundScheduler

from twitterbot.storagehandlers.json_storage_handler import JsonStorageHandler
from twitterbot.tweetselectors.greedy_selector import GreedySelector
from twitterbot.twitter.authentication import authenticate_1
from twitterbot.twitter.tweet_listener import TweetListener
from twitterbot.utils.config import Config


def stream_tweets(auth: tweepy.OAuthHandler, api) -> None:
    config = Config()
    if not config.TRACKS:
        config.TRACKS = {'twitter': 0.9}

    logging.warning('starting config:'
                    + '\nretweet interval: ' + str(config.RETWEET_INTERVAL)
                    + '\nsave_tweets: ' + str(config.SAVE_TWEETS)
                    + '\nsave_tweets_path: ' + config.SAVE_TWEETS_PATH
                    + '\ntracks: ' + " ".join(config.TRACKS.keys()))
    try:
        tweet_selector = GreedySelector(api, config.TRACKS, config.FILTER_WORDS, config.BLACK_LIST)
        storage_handler = None
        if config.SAVE_TWEETS:
            storage_handler = JsonStorageHandler(config.SAVE_TWEETS_PATH)
        listener = TweetListener(tweet_selector, api, storage_handler)
        stream = tweepy.Stream(auth=auth, listener=listener)
        # starting stream
        tracks: list = list(config.TRACKS.keys())
        stream.filter(track=tracks[config.START_INDEX:], languages=config.LANGUAGES)
        logging.warning('the stream thread finished.')
    except Exception as e:
        logging.error("Unexpected error: " + str(sys.exc_info()) + "\n" + traceback.format_exc())
        logging.error(e)


def keyboard_interrupt_handler(signal_input, frame):
    logging.error("KeyboardInterrupt (ID: {}) has been caught. exiting".format(signal_input))
    stream_scheduler.shutdown(wait=False)
    exit(0)


def main():
    config = Config()

    auth = authenticate_1(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.TOKEN_KEY, config.TOKEN_SECRET)
    api = tweepy.API(auth)

    stream_scheduler.add_job(stream_tweets,
                             args=[auth, api],
                             coalesce=True,
                             trigger='interval',
                             minutes=20,
                             misfire_grace_time=200,
                             max_instances=1,
                             name='stream_scheduler',
                             next_run_time=datetime.now(),
                             id='stream_scheduler')
    stream_scheduler.start()

    # registering interrupt handler
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    # apscheduler mostly used in web server application, it can't start a job when the main thread is terminated
    # so this infinit loop will keep the main thread running
    # todo: find a better way(suggestion: port whole bot to flask or django and create an gui as well)
    while True:
        time.sleep(10)


if __name__ == "__main__":
    stream_scheduler = BackgroundScheduler()
    main()

    # auth = authenticate_2(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    # api = tweepy.API(auth)
    # for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
    #     print(tweet.text)
