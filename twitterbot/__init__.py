import logging
import sys

import requests
from twitterbot.utils.config import Config

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# code for logging to console
console = logging.StreamHandler(sys.stdout)
console.setFormatter(formatter)
logging.root.addHandler(console)

# Code for logging to file
file = logging.FileHandler('bot.log', encoding='utf-8')
file.setFormatter(formatter)
logging.root.addHandler(file)


class RequestsHandler(logging.Handler):
    def __init__(self, telegram_token, telegram_chat_id):
        super().__init__()
        self.TELEGRAM_TOKEN = telegram_token
        self.TELEGRAM_CHAT_ID = telegram_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': self.TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=self.TELEGRAM_TOKEN),
                             data=payload).content


# load configs from file
with open('config.json', 'r', encoding="utf-8") as file:
    config = Config(file)

if config.TELEGRAM_BOT_TOKEN != '' and config.TELEGRAM_LOG_CHAT_ID != '':
    telegram = RequestsHandler(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_LOG_CHAT_ID)
    telegram.setFormatter(formatter)
    logging.root.addHandler(telegram)

logging.root.setLevel(logging.WARNING)
