from sqlalchemy import (
Column,
Integer,
String,
Float,
DateTime,
ForeignKey,
Boolean
)

from datetime import datetime

from app.database import Base

class Prediction(Base):
**tablename** = "predictions"

```
# =========================
# PRIMARY KEY
# =========================
id = Column(
    Integer,
    primary_key=True,
    index=True
)

# =========================
# USER
# =========================
user_email = Column(
    String,
    index=True,
    nullable=False
)

# =========================
# FARM
# =========================
farm_id = Column(
    Integer,
    ForeignKey("farms.id"),
    index=True,
    nullable=True
)

# =========================
# AI RESULT
# =========================
disease = Column(
    String,
    nullable=False
)

confidence = Column(
    Float,
    nullable=False
)

image_path = Column(
    String,
    nullable=True
)

# =========================
# AGRICULTURE
# =========================
crop_name = Column(
    String,
    nullable=True
)

region = Column(
    String,
    nullable=True
)

# =========================
# QUALITY CONTROL
# =========================
verified = Column(
    Boolean,
    default=False
)

# =========================
# TIMESTAMP
# =========================
created_at = Column(
    DateTime,
    default=datetime.utcnow
)
```
