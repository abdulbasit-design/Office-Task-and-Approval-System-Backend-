from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None

    assigned_to: int

    deadline: datetime

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH"
    ]


class TaskUpdate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None

    assigned_to: int

    deadline: datetime

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH"
    ]


class TaskSubmit(BaseModel):
    submission_note: str | None = None


class TaskReject(BaseModel):
    rejection_reason: str = Field(
        min_length=1,
        max_length=1000
    )


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_by: int
    assigned_to: int
    deadline: datetime
    priority: str
    status: str
    submitted_at: datetime | None
    submission_note: str | None
    approved_at: datetime | None
    approved_by: int | None
    rejection_reason: str | None
    activity_log: list
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
