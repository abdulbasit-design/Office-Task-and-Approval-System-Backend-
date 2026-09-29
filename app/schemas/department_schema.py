from pydantic import BaseModel, Field
from datetime import datetime


class DepartmentCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )

    description: str | None = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
