import requests
import os

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(URL)
print(response.json())
