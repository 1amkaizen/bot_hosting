# bot/handlers.py
from .telegram_api import send_message
from .state import user_state
from django.conf import settings
from data_hosting import HOSTING_OPTIONS

def handle_message(data):
    if "message" not in data:
        return

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    user_id = chat_id
    state = user_state.get(user_id, {})

    if text == "/start":
        start_text = (
            "👋 *Selamat datang di Bot Hosting Zen!*\n\n"
            "🚀 Kami siap membantumu memilih paket hosting terbaik untuk website, aplikasi, atau proyek digitalmu.\n\n"
            "📦 Mulai dengan perintah /paket untuk melihat pilihan.\n"
            "🆘 Perlu bantuan? Ketik /help ya!"
        )
        send_message(chat_id, start_text, parse_mode="Markdown")

    elif text == "/help":
        help_text = (
            "📚 *Panduan Penggunaan Bot Hosting*\n\n"
            "🔹 /start – Memulai ulang bot\n"
            "🔹 /paket – Lihat pilihan hosting\n"
            "🔹 /help – Bantuan penggunaan bot\n\n"
            "📬 _Hubungi admin jika butuh panduan lebih lanjut._"
        )
        send_message(chat_id, help_text, parse_mode="Markdown")

    elif text == "/paket":
        user_state[user_id] = {"step": "jenis"}
        keyboard = {
            "keyboard": [
                ["🌐 Web Hosting", "📦 VPS Hosting"],
                ["☁️ Cloud Hosting"]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True,
            "input_field_placeholder": "Pilih jenis hosting..."
        }
        send_message(chat_id, "🛠️ *Langkah 1:* Pilih jenis hosting yang kamu butuhkan:", parse_mode="Markdown", reply_markup=keyboard)

    elif state.get("step") == "jenis":
        # Hapus emoji sebelum dicocokkan
        clean_text = text.replace("🌐", "").replace("📦", "").replace("☁️", "").strip()
        if clean_text in HOSTING_OPTIONS:
            user_state[user_id] = {"step": "durasi", "jenis": clean_text}
            durations = list(HOSTING_OPTIONS[clean_text].keys())
            keyboard = {
                "keyboard": [[f"⏳ {d}"] for d in durations],
                "resize_keyboard": True,
                "one_time_keyboard": True,
                "input_field_placeholder": "Pilih durasi paket..."
            }
            send_message(
                chat_id,
                f"📅 *Langkah 2:* Pilih durasi paket untuk *{clean_text}* hosting:",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            send_message(chat_id, "❗ Jenis hosting tidak dikenali. Silakan pilih dari tombol yang tersedia.")

    elif state.get("step") == "durasi":
        jenis = state.get("jenis")
        clean_text = text.replace("⏳", "").strip()
        if jenis and clean_text in HOSTING_OPTIONS[jenis]:
            paket_list = HOSTING_OPTIONS[jenis][clean_text]
            for paket in paket_list:
                fitur_text = "\n".join([f"🔹 {f}" for f in paket["fitur"]])
                response = (
                    f"🎁 *{paket.get('nama', jenis)}* – {clean_text}\n\n"
                    f"💰 *Harga:* `{paket['harga']}`\n"
                    f"🛠️ *Fitur:*\n{fitur_text}"
                )
                button_markup = {
                    "inline_keyboard": [
                        [
                            {
                                "text": "🛒 Beli Sekarang",
                                "url": paket["link"]
                            }
                        ]
                    ]
                }
                send_message(chat_id, response, parse_mode="Markdown", reply_markup=button_markup)
            user_state[user_id] = {"step": None}
        else:
            send_message(chat_id, "⚠️ Durasi tidak sesuai. Silakan pilih dari opsi yang tersedia.")

    else:
        send_message(chat_id, "🤖 Perintah tidak dikenali.\nCoba /start untuk memulai atau /help untuk bantuan.")

