import logging

import tweepy
from twitterbot.abstracts.storage_handler_interface import StorageHandlerInterface


class JsonStorageHandler(StorageHandlerInterface):
    def store_tweet(self, status: tweepy.Status):
        path = '..' + self.FILEPATH + '/' + status.id_str + '.json'
        logging.info('writing: ' + path)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(str(status._json).replace("\"", "").replace("'", "\""))

    def export_tweets_as_jsons(self):
        pass
