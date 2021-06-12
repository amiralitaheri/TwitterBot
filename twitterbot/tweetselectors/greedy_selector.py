import logging

import tweepy
from tweepy import Status, API

from twitterbot.abstracts.tweet_selector_interface import TweetSelectorInterface


def remove_symbols(text: str) -> str:
    return text.translate(str.maketrans(
        {'#': ' ', '$': ' ', '/': ' ', '+': ' ', '=': ' ', ':': ' ', ',': ' ', ';': ' ', '؛': ' ', '،': ' ',
         '.': ' ', '!': ' ', '؟': ' ', '?': ' ', '«': ' ', '»': ' ', '(': ' ', ')': ' ', '_': ' ', '-': ' ',
         '@': ' '}))


class GreedySelector(TweetSelectorInterface):
    def __init__(self, api: API, keywords: dict, filter_words: list, user_black_list: list):
        super(GreedySelector, self).__init__()
        self.api = api
        self.keywords = [remove_symbols(keyword) for keyword in keywords]
        self.me = api.me().id
        self.filter_words = filter_words
        self.user_black_list = user_black_list

    def rate_tweet(self, status: Status) -> float:
        rate = 0.0
        if status.text.startswith("RT @"):
            return rate
        if status.user.id_str in self.user_black_list:
            return rate
        if status.in_reply_to_status_id is not None:
            return rate
        logging.info(status)
        if hasattr(status, 'extended_tweet'):
            rate += self._rate_base_on_text(status.extended_tweet['full_text'])
        else:
            rate += self._rate_base_on_text(status.text)
        rate += self._rate_base_on_user(status.user)
        logging.info(rate)
        return min(rate, 1)

    def _rate_base_on_text(self, text: str) -> float:
        value, keywords_dic = self.word_counter(text)
        return value

    def _rate_base_on_user(self, user: tweepy.User) -> float:
        rate = 0.0

        if user.followers_count < 20:
            rate -= 0.3

        if user.followers_count > 1000:
            rate += 0.03

        if user.following is not None:
            rate += 0.1

        if user.description is None:
            return rate

        value, keywords_dic = self.word_counter(user.description)
        rate += value / 3
        return min(rate, 0.1)

    def word_counter(self, text: str) -> (float, dict):
        text = text.lower()
        text = remove_symbols(text)
        text = text.split()
        keywords_dic = {word: 0 for word in self.keywords.keys()}
        value = 0.0
        for i in range(len(text)):
            stemmed_word = text[i]
            if stemmed_word in keywords_dic:
                keywords_dic[stemmed_word] += 1
                if keywords_dic[stemmed_word] == 1:  # count each word only once
                    value += self.keywords[stemmed_word]
            if stemmed_word in self.filter_words:
                return 0, {}
        return value, keywords_dic
