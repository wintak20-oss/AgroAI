from sqlalchemy import Column, Integer, String
from app.database import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    owner_email = Column(String, index=True)