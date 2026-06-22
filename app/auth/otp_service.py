import time
import random

OTP_STORE = {}

OTP_EXPIRY = 300
MAX_ATTEMPTS = 3


def generate_otp(phone: str):
    otp = str(random.randint(100000, 999999))

    OTP_STORE[phone] = {
        "otp": otp,
        "time": time.time(),
        "attempts": 0
    }

    return otp


def verify_otp(phone: str, otp: str):
    record = OTP_STORE.get(phone)

    if not record:
        return False, "OTP not found"

    if time.time() - record["time"] > OTP_EXPIRY:
        return False, "OTP expired"

    if record["attempts"] >= MAX_ATTEMPTS:
        return False, "Too many attempts"

    record["attempts"] += 1

    if record["otp"] != otp:
        return False, "Invalid OTP"

    return True, "Verified"