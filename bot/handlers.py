# bot/handlers.py
from .telegram_api import send_message
from .state import user_state
from django.conf import settings
import requests
from data_hosting import HOSTING_OPTIONS  # 🔥 ambil dari file terpisah


def handle_message(data):
    if "message" not in data:
        return

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    user_id = chat_id
    state = user_state.get(user_id, {})

    if text == "/start":
        start_text = (
            "Halo! Selamat datang di layanan hosting kami.\n"
            "Pilihan paket hosting terbaik mulai 5 ribu\n\n"
        )
        send_message(chat_id, start_text, parse_mode="Markdown")

    elif text == "/help":
        help_text = (
            "🤖 *Panduan Bot Hosting*\n\n"
            "/start - Memulai pemilihan paket hosting\n"
            "/paket - Memilih paket hosting\n"
            "/help - Menampilkan pesan bantuan ini\n\n"
        )
        send_message(chat_id, help_text, parse_mode="Markdown")

    elif text == "/paket":
        user_state[user_id] = {"step": "jenis"}
        keyboard = {
            "keyboard": [["Web Hosting", "VPS Hosting", "Cloud Hosting"]],
            "one_time_keyboard": True,
            "resize_keyboard": True
        }
        send_message(chat_id, "Silakan pilih jenis hosting:", reply_markup=keyboard)

    elif state.get("step") == "jenis":
        if text in HOSTING_OPTIONS:
            user_state[user_id] = {"step": "durasi", "jenis": text}
            durations = list(HOSTING_OPTIONS[text].keys())
            keyboard = {
                "keyboard": [[d] for d in durations],
                "one_time_keyboard": True,
                "resize_keyboard": True
            }
            send_message(chat_id, "Pilih durasi paket:", reply_markup=keyboard)
        else:
            send_message(chat_id, "Mohon pilih jenis hosting yang valid.")

    elif state.get("step") == "durasi":
        jenis = state.get("jenis")
        if jenis and text in HOSTING_OPTIONS[jenis]:
            paket_list = HOSTING_OPTIONS[jenis][text]
            for paket in paket_list:
                fitur_text = "\n".join([f"• {f}" for f in paket["fitur"]])
                response = (
                    f"📦 *{paket.get('nama', jenis)}* - {text}\n\n"
                    f"💰 Harga: {paket['harga']}\n"
                    f"🔧 Fitur:\n{fitur_text}\n"
                    f"🔗 [Klik untuk beli]({paket['link']})"
                )
                send_message(chat_id, response, parse_mode="Markdown")
            user_state[user_id] = {"step": None}
        else:
            send_message(chat_id, "Mohon pilih durasi paket yang valid.")
    else:
        send_message(chat_id, "Ketik /start untuk memulai atau /help untuk bantuan.")

