from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from datetime import datetime
from app.database import Base

class RefreshTokenSession(Base):
**tablename** = "refresh_sessions"

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
# USER INFO
# =========================
user_email = Column(
    String(100),
    index=True,
    nullable=False
)

# =========================
# TOKEN DATA
# =========================
refresh_token = Column(
    String(500),
    unique=True,
    index=True,
    nullable=False
)

# =========================
# SECURITY TRACKING
# =========================
revoked = Column(
    Boolean,
    default=False,
    nullable=False
)

device_info = Column(
    String(255),
    nullable=True
)

ip_address = Column(
    String(100),
    nullable=True
)

# =========================
# EXPIRATION
# =========================
expires_at = Column(
    DateTime,
    nullable=False
)

# =========================
# TIMESTAMP
# =========================
created_at = Column(
    DateTime,
    default=datetime.utcnow
)
```
