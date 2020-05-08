import logging
from queue import PriorityQueue

import tweepy
from apscheduler.schedulers.background import BackgroundScheduler

from src.selectors.greedy_selector import GreedySelector
from src.storagehandlers.json_storage_handler import JsonStorageHandler
from src.twitter.authentication import authenticate_1
from src.twitter.tweet_listener import TweetListener
from src.utils.config import Config


# this function will be called in intervals and will pop the top tweet from selected_tweets and retweet it
def retweet_function():
    if selected_tweets.qsize() == 0:
        return
    wrapper = selected_tweets.get(block=False)
    logging.warning('retweeting message with rating(' + str(wrapper.rate * -1) + '): ' + str(wrapper.status.id))
    api.retweet(wrapper.status.id)


if __name__ == "__main__":
    # load configs from file
    with open('../config.json', 'r', encoding="utf-8") as file:
        config = Config(file)
    if not config.TRACKS:
        config.TRACKS = ['twitter']

    logging.info('starting config:'
                 + 'retweet interval: ' + str(config.RETWEET_INTERVAL)
                 + 'save_tweets: ' + str(config.SAVE_TWEETS)
                 + 'save_tweets_path: ' + config.SAVE_TWEETS_PATH
                 + 'tracks: ' + " ".join(config.TRACKS))

    auth = authenticate_1(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.TOKEN_KEY, config.TOKEN_SECRET)
    api = tweepy.API(auth)

    selected_tweets = PriorityQueue()
    tweet_selector = GreedySelector(api, config.TRACKS)
    storage_handler = None
    if config.SAVE_TWEETS:
        storage_handler = JsonStorageHandler(config.SAVE_TWEETS_PATH)
    listener = TweetListener(selected_tweets, tweet_selector, storage_handler)
    stream = tweepy.Stream(auth=auth, listener=listener)

    # scheduler to call retweet_function in intervals
    retweet_scheduler = BackgroundScheduler()
    retweet_scheduler.add_job(retweet_function, trigger='interval', minutes=config.RETWEET_INTERVAL, max_instances=1)
    retweet_scheduler.start()

    # starting stream
    stream.filter(track=config.TRACKS[:10], languages=["fa"])

    # auth = authenticate_2(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    # api = tweepy.API(auth)
    # for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
    #     print(tweet.text)
