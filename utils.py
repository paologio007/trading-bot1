import telegram

CHAT_ID = -1002252372969

def handle_update(update, bot):
    if update.message and update.message.text:
        txt = update.message.text.lower()

        if txt == "/start":
            bot.send_message(chat_id=update.message.chat.id,
                             text="Bot attivo ✅")

        elif txt == "/segnale":
            send_segnale_demo(bot)

    elif update.callback_query:
        q = update.callback_query
        if q.data == "conferma_si":
            bot.send_message(chat_id=q.message.chat.id,
                             text="✅ Segnale confermato.")
        elif q.data == "conferma_no":
            bot.send_message(chat_id=q.message.chat.id,
                             text="❌ Segnale ignorato.")

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
            "Vuoi che lo eseguo per te?"
        ),
        reply_markup=telegram.InlineKeyboardMarkup(keyboard)
    )
