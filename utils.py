import telegram

# Chat ID del tuo gruppo Telegram
CHAT_ID = -1001234567890

# Percentuale del guadagno (fee) da riconoscere sui segnali confermati (10%)
FEE_PERCENTUALE = 0.1  

def handle_update(update, bot):
    # Qualsiasi messaggio di testo
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        text = update.message.text.strip().lower()
        print(f"📩 Messaggio ricevuto da {chat_id}: {text}")

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="Bot attivo ✅")
        elif text == "/segnale":
            send_segnale_demo(bot)

    # Callback dei pulsanti
    elif update.callback_query:
        q = update.callback_query

        if q.data == "conferma_si":
            azione = "COMPRA"
            simbolo = "BTC/USDT"
            fee = int(FEE_PERCENTUALE * 100)
            bot.send_message(
                chat_id=q.message.chat.id,
                text=(
                    f"✅ Segnale confermato.\n"
                    f"Eseguo simulazione: {azione} {simbolo}.\n"
                    f"Ti spettano {fee}% del guadagno come fee."
                )
            )
            print(f"🚀 Segnale eseguito: {azione} {simbolo} — fee {fee}% del guadagno")

        elif q.data == "conferma_no":
            bot.send_message(chat_id=q.message.chat.id, text="❌ Segnale ignorato.")
            print("✋ Segnale ignorato dall'utente.")

def send_segnale_demo(bot):
    keyboard = [
        [telegram.InlineKeyboardButton("SÌ, CONFERMO", callback_data="conferma_si")],
        [telegram.InlineKeyboardButton("NO, ANNULLA", callback_data="conferma_no")]
    ]
    bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "📈 Segnale pronto (SIMULAZIONE)\n"
            "Strumento: BTC/USDT\n"
            "Operazione: COMPRA\n"
            "Prezzo di ingresso: 67.200\n"
            "🎯 TP: 67.900\n"
            "🛑 SL: 66.750\n\n"
            "Se confermi, mi spetta il 10% del guadagno derivante da questo trade.\n"
            "Vuoi procedere?"
        ),
        reply_markup=telegram.InlineKeyboardMarkup(keyboard)
    )
