from pushbullet import Pushbullet
import time
from database import collection

# ================= PUSHBULLET =================
import os&#10;API_KEY = os.getenv('PUSHBULLET_API_KEY')
pb = Pushbullet(API_KEY)

# ================= ALERT CONTROL =================
last_alert_time = 0
ALERT_INTERVAL = 15  # seconds (anti-spam)

# ================= ALERT FUNCTION =================
def send_alert(message):
    global last_alert_time
    current_time = time.time()

    # Anti-spam
    if current_time - last_alert_time < ALERT_INTERVAL:
        return

    last_alert_time = current_time

    print("🚨 ALERT:", message)

    # 📱 Pushbullet notification
    try:
        pb.push_note("🚗 Smart Drive AI Alert", message)
    except Exception as e:
        print("❌ Pushbullet error:", e)

    # 🗄️ Save to MongoDB
    try:
        collection.insert_one({
            "message": message,
            "timestamp": time.time()
        })
    except Exception as e:
        print("❌ MongoDB error:", e)
