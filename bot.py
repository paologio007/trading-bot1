from flask import Flask, request
import telegram
import utils

# Token del tuo bot Telegram (già inserito)
TOKEN = "6366356663:AAGc2Z3GUumKw0MXzDz4V6VjO4i3BS9Vb0M"
bot   = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot attivo ✅"

# Percorso fisso per il webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    utils.handle_update(update, bot)
    return "ok"

if __name__ == "__main__":
    # Impostazione necessaria su Render
    app.run(host="0.0.0.0", port=5000)
