import numpy as np
import pandas as pd

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
