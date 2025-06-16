import time
import threading
import requests
import hmac
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import urlencode
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot attivo e funzionante."

def start_flask():
    app.run(host='0.0.0.0', port=10000)

# === CONFIG ===
API_KEY = 'INSERISCI_LA_TUA_API_KEY'
API_SECRET = 'INSERISCI_LA_TUA_API_SECRET'
BASE_URL = 'https://api.binance.com'

SYMBOLS = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'DOGEUSDT',
    'ADAUSDT', 'AVAXUSDT', 'DOTUSDT', 'SHIBUSDT', 'LINKUSDT', 'MATICUSDT',
    'TRXUSDT', 'LTCUSDT', 'UNIUSDT', 'ATOMUSDT', 'ETCUSDT', 'XLMUSDT',
    'ICPUSDT', 'FILUSDT', 'HBARUSDT', 'APTUSDT', 'ARBUSDT', 'SANDUSDT',
    'AAVEUSDT', 'MKRUSDT', 'NEARUSDT', 'THETAUSDT', 'EGLDUSDT', 'FTMUSDT'
]
INTERVAL = '15m'
TRADE_PERCENT = 0.30  # 30% del saldo disponibile

def get_klines(symbol, interval, limit=100):
    url = f"{BASE_URL}/api/v3/klines"
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    return response.json()

def get_price(symbol):
    url = f"{BASE_URL}/api/v3/ticker/price"
    response = requests.get(url, params={'symbol': symbol})
    return float(response.json()['price'])

def get_balance():
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.get(url, headers=headers).json()
    for asset in response['balances']:
        if asset['asset'] == 'USDT':
            return float(asset['free'])
    return 0.0

def place_order(symbol, side, quantity):
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': side,
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

def rsi(close, period=14):
    delta = np.diff(close)
    up = delta.clip(min=0)
    down = -1 * delta.clip(max=0)
    ema_up = pd.Series(up).ewm(span=period).mean()
    ema_down = pd.Series(down).ewm(span=period).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs))

def volume_filter(df):
    current_volume = df['volume'].values[-1]
    average_volume = np.mean(df['volume'].values[-20:])
    return current_volume > average_volume

def trend_filter(df):
    sma50 = df['close'].rolling(window=50).mean()
    sma200 = df['close'].rolling(window=200).mean()
    return sma50.iloc[-1] > sma200.iloc[-1]

def should_buy(df):
    closes = df['close'].values
    rsi_val = rsi(closes)[-1]
    breakout = closes[-1] > max(closes[-10:-2])
    return rsi_val < 30 and breakout and volume_filter(df) and trend_filter(df)

def run_bot():
    print("🔁 Avvio bot potenziato...")
    while True:
        now = datetime.utcnow() + timedelta(hours=2)  # GMT+2
        if now.hour < 9 or now.hour >= 22:
            print("⏰ Fuori orario operativo (09:00–22:00 CET). Dormo 15 min...")
            time.sleep(900)
            continue

        balance = get_balance()
        if balance <= 10:
            print("💸 Saldo insufficiente. Attendo 15 min...")
            time.sleep(900)
            continue

        amount_usdt = balance * TRADE_PERCENT

        for symbol in SYMBOLS:
            try:
                print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Analisi {symbol}")
                data = get_klines(symbol, INTERVAL, 200)
                df = pd.DataFrame(data, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_asset_volume', 'number_of_trades',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                ])
                df['close'] = df['close'].astype(float)
                df['volume'] = df['volume'].astype(float)

                if should_buy(df):
                    price = get_price(symbol)
                    qty = round(amount_usdt / price, 6)
                    response = place_order(symbol, 'BUY', qty)
                    print(f"✅ BUY {symbol} - Qty: {qty} - USDT: {amount_usdt:.2f} - Resp: {response}")
                else:
                    print(f"⛔ Nessun segnale su {symbol}")
            except Exception as e:
                print(f"❌ Errore su {symbol}: {e}")
        print("🕒 Fine ciclo. Dormo 15 minuti...\n")
        time.sleep(900)

if __name__ == '__main__':
    print("🟢 Avvio bot e server Flask...")
    threading.Thread(target=run_bot).start()
    start_flask()
