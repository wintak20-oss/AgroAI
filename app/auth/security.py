from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings

# =========================
# PASSWORD HASHING
# =========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# =========================
# TOKEN CREATION (ACCESS)
# =========================
def create_access_token(data: dict, expires_minutes: int = None):
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# =========================
# TOKEN CREATION (REFRESH)
# =========================
def create_refresh_token(data: dict):
    payload = data.copy()

    payload.update({
        "exp": datetime.utcnow() + timedelta(days=7),
        "type": "refresh"
    })

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# =========================
# DECODE TOKEN
# =========================
def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None


# =========================
# ROLE CHECKER (SAAS CORE)
# =========================
def require_role(user: dict, allowed_roles: list):
    role = user.get("role", "farmer")

    if role not in allowed_roles:
        return False
    return True


# =========================
# CURRENT USER (FIXED FOR FASTAPI)
# =========================
def get_current_user(token: str):
    payload = decode_token(token)

    if not payload:
        return None

    return {
        "email": payload.get("sub"),
        "role": payload.get("role", "farmer")
    }