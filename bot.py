from utils import keep_alive
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot avviato!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

keep_alive()
main()
