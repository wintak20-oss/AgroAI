from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    phone = Column(String, unique=True)

    password = Column(String, nullable=False)

    role = Column(String, default="farmer")

    is_verified = Column(Boolean, default=False)

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)