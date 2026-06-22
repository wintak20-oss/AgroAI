from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models import Prediction
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/sync", tags=["Sync"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# OFFLINE PREDICTIONS SYNC
# =========================
@router.post("/predictions")
def sync_predictions(
    data: list[dict],
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    saved = 0

    for item in data:
        prediction = Prediction(
            user_email=user["email"],
            disease=item.get("disease"),
            confidence=item.get("confidence"),
            created_at=datetime.utcnow()
        )
        db.add(prediction)
        saved += 1

    db.commit()

    return {
        "message": "Sync successful",
        "saved_records": saved
    }