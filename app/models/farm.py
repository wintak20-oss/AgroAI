from sqlalchemy import (
Column,
Integer,
String,
Float,
DateTime
)

from datetime import datetime

from app.database import Base

class Farm(Base):
**tablename** = "farms"

```
id = Column(
    Integer,
    primary_key=True,
    index=True
)

# =========================
# FARM INFO
# =========================

name = Column(
    String,
    nullable=False
)

owner_email = Column(
    String,
    index=True,
    nullable=False
)

crop_name = Column(
    String,
    nullable=True
)

farm_size_hectares = Column(
    Float,
    default=0
)

# =========================
# LOCATION
# =========================

country = Column(
    String,
    default="Ethiopia"
)

region = Column(
    String,
    nullable=True
)

zone = Column(
    String,
    nullable=True
)

district = Column(
    String,
    nullable=True
)

village = Column(
    String,
    nullable=True
)

latitude = Column(
    Float,
    nullable=True
)

longitude = Column(
    Float,
    nullable=True
)

# =========================
# METADATA
# =========================

created_at = Column(
    DateTime,
    default=datetime.utcnow
)
```
