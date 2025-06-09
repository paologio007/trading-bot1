import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils import execute_trade
from flask import Flask, request

app = Flask(__name__)

TOKEN = "7257421165:AAGfkQ7jydVeS8WvrixCEb7diUnhHIF30ls"
CHAT_ID = 1492921711

bot = telegram.Bot(token=TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot avviato!")

def handle_message(update, context):
    text = update.message.text.strip().upper()
    if "BUY" in text or "SELL" in text:
        result = execute_trade(text)
        context.bot.send_message(chat_id=CHAT_ID, text=f"📩 Segnale ricevuto:\n{text}\n\n⛓ Risultato:\n{result}")

def webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "OK"

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

@app.route('/', methods=["GET", "POST"])
def index():
    return webhook(request)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
