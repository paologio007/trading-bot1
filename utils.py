def parse_signal(message):
    try:
        parts = message.strip().split()
        if len(parts) < 3:
            return "❌ Formato segnale non valido."

        action = parts[0].upper()
        symbol = parts[1].upper()
        price = parts[2]

        return f"✅ Segnale ricevuto: {action} {symbol} a {price}"
    except Exception as e:
        return f"❌ Errore nel parsing: {str(e)}"
