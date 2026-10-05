from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base
from app.models.user_model import User


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

    creator = relationship("User", foreign_keys=[created_by], lazy="joined")
    assignee = relationship("User", foreign_keys=[assigned_to], lazy="joined")
    approver = relationship("User", foreign_keys=[approved_by], lazy="joined")

    @property
    def assigned_to_name(self) -> str | None:
        return self.assignee.full_name if self.assignee else None

    @property
    def created_by_name(self) -> str | None:
        return self.creator.full_name if self.creator else None

    @property
    def approved_by_name(self) -> str | None:
        return self.approver.full_name if self.approver else None

    @property
    def department_name(self) -> str | None:
        if self.assignee and self.assignee.department:
            return self.assignee.department.name
        return None
