

```python
import requests
import os
import time

# Config
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BLS_URL = "https://algeria.blsspainglobal.com/dza/appointment/newappointment"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8,ar;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

GOOD_KEYWORDS = [
    "appointment available",
    "book appointment",
    "select date",
    "choose date",
    "datepicker",
    "calendar",
    "available slot",
    "rendez-vous disponible",
    "créneau disponible",
    "réserver",
    "book now",
]

BAD_KEYWORDS = [
    "no appointment available",
    "not available",
    "fully booked",
    "aucun rendez-vous",
    "no slots available",
    "complet",
    "unavailable",
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=data, timeout=10)
        print(f"Telegram sent: {r.status_code}")
    except Exception as e:
        print(f"Telegram error: {e}")

def check_bls():
    print("Checking BLS website...")
    try:
        r = requests.get(BLS_URL, headers=HEADERS, timeout=20)
        html = r.text.lower()
        size = len(html)
        status = r.status_code
        print(f"Response: {status}, Size: {size} chars")

        found_good = [k for k in GOOD_KEYWORDS if k in html]
        found_bad  = [k for k in BAD_KEYWORDS  if k in html]

        print(f"Good keywords found: {found_good}")
        print(f"Bad keywords found: {found_bad}")

        if found_good and not found_bad:
            msg = (
                "🎉 APPOINTMENT AVAILABLE!\n\n"
                f"Detected: {', '.join(found_good)}\n\n"
                "Book NOW before it's gone!\n"
                f"🔗 {BLS_URL}"
            )
            send_telegram(msg)
            time.sleep(5)
            send_telegram(msg)
            time.sleep(5)
            send_telegram(msg)
            return True
        elif found_bad:
            print("No appointments available")
            send_telegram(f"🔴 No appointments yet. Checked: {time.strftime('%H:%M UTC')}")
            return False
        else:
            preview = r.text[:200].replace('<','').replace('>','')
            send_telegram(f"⚠️ Inconclusive\nStatus: {status} | Size: {size}\n{preview}")
            return False

    except Exception as e:
        print(f"Error: {e}")
        send_telegram(f"❌ Check failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== BLS Spain Monitor - Oran ===")
    check_bls()
```

انسخه كاملاً والصقه، ثم اضغط **"Commit changes"** ✅
