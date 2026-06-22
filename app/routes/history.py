from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Prediction
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/history", tags=["History"])


# =========================
# DB SESSION
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 📜 USER PREDICTION HISTORY
# =========================
@router.get("/")
def get_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    limit: int = Query(50, ge=1, le=200)
):

    history = db.query(Prediction).filter(
        Prediction.user_email == user["email"]
    ).order_by(
        Prediction.created_at.desc()
    ).limit(limit).all()

    return [
        {
            "id": h.id,
            "disease": h.disease,
            "confidence": h.confidence,
            "created_at": h.created_at
        }
        for h in history
    ]


# =========================
# 🔍 FILTER HISTORY
# =========================
@router.get("/search")
def search_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    disease: str = None
):

    query = db.query(Prediction).filter(
        Prediction.user_email == user["email"]
    )

    if disease:
        query = query.filter(Prediction.disease == disease)

    results = query.all()

    return {
        "count": len(results),
        "data": results
    }