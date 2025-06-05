from utils import keep_alive
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

def start(update, context):
    update.message.reply_text("Bot avviato!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

keep_alive()
main()
