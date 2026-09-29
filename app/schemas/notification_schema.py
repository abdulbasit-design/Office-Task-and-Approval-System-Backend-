from pydantic import BaseModel
from datetime import datetime


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    task_id: int | None
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    read_at: datetime | None

    model_config = {
        "from_attributes": True
    }
