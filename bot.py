from flask import Flask, request
import telegram
import os
from utils import parse_signal

TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
CHAT_ID = "-1002292399479"

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

@app.route("/")
def index():
    # Imposto il webhook quando viene chiamata la root
    WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.setWebhook(WEBHOOK_URL)
    print("➡️ Webhook settato su", WEBHOOK_URL)
    return "Webhook settato."

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message and update.message.text:
        message = update.message.text.strip()

        if message.startswith("BUY") or message.startswith("SELL"):
            response = parse_signal(message)
            bot.send_message(chat_id=CHAT_ID, text=response)
    return "ok"
