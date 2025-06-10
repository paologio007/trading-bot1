import os
from flask import Flask, request
import telegram
import utils

# Token e Chat ID
TOKEN   = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
CHAT_ID = -1002225387120

bot = telegram.Bot(token=TOKEN)

# Messaggio di test all’avvio
try:
    bot.send_message(chat_id=CHAT_ID, text="🚀 Bot avviato e pronto ✅")
    print("✅ Messaggio di test inviato al gruppo.")
except Exception as e:
    print("❌ Errore invio test:", e)

# Imposta webhook automaticamente (Render)
WEBHOOK_URL = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
bot.setWebhook(WEBHOOK_URL)
print(f"➡️ Webhook impostato su {WEBHOOK_URL}")

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
