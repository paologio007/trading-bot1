import requests

def get_top_usdt_symbols(limit=20):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()

    # Filtro solo coppie con USDT, escluse stablecoin & leverage token
    usdt_pairs = [
        d for d in data
        if d['symbol'].endswith('USDT')
        and not any(x in d['symbol'] for x in ['BUSD', 'USDC', 'UP', 'DOWN', 'BULL', 'BEAR'])
        and float(d['quoteVolume']) > 0
    ]

    # Ordina per volume discendente
    usdt_pairs.sort(key=lambda x: float(x['quoteVolume']), reverse=True)

    # Prendi solo i primi N simboli
    top_symbols = [d['symbol'] for d in usdt_pairs[:limit]]
    return top_symbols
