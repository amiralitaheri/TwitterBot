import logging
import sys

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# code for logging to console
console = logging.StreamHandler(sys.stdout)
console.setFormatter(formatter)
logging.root.addHandler(console)

# Code for logging to file
file = logging.FileHandler('bot.log', encoding='utf-8')
file.setFormatter(formatter)
logging.root.addHandler(file)

logging.root.setLevel(logging.WARNING)
