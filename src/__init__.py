import logging
import sys

# code for logging to console
console = logging.StreamHandler(sys.stdout)
logging.root.addHandler(console)

# Code for logging to file
file = logging.FileHandler('bot.log')
logging.root.addHandler(file)

logging.basicConfig(level=logging.WARNING)
