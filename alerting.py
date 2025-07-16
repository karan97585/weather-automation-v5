# alerting.py ✅ Error Logging + Email Alert

import logging
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def log_error(message):
    logging.error(f"❌ {message}")
    send_email_alert(message)

def send_email_alert(message):
    try:
        msg = EmailMessage()
        msg.set_content(f"🚨 Weather Script Error:\n\n{message}")
        msg["Subject"] = "Weather Automation Alert"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        logging.error(f"❌ Failed to send alert email: {e}")
