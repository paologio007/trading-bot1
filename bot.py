from flask import Flask, request
import telegram
import logging

TOKEN = '7573566344:AAFR5w3pQUkucnvk0woXG63GSy_xFRfp008'
CHAT_ID = 5343167264  # tuo chat ID personale
URL = f"https://trading-bot1-6m9q.onrender.com/{TOKEN}"

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

# Log per debug
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

@app.route('/')
def index():
    return 'Bot attivo!'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text

        # Logica semplice per i segnali
        if text and text.lower().startswith("buy") or text.lower().startswith("sell"):
            bot.send_message(chat_id=CHAT_ID, text=f"📥 Segnale ricevuto:\n{text}")
        else:
            bot.send_message(chat_id=chat_id, text="✅ Bot attivo e funzionante!")

    return 'ok'

if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(host='0.0.0.0', port=10000)
