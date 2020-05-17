import json
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
        Telegram.send_poll(status.id_str, bot_token, chat_id, ['funny', 'useful', 'offensive'])

    @staticmethod
    def send_poll(tweet_id: str, bot_token: str, chat_id: str, options: list):
        payload = {
            'chat_id': chat_id,
            'question': '⬆⬆' + tweet_id + '⬆⬆',
            'options': json.dumps(options),
            'is_anonymous': True,
            'allows_multiple_answers': True,
            'parse_mode': 'HTML'
        }

        logging.info(requests.post("https://api.telegram.org/bot{token}/sendPoll".format(token=bot_token),
                                   data=payload).content)
