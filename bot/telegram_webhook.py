# bot/telegram_webhook.py
import requests
from django.conf import settings

def set_telegram_webhook():
    webhook_url = settings.WEBHOOK_URL
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    response = requests.post(url, data={"url": webhook_url})
    
    if response.status_code == 200:
        print("[✅] Webhook set successfully!")
    else:
        print(f"[❌] Failed to set webhook: {response.text}")

