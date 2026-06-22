from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models import User, Prediction
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


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
# 👥 GET ALL USERS (SAFE PAGINATION)
# =========================
@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):

    users = db.query(User).offset(offset).limit(limit).all()

    return {
        "count": len(users),
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role,
            }
            for u in users
        ]
    }


# =========================
# 🔁 UPDATE USER ROLE
# =========================
@router.put("/users/{user_id}/role")
def update_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    allowed_roles = ["farmer", "admin", "expert"]

    if role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Allowed: {allowed_roles}"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role
    db.commit()

    return {
        "success": True,
        "message": "Role updated successfully",
        "user_id": user_id,
        "new_role": role
    }


# =========================
# ❌ DELETE USER
# =========================
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {
        "success": True,
        "message": "User deleted",
        "user_id": user_id
    }


# =========================
# 📊 SYSTEM OVERVIEW (SAAS KPI)
# =========================
@router.get("/overview")
def system_overview(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    total_users = db.query(User).count()
    total_predictions = db.query(Prediction).count()

    role_distribution = db.query(
        User.role,
        func.count(User.id)
    ).group_by(User.role).all()

    latest_user = db.query(User).order_by(User.id.desc()).first()

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "role_distribution": {
            r: c for r, c in role_distribution
        },
        "latest_user": latest_user.email if latest_user else None
    }