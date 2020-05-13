import logging
import sys

import requests

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# code for logging to console
console = logging.StreamHandler(sys.stdout)
console.setFormatter(formatter)
logging.root.addHandler(console)

# Code for logging to file
file = logging.FileHandler('bot.log', encoding='utf-8')
file.setFormatter(formatter)
logging.root.addHandler(file)

# code for logging to telegram
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''


class RequestsHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
                             data=payload).content


if TELEGRAM_TOKEN != '' and TELEGRAM_CHAT_ID != '':
    telegram = RequestsHandler()
    telegram.setFormatter(formatter)
    logging.root.addHandler(telegram)

logging.root.setLevel(logging.WARNING)
