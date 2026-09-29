from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func

from app.config.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
