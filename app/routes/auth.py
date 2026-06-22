from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, RefreshTokenSession
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.auth.schemas import RegisterRequest, LoginRequest, RefreshRequest

router = APIRouter()


# =========================
# REGISTER
# =========================
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "User already exists")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role="farmer"
    )

    db.add(user)
    db.commit()
    return {"message": "User created"}


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    access = create_access_token({"sub": user.email, "role": user.role})
    refresh = create_refresh_token({"sub": user.email})

    session = RefreshTokenSession(
        user_email=user.email,
        refresh_token=refresh,
        expires_at=datetime.utcnow() + timedelta(days=7),
        revoked=False
    )

    db.add(session)
    db.commit()

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


# =========================
# REFRESH
# =========================
@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):

    payload = decode_token(data.token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")

    session = db.query(RefreshTokenSession).filter(
        RefreshTokenSession.refresh_token == data.token,
        RefreshTokenSession.revoked == False
    ).first()

    if not session:
        raise HTTPException(401, "Session expired")

    return {
        "access_token": create_access_token({"sub": payload["sub"]})
    }


# =========================
# LOGOUT
# =========================
@router.post("/logout")
def logout(data: RefreshRequest, db: Session = Depends(get_db)):

    session = db.query(RefreshTokenSession).filter(
        RefreshTokenSession.refresh_token == data.token
    ).first()

    if session:
        session.revoked = True
        db.commit()

    return {"message": "Logged out"}