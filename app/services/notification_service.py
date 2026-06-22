import requests
import os

WHATSAPP_API = "https://api.callmebot.com/whatsapp.php"


def send_whatsapp(phone: str, message: str):
    url = f"{WHATSAPP_API}?phone={phone}&text={message}&apikey={os.getenv('WHATSAPP_KEY')}"
    requests.get(url)


def send_sms(phone: str, message: str):
    # placeholder for Twilio / AWS SNS
    print(f"SMS to {phone}: {message}")


def notify_user(phone: str, message: str):
    send_whatsapp(phone, message)
    send_sms(phone, message)