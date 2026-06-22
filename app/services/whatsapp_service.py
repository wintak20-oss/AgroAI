import os
import requests


WHATSAPP_API = "https://api.callmebot.com/whatsapp.php"

API_KEY = os.getenv("CALLMEBOT_API_KEY")


def send_whatsapp(phone: str, message: str):
    """
    Production-safe WhatsApp sender using CallMeBot API
    """

    if not API_KEY:
        return {
            "success": False,
            "error": "CALLMEBOT_API_KEY is missing"
        }

    try:
        url = (
            f"{WHATSAPP_API}"
            f"?phone={phone}"
            f"&text={message}"
            f"&apikey={API_KEY}"
        )

        response = requests.get(url, timeout=10)

        # CallMeBot usually returns plain text response
        if response.status_code == 200:
            return {
                "success": True,
                "response": response.text
            }

        return {
            "success": False,
            "status_code": response.status_code,
            "response": response.text
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }