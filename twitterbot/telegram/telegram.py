import logging

import requests
import tweepy


class Telegram:
    @staticmethod
    def post_tweet_link(status: tweepy.Status, bot_token: str, chat_id: str):
        tweet_link = "https://twitter.com/" + status.user.screen_name + "/status/" + status.id_str
        payload = {
            'chat_id': chat_id,
            'text': tweet_link,
            'parse_mode': 'HTML'
        }
        logging.info(requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=bot_token),
                                   data=payload).content)
