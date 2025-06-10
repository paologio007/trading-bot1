import os
from flask import Flask, request
import telegram
import utils

# Token del tuo bot Telegram
TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
bot = telegram.Bot(token=TOKEN)

# Imposta automaticamente il webhook su Render
WEBHOOK_URL = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
bot.setWebhook(WEBHOOK_URL)
print(f"➡️ Webhook settato su {WEBHOOK_URL}")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot attivo ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    utils.handle_update(update, bot)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
