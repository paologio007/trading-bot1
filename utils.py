from binance.client import Client
import os

# API KEY e SECRET reale Binance
api_key = "HaG1iRu65S9G1OxfOO1GmXjZ6fqTqCVghtrcIFUW8ry6o7Oyckp8qEynfMtgDlXQ"
api_secret = "vgBpgEQLv6sejc0IhFMAiL2jGkQqcL6QnMT77iypGY5zJI8zR1auBkxUKWYjhZ24"

client = Client(api_key, api_secret)

def execute_trade(signal_text):
    try:
        action = "BUY" if "BUY" in signal_text.upper() else "SELL"
        symbol = "BTCUSDT"
        quantity = 0.0001  # imposta la quantità desiderata

        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY if action == "BUY" else Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return f"✅ Ordine {action} eseguito\nID ordine: {order['orderId']}"
    except Exception as e:
        return f"❌ Errore durante l'esecuzione: {e}"
