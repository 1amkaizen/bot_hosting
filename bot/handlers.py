from .telegram_api import send_message

def handle_telegram_update(data):
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message = data["message"].get("text", "")

        if message == "/start":
            reply = "Selamat datang di bot hosting kami!"
        else:
            reply = f"Kamu bilang: {message}"

        send_message(chat_id, reply)

