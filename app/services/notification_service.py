from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.notification_model import Notification


def create_notification(
    db: Session,
    user_id: int,
    task_id: int | None,
    notification_type: str,
    title: str,
    message: str
):
    new_notification = Notification(
        user_id=user_id,
        task_id=task_id,
        type=notification_type,
        title=title,
        message=message,
        is_read=False
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification


def get_user_notifications(
    db: Session,
    user_id: int
):
    notifications = db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return notifications


def get_notification(
    db: Session,
    notification_id: int,
    user_id: int
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()

    return notification


def mark_notification_as_read(
    db: Session,
    notification: Notification
):
    notification.is_read = True
    notification.read_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(notification)

    return notification
