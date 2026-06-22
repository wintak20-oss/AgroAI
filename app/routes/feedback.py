from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models import Feedback
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/feedback", tags=["Feedback"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# SUBMIT FEEDBACK
# =========================
@router.post("/")
def send_feedback(
    message: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    feedback = Feedback(
        user_email=user["email"],
        message=message,
        created_at=datetime.utcnow()
    )

    db.add(feedback)
    db.commit()

    return {"message": "Feedback submitted successfully"}