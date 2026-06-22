import random
import time

OTP_STORE = {}  # replace with Redis later
OTP_EXPIRY = 300

def generate_otp(phone: str):
    otp = str(random.randint(100000, 999999))

    OTP_STORE[phone] = {
        "otp": otp,
        "time": time.time()
    }

    return otp


def verify_otp(phone: str, otp: str):
    record = OTP_STORE.get(phone)

    if not record:
        return False

    if time.time() - record["time"] > OTP_EXPIRY:
        return False

    return record["otp"] == otp