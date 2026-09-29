from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func

from app.config.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    created_by = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_to = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    deadline = Column(
        DateTime(timezone=True),
        nullable=False
    )

    priority = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="PENDING"
    )

    submitted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    submission_note = Column(
        Text,
        nullable=True
    )

    approved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    approved_by = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    rejection_reason = Column(
        Text,
        nullable=True
    )

    activity_log = Column(
        MutableList.as_mutable(JSONB),
        nullable=False,
        default=list
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
