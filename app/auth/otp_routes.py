from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth.otp_service import generate_otp, verify_otp
from app.auth.security import create_access_token, create_refresh_token
from app.models import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/send-otp")
def send_otp(phone: str):

    otp = generate_otp(phone)
    print(f"OTP: {otp}")

    return {"message": "OTP sent"}


@router.post("/verify-otp")
def verify(phone: str, otp: str, db: Session = Depends(get_db)):

    ok, msg = verify_otp(phone, otp)

    if not ok:
        raise HTTPException(401, msg)

    user = db.query(User).filter(User.phone == phone).first()

    if not user:
        user = User(phone=phone, role="farmer", is_verified=True)
        db.add(user)
        db.commit()

    access = create_access_token({"sub": phone, "role": user.role})
    refresh = create_refresh_token({"sub": phone, "type": "refresh"})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "role": user.role
    }