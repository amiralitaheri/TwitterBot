import tweepy


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
        print(status)

    def on_error(self, status_code):
        print(status_code)

    def on_disconnect(self, notice):
        print(notice)

    def on_exception(self, exception):
        super().on_exception(exception)

    def on_limit(self, track):
        super().on_limit(track)
