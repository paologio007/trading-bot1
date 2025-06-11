from flask import Flask, request
import telegram

TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"
ID_CHAT = 5343167264

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot attivo'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message_text = update.message.text

    response = f"Messaggio ricevuto: {message_text}"
    bot.send_message(chat_id=ID_CHAT, text=response)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
