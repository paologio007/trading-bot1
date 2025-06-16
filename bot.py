import time
import threading
import requests
import hmac
import hashlib
import pandas as pd
import csv
from datetime import datetime, timedelta
from urllib.parse import urlencode
from flask import Flask

from strategy import should_buy
from symbol_selector import get_top_usdt_symbols

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

INTERVAL = '15m'
RISK_PERCENT = 0.10  # Usa il 10% del capitale
TRAILING_PERCENT = 0.03
MAX_HOURS_OPEN = 6

ACTIVE_TRADES = {}

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

def get_balance(asset='USDT'):
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f'{BASE_URL}/api/v3/account?{query_string}&signature={signature}'
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.get(url, headers=headers).json()
    for b in response['balances']:
        if b['asset'] == asset:
            return float(b['free'])
    return 0.0

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
    return requests.post(url, headers=headers).json()

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
    return requests.post(url, headers=headers).json()

def log_trade(symbol, price, qty, sl, tp):
    with open("trades.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), symbol, price, qty, sl, tp])

# === CICLO PRINCIPALE ===
def run_bot():
    print("🔁 Avvio bot potenziato...")

    while True:
        try:
            symbols = get_top_usdt_symbols(limit=20)

            for symbol in symbols:
                print(f"\n[{datetime.now()}] Analizzo {symbol}")

                # Skip se già attiva
                if symbol in ACTIVE_TRADES:
                    start_time = ACTIVE_TRADES[symbol]['time']
                    if datetime.now() - start_time > timedelta(hours=MAX_HOURS_OPEN):
                        print(f"⏳ {symbol} aperto da troppo tempo. Chiudo (simulato).")
                        del ACTIVE_TRADES[symbol]
                    else:
                        print(f"⏸️ Trade già attivo su {symbol}")
                        continue

                data = get_klines(symbol, INTERVAL, 100)
                df = pd.DataFrame(data, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_asset_volume', 'number_of_trades',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                ])
                df['close'] = df['close'].astype(float)

                if should_buy(df):
                    usdt_balance = get_balance()
                    budget = usdt_balance * RISK_PERCENT
                    price = get_price(symbol)
                    qty = round(budget / price, 6)

                    place_market_buy(symbol, qty)

                    sl_price = price * (1 - TRAILING_PERCENT)
                    tp_price = price * (1 + TRAILING_PERCENT * 1.5)

                    place_oco_order(symbol, qty, price, sl_price, tp_price)

                    ACTIVE_TRADES[symbol] = {
                        'time': datetime.now(),
                        'price': price
                    }

                    log_trade(symbol, price, qty, sl_price, tp_price)
                    print(f"✅ BUY {symbol} @ {price:.2f} | SL: {sl_price:.2f} | TP: {tp_price:.2f}")
                else:
                    print(f"❌ Nessun segnale su {symbol}")

        except Exception as e:
            print(f"‼️ Errore: {e}")

        print("⏱️ Attendo 15 minuti...\n")
        time.sleep(60 * 15)

# === AVVIO ===
if __name__ == '__main__':
    print("🟢 Avvio bot e Flask...")
    threading.Thread(target=run_bot).start()
    start_flask()
