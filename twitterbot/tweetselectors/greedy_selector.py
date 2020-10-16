import hazm
from tweepy import Status

from twitterbot.abstracts.tweet_selector_interface import TweetSelectorInterface


class GreedySelector(TweetSelectorInterface):
    def __init__(self, keywords: dict, filter_words: list, user_black_list: list):
        super(GreedySelector, self).__init__()
        self.keywords = keywords
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
        if hasattr(status, 'extended_tweet'):
            rate += self._rate_base_on_text(status.extended_tweet['full_text'])
        else:
            rate += self._rate_base_on_text(status.text)
        if status.user.followers_count < 20:
            rate -= 0.3
        return min(rate, 1)

    def _rate_base_on_text(self, text: str) -> float:
        return self.word_counter(text)

    def word_counter(self, text: str) -> float:
        text = text.lower()
        text = text.translate(str.maketrans(
            {'#': ' ', '$': ' ', '/': ' ', '+': ' ', '=': ' ', ':': ' ', ',': ' ', ';': ' ', '؛': ' ', '،': ' ',
             '.': ' ', '!': ' ', '؟': ' ', '?': ' ', '«': ' ', '»': ' ', '(': ' ', ')': ' ', '_': ' ', '-': ' ',
             '@': ' '}))
        text = hazm.Normalizer().normalize(text)
        text = hazm.word_tokenize(text)
        stemmer = hazm.Stemmer()
        keywords_dic = {word: 0 for word in self.keywords.keys()}
        value = 0.0
        for i in range(len(text)):
            stemmed_word = stemmer.stem(text[i])
            if stemmed_word in keywords_dic:
                keywords_dic[stemmed_word] += 1
                if keywords_dic[stemmed_word] == 1:  # count each word only once
                    value += self.keywords[stemmed_word]
            if stemmed_word in self.filter_words:
                return 0
        return value
