import numpy as np
import pandas as pd

def rsi(close_prices, period=14):
    delta = np.diff(close_prices)
    up = delta.clip(min=0)
    down = -1 * delta.clip(max=0)

    ema_up = pd.Series(up).ewm(span=period).mean()
    ema_down = pd.Series(down).ewm(span=period).mean()

    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def should_buy(df):
    close_prices = df['close'].values

    # Protezione: serve almeno 20 candele
    if len(close_prices) < 20:
        return False

    rsi_val = rsi(close_prices)[-1]
    recent_close = close_prices[-1]
    previous_highs = close_prices[-10:-2]
    breakout = recent_close > max(previous_highs)

    return rsi_val < 30 and breakout

def should_sell(df):
    close_prices = df['close'].values

    # Usiamo un RSI > 70 come possibile segnale di ipercomprato (non usato dal bot ora)
    rsi_val = rsi(close_prices)[-1]
    return rsi_val > 70
