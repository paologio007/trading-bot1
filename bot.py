from flask import Flask, request
import telegram
import utils

TOKEN = "6366356663:AAGc2Z3GUumKw0MXzDz4V6VjO4i3BS9Vb0M"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot attivo'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    utils.handle_update(update, bot)
    return 'ok'

if __name__ == '__main__':
    app.run(port=5000)
