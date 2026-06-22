from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    user_email = Column(String, index=True)
    farm_id = Column(Integer, index=True)

    disease = Column(String)
    confidence = Column(Float)
    image_path = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)