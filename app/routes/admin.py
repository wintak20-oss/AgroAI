```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.database import SessionLocal
from app.models import User, Prediction
from app.auth.dependencies import require_admin
from app.schemas.admin import RoleUpdate

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# =====================================
# DATABASE
# =====================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================
# ADMIN DASHBOARD
# =====================================

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    total_users = db.query(User).count()

    total_farmers = db.query(User).filter(
        User.role == "farmer"
    ).count()

    total_experts = db.query(User).filter(
        User.role == "expert"
    ).count()

    total_admins = db.query(User).filter(
        User.role == "admin"
    ).count()

    active_users = db.query(User).filter(
        User.is_active.is_(True)
    ).count()

    inactive_users = db.query(User).filter(
        User.is_active.is_(False)
    ).count()

    verified_users = db.query(User).filter(
        User.is_verified.is_(True)
    ).count()

    total_predictions = db.query(
        Prediction
    ).count()

    disease_distribution = db.query(
        Prediction.disease_name,
        func.count(Prediction.id)
    ).group_by(
        Prediction.disease_name
    ).all()

    return {
        "total_users": total_users,
        "total_farmers": total_farmers,
        "total_experts": total_experts,
        "total_admins": total_admins,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "verified_users": verified_users,
        "total_predictions": total_predictions,
        "disease_distribution": [
            {
                "disease": disease,
                "count": count
            }
            for disease, count in disease_distribution
        ]
    }


# =====================================
# GET USERS
# =====================================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
    search: str = "",
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    query = db.query(User)

    if search:
        query = query.filter(
            or_(
                User.email.contains(search),
                User.name.contains(search)
            )
        )

    total = query.count()

    users = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": getattr(user, "phone", None),
                "role": user.role,
                "is_active": user.is_active,
                "is_verified": user.is_verified
            }
            for user in users
        ]
    }


# =====================================
# USER DETAILS
# =====================================

@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified
    }


# =====================================
# VERIFY USER
# =====================================

@router.put("/users/{user_id}/verify")
def verify_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_verified = True

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "User verified"
    }


# =====================================
# UPDATE ROLE
# =====================================

@router.put("/users/{user_id}/role")
def update_role(
    user_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    allowed_roles = [
        "farmer",
        "expert",
        "admin"
    ]

    if data.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    admin_count = db.query(User).filter(
        User.role == "admin"
    ).count()

    if (
        user.role == "admin"
        and data.role != "admin"
        and admin_count <= 1
    ):
        raise HTTPException(
            status_code=400,
            detail="System must have at least one admin"
        )

    user.role = data.role

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "new_role": data.role
    }


# =====================================
# ACTIVATE USER
# =====================================

@router.put("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_active = True

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "User activated"
    }


# =====================================
# SUSPEND USER
# =====================================

@router.put("/users/{user_id}/suspend")
def suspend_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_active = False

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "User suspended"
    }


# =====================================
# DELETE USER
# =====================================

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account"
        )

    admin_count = db.query(User).filter(
        User.role == "admin"
    ).count()

    if (
        user.role == "admin"
        and admin_count <= 1
    ):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete the last admin"
        )

    db.delete(user)
    db.commit()

    return {
        "success": True,
        "message": "User deleted successfully"
    }


# =====================================
# OVERVIEW
# =====================================

@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    total_users = db.query(User).count()

    total_predictions = db.query(
        Prediction
    ).count()

    latest_user = db.query(
        User
    ).order_by(
        User.id.desc()
    ).first()

    roles = db.query(
        User.role,
        func.count(User.id)
    ).group_by(
        User.role
    ).all()

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "latest_user": (
            latest_user.email
            if latest_user
            else None
        ),
        "roles": {
            role: count
            for role, count in roles
        }
    }
```
