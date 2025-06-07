from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import time
from flask import Flask
from threading import Thread

# Token del bot
TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
CHAT_ID = 1492921711

# Flask app per il keep-alive
app = Flask('')

@app.route('/')
def home():
    return "Bot attivo!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# Funzione di start
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot avviato!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handler per /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Avvio del bot
    updater.start_polling()
    keep_alive()
    updater.idle()

if __name__ == '__main__':
    main()
