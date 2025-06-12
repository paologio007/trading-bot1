import time
import requests
import hmac
import hashlib
import json
import numpy as np
import pandas as pd
from datetime import datetime
from urllib.parse import urlencode

# === CONFIG ===
API_KEY = 'encRf4ZyAY6qWbAnYeuEb1SQ7oPFMDYKJxnsKbdznWc1EpM1AcPleK1fagVcVZap'
API_SECRET = 'h4fBXuTDi9zeHsc5bD6MLPnhbkc21sKFpP2Hcjd9X6owZXPkaPf4ueOTloVd6BfP'
BASE_URL = 'https://api.binance.com'

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'AVAXUSDT']
INTERVAL = '15m'
TRADE_AMOUNT_USDT = 40

# === API BINANCE ===
def get_klines(symbol, interval, limit=100):
    url = f"{BASE_URL}/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    return response.json()

def get_price(symbol):
    url = f"{BASE_URL}/api/v3/ticker/price"
    params = {'symbol': symbol}
    response = requests.get(url, params=params)
    return float(response.json()['price'])

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

def run_bot():
    for symbol in SYMBOLS:
        try:
            data = get_klines(symbol, INTERVAL, 100)
            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            df['close'] = df['close'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)

            if should_buy(df):
                price = get_price(symbol)
                qty = round(TRADE_AMOUNT_USDT / price, 6)
                response = place_order(symbol, 'BUY', qty)
                print(f"{datetime.now()} - BUY {symbol} - qty: {qty} - {response}")
            else:
                print(f"{datetime.now()} - No signal for {symbol}")
        except Exception as e:
            print(f"Error on {symbol}: {e}")

# === LOOP CONTINUO ===
while True:
    run_bot()
    time.sleep(60 * 15)  # ogni 15 minuti
