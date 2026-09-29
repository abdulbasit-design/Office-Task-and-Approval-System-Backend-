from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Literal


class UserCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100
    )


class UserLogin(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=100
    )


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    department_id: int | None
    manager_id: int | None
    is_active: bool
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserAdminUpdate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    email: EmailStr

    role: Literal[
        "employee",
        "manager",
        "admin"
    ]

    department_id: int | None = None

    manager_id: int | None = None

    is_active: bool
