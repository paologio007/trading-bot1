import telegram

# Chat ID del tuo gruppo Telegram
CHAT_ID = -1002114553796

# Percentuale del capitale da usare per ogni segnale (10%)
PERCENTUALE = 0.1  

def handle_update(update, bot):
    # Se è un messaggio di testo
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        text = update.message.text.strip().lower()

        # Comando /start
        if text == "/start":
            bot.send_message(chat_id=chat_id, text="Bot attivo ✅")

        # Comando /segnale: invia un segnale di demo con inline buttons
        elif text == "/segnale":
            send_segnale_demo(bot)

    # Se è il callback di un pulsante
    elif update.callback_query:
        q = update.callback_query

        # Utente ha cliccato SÌ → eseguo ordine simulato al 10%
        if q.data == "conferma_si":
            azione = "COMPRA"
            simbolo = "BTC/USDT"
            percent = int(PERCENTUALE * 100)
            
            # Messaggio di conferma all’utente
            bot.send_message(
                chat_id=q.message.chat.id,
                text=(
                    f"✅ Segnale confermato.\n"
                    f"Eseguo simulazione: {azione} {simbolo} usando il {percent}% del capitale."
                )
            )
            # Log per debug
            print(f"🚀 Ordine simulato: {azione} {simbolo} al {percent}% del capitale")

        # Utente ha cliccato NO → ignoro
        elif q.data == "conferma_no":
            bot.send_message(chat_id=q.message.chat.id, text="❌ Segnale ignorato.")
            print("✋ Segnale ignorato dall'utente.")

def send_segnale_demo(bot):
    keyboard = [
        [telegram.InlineKeyboardButton("SÌ", callback_data="conferma_si")],
        [telegram.InlineKeyboardButton("NO", callback_data="conferma_no")]
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
            "Vuoi che lo esegua usando il 10% del tuo capitale?"
        ),
        reply_markup=telegram.InlineKeyboardMarkup(keyboard)
    )
