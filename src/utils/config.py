import json


class Config:
    def __init__(self, file):
        self.__dict__ = json.load(file)

    # app consumer credentials
    CONSUMER_KEY = "<your consumer key>"
    CONSUMER_SECRET = "<your consumer secret>"
    # user credentials
    TOKEN_KEY = "<your user token(oauth_token)>"
    TOKEN_SECRET = "<your user token secret(oauth_verifier)>"
    # retweet interval in min
    RETWEET_INTERVAL = 10
    # tweets save
    SAVE_TWEETS = False
    SAVE_TWEETS_PATH = "/tweets"
    # custom tracks(keywords) up to 400 keywords
    TRACKS = ["computer"]
