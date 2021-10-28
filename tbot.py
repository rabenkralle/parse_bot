from parse_web import logging_site, parse_site
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger()

addr = {1: "___",
        2: "___",
        3: "___"}


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi!')
    choose_parse = input('1', '2', '3')
    br = logging_site()
    if choose_parse == 1:
        in_stock_check, button_check = parse_site(addr[1],br)
        if in_stock_check and button_check:

#NOT FINISHED