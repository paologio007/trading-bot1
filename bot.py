import time
import threading
import requests
import hmac
import hashlib
import numpy as np
import pandas as pd
import csv
from datetime import datetime
from urllib.parse import urlencode
from flask import Flask

# === SERVER FLASK ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot attivo e funzionante."

def start_flask():
    app.run(host='0.0.0.0', port=10000)

# === CONFIG ===
API_KEY = 'encRf4ZyAY6qWbAnYeuEb1SQ7oPFMDYKJxnsKbdznWc1EpM1AcPleK1fagVcVZap'
API_SECRET = 'h4fBXuTDi9zeHsc5bD6MLPnhbkc21sKFpP2Hcjd9X6owZXPkaPf4ueOTloVd6BfP'
BASE_URL = 'https://api.binance.com'

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'AVAXUSDT']
INTERVAL = '15m'
TRADE_AMOUNT_USDT = 40
ACTIVE_POSITIONS = set()

# === BINANCE API ===
def get_klines(symbol, interval, limit=100):
    url = f"{BASE_URL}/api/v3/klines"
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    return response.json()

def get_price(symbol):
    url = f"{BASE_URL}/api/v3/ticker/price"
    params = {'symbol': symbol}
    response = requests.get(url, params=params)
    return float(response.json()['price'])

def log_trade(symbol, price, qty, sl, tp):
    with open("trades.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), symbol, price, qty, sl, tp])

def place_oco_order(symbol, quantity, entry_price, stop_loss, take_profit):
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'OCO',
        'quantity': quantity,
        'price': f"{take_profit:.2f}",
        'stopPrice': f"{stop_loss * 1.01:.2f}",
        'stopLimitPrice': f"{stop_loss:.2f}",
        'stopLimitTimeInForce': 'GTC',
        'timestamp': timestamp
    }
    query_string = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}/api/v3/order/oco?{query_string}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.post(url, headers=headers)
    return response.json()

def place_market_buy(symbol, quantity):
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': quantity,
        'timestamp': timestamp
    }
    query_string = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}/api/v3/order?{query_string}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.post(url, headers=headers)
    return response.json()

# === STRATEGIA ===
def rsi(close, period=14):
    delta = np.diff(close)
    up = delta.clip(min=0)
    down = -1 * delta.clip(max=0)
    ema_up = pd.Series(up).ewm(span=period).mean()
    ema_down = pd.Series(down).ewm(span=period).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs))

def should_buy(df):
    recent_close = df['close'].values
    rsi_val = rsi(recent_close)[-1]
    breakout = recent_close[-1] > max(recent_close[-10:-2])
    return rsi_val < 30 and breakout

# === LOGICA DEL BOT ===
def run_bot():
    print("🔁 Avvio ciclo trading bot...")
    while True:
        for symbol in SYMBOLS:
            try:
                print(f"\n[{datetime.now()}] Analizzo {symbol}")

                if symbol in ACTIVE_POSITIONS:
                    print(f"⏳ Posizione già attiva per {symbol}. Skipping.")
                    continue

                data = get_klines(symbol, INTERVAL, 100)
                df = pd.DataFrame(data, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_asset_volume', 'number_of_trades',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                ])
                df['close'] = df['close'].astype(float)

                if should_buy(df):
                    price = get_price(symbol)
                    qty = round(TRADE_AMOUNT_USDT / price, 6)
                    entry_order = place_market_buy(symbol, qty)

                    sl_price = price * 0.97
                    tp_price = price * 1.04
                    oco_order = place_oco_order(symbol, qty, price, sl_price, tp_price)

                    ACTIVE_POSITIONS.add(symbol)
                    log_trade(symbol, price, qty, sl_price, tp_price)

                    print(f"✅ Eseguito BUY su {symbol} - Prezzo: {price:.2f} - SL: {sl_price:.2f} - TP: {tp_price:.2f}")
                else:
                    print(f"Nessun segnale per {symbol}.")
            except Exception as e:
                print(f"❌ Errore su {symbol}: {e}")

        print("🕒 Attesa 15 minuti...\n")
        time.sleep(60 * 15)

# === AVVIO PARALLELO ===
if __name__ == '__main__':
    print("🟢 Avvio bot e server Flask...")
    threading.Thread(target=run_bot).start()
    start_flask()
