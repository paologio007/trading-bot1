import os
import time
import random
import requests
from flask import Flask
from prophet import Prophet
import pandas as pd

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

app = Flask(__name__)

def genera_dati_fake():
    oggi = pd.Timestamp.now()
    giorni = pd.date_range(oggi - pd.Timedelta(days=30), oggi, freq='D')
    prezzo = [random.uniform(1500, 65000) for _ in giorni]
    return pd.DataFrame({'ds': giorni, 'y': prezzo})

def predici():
    df = genera_dati_fake()
    modello = Prophet()
    modello.fit(df)
    futuro = modello.make_future_dataframe(periods=1)
    forecast = modello.predict(futuro)
    ultimo = forecast.iloc[-1]
    return round(ultimo['yhat'], 2)

def genera_segnale():
    crypto = random.choice(["BTC/USDT", "ETH/USDT"])
    direzione = random.choice(["BUY", "SELL"])
    entry = predici()
    tp = round(entry * 1.03, 2)
    sl = round(entry * 0.985, 2)
    return f"📡 Segnale AI:\n{crypto} - {direzione}\nEntry: {entry}$\nTP: {tp}$\nSL: {sl}$"

def invia_segnale(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=payload)

@app.route('/')
def home():
    return "TradeBrainAI attivo"

@app.route('/send')
def send():
    segnale = genera_segnale()
    invia_segnale(segnale)
    return "Segnale inviato!"

if __name__ == "__main__":
    while True:
        try:
            segnale = genera_segnale()
            invia_segnale(segnale)
            print("Segnale inviato")
        except Exception as e:
            print(f"Errore: {e}")
        time.sleep(900)  # ogni 15 minuti
