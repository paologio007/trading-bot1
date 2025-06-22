import os
import time
import telegram
import random
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def genera_segnale():
    crypto = random.choice(["BTC/USDT", "ETH/USDT"])
    direzione = random.choice(["BUY", "SELL"])
    prezzo = round(random.uniform(1500, 65000), 2)
    tp = round(prezzo * (1 + 0.03), 2)
    sl = round(prezzo * (1 - 0.015), 2)
    return f"📡 Segnale AI:\n{crypto} - {direzione}\nEntry: {prezzo}$\nTP: {tp}$\nSL: {sl}$"

@app.route('/', methods=['GET'])
def home():
    return 'Bot attivo'

@app.route('/send', methods=['GET'])
def send_signal():
    segnale = genera_segnale()
    bot.send_message(chat_id=CHAT_ID, text=segnale)
    return 'Segnale inviato!'

if __name__ == '__main__':
    while True:
        try:
            segnale = genera_segnale()
            bot.send_message(chat_id=CHAT_ID, text=segnale)
            print("Segnale inviato.")
        except Exception as e:
            print(f"Errore: {e}")
        time.sleep(900)
