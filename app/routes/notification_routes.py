from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user_model import User
from app.schemas.notification_schema import NotificationResponse
from app.controllers.notification_controller import (
    get_notifications_controller,
    get_notification_controller,
    mark_notification_as_read_controller
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get(
    "",
    response_model=list[NotificationResponse]
)
def get_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_notifications_controller(
        current_user,
        db
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse
)
def get_one_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_notification_controller(
        notification_id,
        current_user,
        db
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return mark_notification_as_read_controller(
        notification_id,
        current_user,
        db
    )
