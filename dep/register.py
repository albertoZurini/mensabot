from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
import logging
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='', use_context=True)

dispatcher = updater.dispatcher

from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Chat id: {update.effective_chat.id}")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_polling()
