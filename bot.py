from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import time
from flask import Flask
from threading import Thread

# Token e chat ID
TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
CHAT_ID = 1492921711

# Flask per mantenere il bot attivo
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot attivo!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# Comando /start
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot avviato!")

# Messaggi normali nel gruppo
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=CHAT_ID, text=f"📩 Segnale ricevuto:\n{update.message.text}")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters=None, callback=echo))  # Riceve tutti i messaggi

    keep_alive()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
