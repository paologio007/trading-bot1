from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from flask import Flask
from threading import Thread

# Bot token
TOKEN = "7257421165:AAGfkQ7jydVeS8WVrixCEb7diUnhHIF30ls"

# Keep-alive con Flask per Render
app = Flask('')

@app.route('/')
def home():
    return "Bot attivo!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# Comando /start
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot avviato!")

# Gestione messaggi (parser segnali)
def handle_message(update: Update, context: CallbackContext):
    message = update.message.text.strip()
    print(f"Messaggio ricevuto: {message}")

    parts = message.upper().split()

    if len(parts) == 3 and parts[0] in ['BUY', 'SELL'] and 'X' in parts[2].upper():
        action = parts[0]
        symbol = parts[1].replace('/', '').upper()
        leverage = parts[2].lower().replace('x', '')

        print(f"Segnale valido → Azione: {action}, Symbol: {symbol}, Leva: {leverage}x")

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"📈 Segnale ricevuto:\n▶️ {action}\n💱 {symbol}\n⚙️ Leverage: {leverage}x")
    else:
        print("Messaggio ignorato: non è un segnale valido.")

# Avvio bot
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    keep_alive()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
