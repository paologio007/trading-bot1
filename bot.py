from flask import Flask, request
import telegram
from utils import parse_signal

TOKEN = "7573566344:AAFR5w3pQUkucnvk0woXG63GSy_xFRfp008"
ID_CHAT = 5343167264

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot attivo'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    if update.message:
        message_text = update.message.text
        response = parse_signal(message_text)
        bot.send_message(chat_id=ID_CHAT, text=response)
    
    return 'ok'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
