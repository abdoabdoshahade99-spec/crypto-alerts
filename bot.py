import os
import sys
import requests

# ==============================
# الإعدادات
# ==============================
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
MESSAGE   = os.environ["MESSAGE"]

# ==============================
# إرسال الرسالة إلى Telegram
# ==============================
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    resp = requests.post(url, json=payload, timeout=10)
    result = resp.json()

    if result.get("ok"):
        print("✅ تم الإرسال بنجاح!")
    else:
        print(f"❌ خطأ: {result}")
        sys.exit(1)

if __name__ == "__main__":
    send_message(MESSAGE)
