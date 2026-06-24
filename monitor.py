import requests
import os
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

CITIES = {
    "Oran": "https://algeria.blsspainglobal.com/dza/appointment/newappointment?location=oran",
    "Alger": "https://algeria.blsspainglobal.com/dza/appointment/newappointment?location=alger",
    "Constantine": "https://algeria.blsspainglobal.com/dza/appointment/newappointment?location=constantine",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Accept-Language": "fr-FR,fr;q=0.9",
}

GOOD = ["datepicker","calendar","select date","available","book","reserver"]
BAD = ["no appointment","not available","complet","aucun","fully booked"]

def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except Exception as e:
        print(e)

def alert(city, url):
    msg = (
        f"🚨🚨🚨 موعد متاح في {city}!\n\n"
        f"⚡ احجز فوراً!\n\n"
        f"🔗 {url}"
    )
    for i in range(5):
        send(msg)
        time.sleep(3)

def check():
    results = []
    for city, url in CITIES.items():
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            html = r.text.lower()
            good = [k for k in GOOD if k in html]
            bad = [k for k in BAD if k in html]
            if good and not bad:
                alert(city, url)
            else:
                results.append(f"🔴 {city}: لا يوجد ({len(html)})")
        except Exception as e:
            results.append(f"❌ {city}: خطأ")
    send("\n".join(results))

check()

