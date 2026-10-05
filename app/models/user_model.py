from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base
from app.models.department_model import Department


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

    department = relationship("Department", foreign_keys=[department_id], lazy="joined")

    @property
    def department_name(self) -> str | None:
        return self.department.name if self.department else None

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

    password_reset_status = Column(
        String(30),
        nullable=True,
        default=None
    )

    password_reset_requested_at = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )

    joined_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

