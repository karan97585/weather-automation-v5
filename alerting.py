# alerting.py

import logging
import requests
# from smtplib import SMTP  # (Optional: for email alerts)

# Setup logging
logging.basicConfig(
    filename='weather_log.log',
    level=logging.ERROR,
    format='%(asctime)s - ERROR - %(message)s'
)

def log_error(message):
    """
    Logs the error to a file and prints it to console.
    """
    logging.error(f"❌ {message}")
    print(f"[❌ ERROR] {message}")

    # Optional future alerts (currently disabled)
    # send_webhook_alert(message)
    # send_email_alert(message)

# -------------------------------
# ✅ Optional Webhook Alert Setup
# -------------------------------
def send_webhook_alert(message):
    webhook_url = "https://your-webhook-url.com"  # replace if needed
    payload = {"text": f"⚠️ Weather Alert: {message}"}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            logging.error(f"Webhook failed: {response.status_code}")
    except Exception as e:
        logging.error(f"Webhook exception: {e}")

# -------------------------------
# ✅ Optional Email Alert Setup
# -------------------------------
# def send_email_alert(message):
#     # Future implementation if needed
#     pass
