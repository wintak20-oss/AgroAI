from pydantic import BaseModel, EmailStr, Field

# =========================
# REGISTER
# =========================
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str | None = None


# =========================
# LOGIN
# =========================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


# =========================
# REFRESH TOKEN
# =========================
class RefreshRequest(BaseModel):
    token: str