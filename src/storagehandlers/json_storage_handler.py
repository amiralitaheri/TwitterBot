from src.abstracts.storage_handler_interface import StorageHandlerInterface
import logging


class JsonStorageHandler(StorageHandlerInterface):
    def store_tweet(self, status):
        path = '../..' + self.FILEPATH + '/' + status.id + '.json'
        logging.info('writing: ' + path)
        with open(path, 'w') as tweet:
            tweet.write(status)

    def export_tweets_as_jsons(self):
        pass
