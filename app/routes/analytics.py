from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from app.database import SessionLocal
from app.models import Prediction
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/analytics", tags=["Analytics"])


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
# 📊 DASHBOARD KPI
# =========================
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    total_predictions = db.query(Prediction).count()

    unique_users = db.query(
        func.count(func.distinct(Prediction.user_email))
    ).scalar() or 0

    avg_confidence = db.query(
        func.avg(Prediction.confidence)
    ).scalar() or 0

    return {
        "total_predictions": total_predictions,
        "unique_users": unique_users,
        "avg_confidence": round(float(avg_confidence), 2)
    }


# =========================
# 📈 DAILY TREND
# =========================
@router.get("/daily-trend")
def daily_trend(
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365),
    admin=Depends(require_admin)
):

    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    results = (
        db.query(
            func.date(Prediction.created_at),
            func.count(Prediction.id)
        )
        .filter(Prediction.created_at >= start_date)
        .group_by(func.date(Prediction.created_at))
        .order_by(func.date(Prediction.created_at))
        .all()
    )

    return {
        "labels": [str(r[0]) for r in results],
        "values": [r[1] for r in results]
    }


# =========================
# 🌿 DISEASE DISTRIBUTION
# =========================
@router.get("/disease-distribution")
def disease_distribution(
    db: Session = Depends(get_db),
    days: int = Query(30),
    limit: int = Query(10),
    admin=Depends(require_admin)
):

    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    results = (
        db.query(
            Prediction.disease,
            func.count(Prediction.id)
        )
        .filter(Prediction.created_at >= start_date)
        .group_by(Prediction.disease)
        .order_by(func.count(Prediction.id).desc())
        .limit(limit)
        .all()
    )

    return {
        "labels": [r[0] for r in results],
        "values": [r[1] for r in results]
    }


# =========================
# 🚀 GROWTH RATE
# =========================
@router.get("/growth")
def growth(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    now = datetime.now(timezone.utc)

    last_7 = now - timedelta(days=7)
    last_14 = now - timedelta(days=14)

    this_week = db.query(Prediction).filter(
        Prediction.created_at >= last_7
    ).count()

    last_week = db.query(Prediction).filter(
        Prediction.created_at >= last_14,
        Prediction.created_at < last_7
    ).count()

    growth_rate = 0.0
    if last_week > 0:
        growth_rate = ((this_week - last_week) / last_week) * 100

    return {
        "this_week": this_week,
        "last_week": last_week,
        "growth_rate_percent": round(growth_rate, 2)
    }


# =========================
# 🔥 SUMMARY
# =========================
@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
    days: int = Query(30),
    admin=Depends(require_admin)
):

    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    total = db.query(Prediction).filter(
        Prediction.created_at >= start_date
    ).count()

    unique_diseases = db.query(
        func.count(func.distinct(Prediction.disease))
    ).filter(
        Prediction.created_at >= start_date
    ).scalar() or 0

    latest = db.query(Prediction).order_by(
        Prediction.created_at.desc()
    ).first()

    return {
        "total_predictions": total,
        "unique_diseases_detected": unique_diseases,
        "latest_disease": latest.disease if latest else None,
        "time_range_days": days
    }