import os
import sys
import requests
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    btc_price  = data["bitcoin"]["usd"]
    btc_change = data["bitcoin"]["usd_24h_change"]
    eth_price  = data["ethereum"]["usd"]
    eth_change = data["ethereum"]["usd_24h_change"]

    return btc_price, btc_change, eth_price, eth_change

def format_change(change):
    if change >= 0:
        return f"🟢 +{change:.2f}%"
    else:
        return f"🔴 {change:.2f}%"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True
    }
    resp = requests.post(url, json=payload, timeout=10)
    result = resp.json()
    if result.get("ok"):
        print("تم الارسال بنجاح!")
    else:
        print(f"خطا: {result}")
        sys.exit(1)

if __name__ == "__main__":
    btc_price, btc_change, eth_price, eth_change = get_prices()

    # الوقت بتوقيت تركيا
    now = datetime.now(timezone(timedelta(hours=3))).strftime("%H:%M — %d/%m/%Y")

    message = (
        f"📊 تحديث الاسعار المباشر\n\n"
        f"₿ Bitcoin: ${btc_price:,.0f}\n"
        f"   {format_change(btc_change)} (24 ساعة)\n\n"
        f"⟠ Ethereum: ${eth_price:,.0f}\n"
        f"   {format_change(eth_change)} (24 ساعة)\n\n"
        f"🕐 اخر تحديث: {now}\n\n"
        f"🚀 للانضمام مجانا توصيات كريبتو weex\n"
        f"https://www.weex.com/register?vipCode=ub60\n\n"
        f"📲 للتسجيل في منصة bitget\n"
        f"https://partner.bitget.fit/bg/7hlx3w3x\n\n"
        f"💬 للدعم والاستفسار\n"
        f"https://t.me/abdoshahade1"
    )

    send_message(message)
