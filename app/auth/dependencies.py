from fastapi import Header, HTTPException, Depends, status
from app.auth.security import decode_token


# =========================
# 👤 CURRENT USER
# =========================
def get_current_user(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header"
        )

    try:
        token = authorization.split(" ")[1]
        payload = decode_token(token)

        if not payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {
            "email": payload.get("sub"),
            "role": payload.get("role", "user")
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )


# =========================
# 🔐 ADMIN ONLY GUARD
# =========================
def require_admin(user: dict = Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user