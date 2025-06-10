import os
from flask import Flask, request
import telegram
import utils

TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
CHAT_ID = -1002252372969

bot = telegram.Bot(token=TOKEN)

print("📡 TOKEN usato:", TOKEN)
print("💬 CHAT_ID usato:", CHAT_ID)

try:
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot avviato con successo.")
    print("✅ Messaggio di test inviato.")
except Exception as e:
    print("❌ Errore nell'invio del messaggio di test:", e)

WEBHOOK_URL = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"
bot.setWebhook(WEBHOOK_URL)
print(f"🔗 Webhook impostato su {WEBHOOK_URL}")

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
