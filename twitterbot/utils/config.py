import json


class Config:
    instance = None

    def __init__(self, file=None):
        if not file:
            return
        if not Config.instance:
            Config.instance = Config.__Config(file)
        else:
            Config.instance.load_config(file)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Config:
        def __init__(self, file):
            self.load_config(file)

        def load_config(self, file):
            self.__dict__ = json.load(file)

        # app consumer credentials
        CONSUMER_KEY: str = "<your consumer key>"
        CONSUMER_SECRET: str = "<your consumer secret>"
        # user credentials
        TOKEN_KEY: str = "<your user token(oauth_token)>"
        TOKEN_SECRET: str = "<your user token secret(oauth_verifier)>"
        # retweet interval in min
        RETWEET_INTERVAL: int = 10
        # tweets save
        SAVE_TWEETS: bool = False
        SAVE_TWEETS_PATH: str = "/tweets"
        # number of elements to skip from track but include as key word
        START_INDEX: int = 0
        # custom tracks(keywords) up to 400 keywords with a wight between [0,1]
        TRACKS: dict = {"computer": 0.9}
        # languages of tracked tweets
        LANGUAGES: list = ["fa"]
        # words to filter out
        FILTER_WORDS: list = ["sex", "fuck"]
        # users blacklist
        BLACK_LIST: list = ["45645645646"]
        # telegram channel info
        TELEGRAM: bool = False
        TELEGRAM_BOT_TOKEN: str = ""
        TELEGRAM_CHANNEL_ID: str = ""
        TELEGRAM_LOG_CHAT_ID: str = ""
        TELEGRAM_VOTE_CHANNEL_ID: str = ""
        VOTE_SKIP_FACTOR: int = 0
