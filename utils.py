from telegram import Update
from telegram.ext import ContextTypes

# Funzione per gestire il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Bot avviato!")

# Funzione per gestire ogni altro messaggio ricevuto (es. segnali di trading)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"📩 Messaggio ricevuto: {text}")
    # Qui puoi aggiungere il parsing e le azioni per il segnale
