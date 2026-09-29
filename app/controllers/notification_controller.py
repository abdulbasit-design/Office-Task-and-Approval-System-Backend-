from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.services.notification_service import (
    get_user_notifications,
    get_notification,
    mark_notification_as_read
)


def get_notifications_controller(
    current_user: User,
    db: Session
):
    return get_user_notifications(
        db,
        current_user.id
    )


def get_notification_controller(
    notification_id: int,
    current_user: User,
    db: Session
):
    notification = get_notification(
        db,
        notification_id,
        current_user.id
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


def mark_notification_as_read_controller(
    notification_id: int,
    current_user: User,
    db: Session
):
    notification = get_notification(
        db,
        notification_id,
        current_user.id
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return mark_notification_as_read(
        db,
        notification
    )
