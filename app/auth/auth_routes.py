from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import User, RefreshTokenSession
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

from app.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    RefreshRequest
)

router = APIRouter()


# =========================
# DB
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# REGISTER
# =========================
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(
        (User.email == data.email) | (User.phone == data.phone)
    ).first()

    if existing:
        raise HTTPException(400, "User already exists")

    user = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password=hash_password(data.password),
        role="farmer",
        is_verified=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"success": True, "message": "User created"}


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    if not user.is_verified:
        raise HTTPException(403, "Account not verified")

    access = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    refresh = create_refresh_token({
        "sub": user.email,
        "type": "refresh"
    })

    session = RefreshTokenSession(
        user_email=user.email,
        refresh_token=refresh,
        expires_at=datetime.utcnow() + timedelta(days=7),
        revoked=False
    )

    db.add(session)
    db.commit()

    return {
        "success": True,
        "access_token": access,
        "refresh_token": refresh,
        "role": user.role
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

    new_access = create_access_token({
        "sub": payload["sub"],
        "role": payload.get("role", "farmer")
    })

    return {"access_token": new_access}


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