MESSAGES = {
    "en": {
        "login_success": "Login successful",
        "otp_sent": "OTP sent successfully",
        "invalid_otp": "Invalid OTP"
    },
    "ti": {
        "login_success": "ናብ ስርዓት ብዓወት ኣትዩ",
        "otp_sent": "OTP ተላኢኹ",
        "invalid_otp": "ዘይቅኑዕ OTP"
    },
    "am": {
        "login_success": "በትክክል ገብተዋል",
        "otp_sent": "OTP ተልኳል",
        "invalid_otp": "ልክ ያልሆነ OTP"
    }
}

def get_message(lang: str, key: str):
    return MESSAGES.get(lang, MESSAGES["en"]).get(key, key)