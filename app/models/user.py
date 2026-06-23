from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # BASIC INFO
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    # AUTH
    password = Column(String, nullable=False)

    # 🔥 ROLE SYSTEM
    role = Column(String, default="farmer")  # farmer | admin

    # STATUS
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)