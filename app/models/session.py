from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database import Base


class RefreshTokenSession(Base):
    __tablename__ = "refresh_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_email = Column(String(100), index=True)
    refresh_token = Column(String(500), unique=True)

    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)