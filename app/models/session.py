from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import Base
import datetime


class RefreshTokenSession(Base):
    __tablename__ = "refresh_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)