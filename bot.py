from flask import Flask, request
import telegram
import os
from utils import parse_signal

TOKEN = "7573566344:AAFR5w3pQUkucnvk0woXG63GSy_xFRfp008"
CHAT_ID = 5343167264

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
bot.setWebhook(WEBHOOK_URL)
print("➡️ Webhook impostato su", WEBHOOK_URL)

@app.route("/")
def index():
    return "Bot attivo."

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message.text.strip()

    if message.startswith("BUY") or message.startswith("SELL"):
        response = parse_signal(message)
        bot.send_message(chat_id=CHAT_ID, text=response)
    return "ok"
