import hazm
from tweepy import Status, API

from src.abstracts.tweet_selector_interface import TweetSelectorInterface


class GreedySelector(TweetSelectorInterface):
    def __init__(self, api: API, keywords: list):
        super(GreedySelector, self).__init__()
        self.api = api
        self.keywords = keywords
        self.me = api.me().id

    def rate_tweet(self, status: Status):
        rate = 0
        if status.lang != 'fa':
            return rate
        rate += self._rate_base_on_text(status.text)
        rate += self._rate_base_on_user(status.user)
        return max(rate, 1)

    def _rate_base_on_text(self, text):
        keywords_counter, keywords_dic = self.word_counter(text)
        if keywords_counter < 5:
            return keywords_counter * 0.2
        return 0.4  # to many keywords probably is a spam

    def _rate_base_on_user(self, user):
        rate = 0

        if user.friends_count < user.followers_count:
            rate += 0.1

        if user.followers_count > 1000:
            rate += 0.1

        relation = self.api.lookup_friendships([self.me, user.id])[0]
        if relation.is_following or relation.is_followed_by:
            rate += 0.1

        if user.description is None:
            return rate

        keywords_counter, keywords_dic = self.word_counter(user.description)
        rate += keywords_counter * 0.1
        return rate

    def word_counter(self, text):
        text = hazm.Normalizer().normalize(text)
        text = hazm.word_tokenize(text)
        stemmer = hazm.Stemmer()
        keywords_dic = {word: 0 for word in self.keywords}
        keywords_counter = 0
        for i in range(len(text)):
            stemmed_word = stemmer.stem(text[i])
            if stemmed_word in keywords_dic:
                keywords_dic[stemmed_word] += 1
                keywords_counter += 1
        return keywords_counter, keywords_dic
