from fastapi import APIRouter, HTTPException
from app.auth.otp_service import generate_otp, verify_otp
from app.auth.security import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/send")
def send_otp(phone: str):

    otp = generate_otp(phone)
    print(f"OTP {phone}: {otp}")  # replace with SMS/WhatsApp

    return {"message": "OTP sent"}


@router.post("/verify")
def verify(phone: str, otp: str, role: str = "farmer"):

    if not verify_otp(phone, otp):
        raise HTTPException(401, "Invalid OTP")

    return {
        "access_token": create_access_token({"sub": phone, "role": role}),
        "refresh_token": create_refresh_token({"sub": phone}),
        "role": role
    }