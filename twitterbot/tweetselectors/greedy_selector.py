import logging

import hazm
from tweepy import Status, API
from twitterbot.abstracts.tweet_selector_interface import TweetSelectorInterface


class GreedySelector(TweetSelectorInterface):
    def __init__(self, api: API, keywords: list, filter_words: list):
        super(GreedySelector, self).__init__()
        self.api = api
        self.keywords = keywords
        self.me = api.me().id
        self.filter_words = filter_words

    def rate_tweet(self, status: Status):
        rate = 0

        if status.in_reply_to_status_id is not None:
            rate -= 0.4
        logging.info(status)
        if hasattr(status, 'extended_tweet'):
            rate += self._rate_base_on_text(status.extended_tweet['full_text'])
        else:
            rate += self._rate_base_on_text(status.text)
        rate += self._rate_base_on_user(status.user)
        logging.info(rate)
        return min(rate, 1)

    def _rate_base_on_text(self, text):
        keywords_counter, keywords_dic = self.word_counter(text)
        if keywords_counter < 6:
            return keywords_counter * 0.2
        return 0.4  # to many keywords probably is a spam

    def _rate_base_on_user(self, user):
        rate = 0.0

        if user.followers_count < 20:
            rate -= 0.3

        if user.followers_count > 1000:
            rate += 0.03

        if user.following is not None:
            rate += 0.1

        if user.description is None:
            return rate

        keywords_counter, keywords_dic = self.word_counter(user.description)
        rate += keywords_counter * 0.1
        return min(rate, 0.33)

    def word_counter(self, text):
        text = text.lower()
        text = text.translate(str.maketrans(
            {'#': ' ', '$': ' ', '/': ' ', '+': ' ', '=': ' ', ':': ' ', ',': ' ', ';': ' ', '؛': ' ', '،': ' ',
             '.': ' ', '!': ' ', '؟': ' ', '?': ' ', '«': ' ', '»': ' ', '(': ' ', ')': ' ', '_': ' ', '-': ' ',
             '@': ' '}))
        text = hazm.Normalizer().normalize(text)
        text = hazm.word_tokenize(text)
        stemmer = hazm.Stemmer()
        keywords_dic = {word: 0 for word in self.keywords}
        keywords_counter = 0
        for i in range(len(text)):
            stemmed_word = stemmer.stem(text[i])
            if stemmed_word in keywords_dic:
                keywords_dic[stemmed_word] += 1
                if keywords_dic[stemmed_word] == 1:
                    keywords_counter += 1
            if stemmed_word in self.filter_words:
                return 0, {}
        return keywords_counter, keywords_dic
