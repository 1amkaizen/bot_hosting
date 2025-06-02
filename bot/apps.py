# bot/apps.py
from django.apps import AppConfig

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        from .telegram_webhook import set_telegram_webhook
        set_telegram_webhook()

