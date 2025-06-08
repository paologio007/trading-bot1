from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask
from threading import Thread
import os

# Dati personali già inseriti
TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
ID_CHAT = 1492921711  # tuo user ID da @userinfobot

# Flask app per il keep-alive su Render
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot attivo!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Comando /start
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot avviato!")

# Gestione dei messaggi
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    context.bot.send_message(chat_id=ID_CHAT, text=f"📩 Segnale ricevuto:\n{text}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Aggiungi gestori
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Avvio bot
    keep_alive()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
