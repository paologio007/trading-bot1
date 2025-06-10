import telegram

# Chat ID del tuo gruppo Telegram
CHAT_ID = -1002114553796

def handle_update(update, bot):
    if update.message and update.message.text:
        text = update.message.text.lower()

        if text == "/start":
            bot.send_message(chat_id=update.message.chat.id, text="Bot attivo ✅")

        elif text == "/segnale":
            send_segnale_demo(bot)

    elif update.callback_query:
        query = update.callback_query
        if query.data == "conferma_si":
            bot.send_message(chat_id=query.message.chat.id, text="✅ Segnale confermato.")
        elif query.data == "conferma_no":
            bot.send_message(chat_id=query.message.chat.id, text="❌ Segnale ignorato.")

def send_segnale_demo(bot):
    keyboard = [
        [telegram.InlineKeyboardButton("SÌ", callback_data='conferma_si')],
        [telegram.InlineKeyboardButton("NO", callback_data='conferma_no')]
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "📈 Segnale pronto (SIMULAZIONE)\n"
            "Strumento: BTC/USDT\n"
            "Operazione: COMPRA\n"
            "Prezzo di ingresso: 67.200\n"
            "🎯 TP: 67.900\n"
            "🛑 SL: 66.750\n\n"
            "Vuoi che lo eseguo per te?"
        ),
        reply_markup=reply_markup
    )
