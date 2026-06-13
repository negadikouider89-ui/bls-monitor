import requests
import os
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BLS_URL = "https://algeria.blsspainglobal.com/dza/appointment/newappointment"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Accept-Language": "fr-FR,fr;q=0.9",
}

GOOD = ["datepicker","calendar","select date","available","book","reserver"]
BAD = ["no appointment","not available","complet","aucun","fully booked"]

def send(msg, alert=False):
    try:
        data = {
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML"
        }
        if alert:
            data["disable_notification"] = False
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data=data,
            timeout=10
        )
    except Exception as e:
        print(e)

def alert_user():
    msg = (
        "🚨🚨🚨 موعد متاح الآن! 🚨🚨🚨\n\n"
        "⚡ احجز فوراً قبل أن يختفي!\n\n"
        "🔗 " + BLS_URL
    )
    for i in range(5):
        send(msg, alert=True)
        time.sleep(3)

def check():
    try:
        r = requests.get(BLS_URL, headers=HEADERS, timeout=20)
        html = r.text.lower()
        good = [k for k in GOOD if k in html]
        bad = [k for k in BAD if k in html]
        if good and not bad:
            alert_user()
        elif bad:
            send("🔴 لا توجد مواعيد - " + time.strftime("%H:%M UTC"))
        else:
            send("✅ فحص - Size: " + str(len(html)))
    except Exception as e:
        send("❌ خطأ: " + str(e))

check()

