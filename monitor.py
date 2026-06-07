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

def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id":CHAT_ID,"text":msg},
            timeout=10
        )
    except Exception as e:
        print(e)

def check():
    try:
        r = requests.get(BLS_URL, headers=HEADERS, timeout=20)
        html = r.text.lower()
        good = [k for k in GOOD if k in html]
        bad = [k for k in BAD if k in html]
        if good and not bad:
            send("APPOINTMENT AVAILABLE! Book now: " + BLS_URL)
            time.sleep(5)
            send("APPOINTMENT AVAILABLE! Book now: " + BLS_URL)
        elif bad:
            send("No appointments yet. Checked: " + time.strftime("%H:%M UTC"))
        else:
            send("Check done. Size: " + str(len(html)))
    except Exception as e:
        send("Error: " + str(e))

check()

