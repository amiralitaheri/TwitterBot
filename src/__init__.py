import logging
import sys

# code for logging to console
console = logging.StreamHandler(sys.stdout)
logging.root.addHandler(console)

# Code for logging to file
file = logging.FileHandler('bot.log', encoding='utf-8')
logging.root.addHandler(file)
logging.root.setLevel(logging.WARNING)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
