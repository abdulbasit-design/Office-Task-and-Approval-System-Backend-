from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)

    email = Column(String(255), nullable=False, unique=True, index=True)

    password_hash = Column(String, nullable=False)

    role = Column(String(30), nullable=False)

    department_id = Column(
        BigInteger,
        ForeignKey("departments.id"),
        nullable=True
    )

    manager_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    joined_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
