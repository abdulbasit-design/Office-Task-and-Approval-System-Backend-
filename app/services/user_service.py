from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.task_model import Task
from app.models.notification_model import Notification
from app.models.department_model import Department
from app.schemas.user_schema import UserAdminUpdate
from app.utils.password import hash_password


def get_users(
    db: Session
):
    return db.query(User).all()


def get_user(
    db: Session,
    user_id: int
):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def update_user(
    db: Session,
    user: User,
    user_data: UserAdminUpdate
):
    existing_email = db.query(User).filter(
        User.email == user_data.email,
        User.id != user.id
    ).first()

    if existing_email:
        return None

    if user_data.manager_id is not None:
        manager = db.query(User).filter(
            User.id == user_data.manager_id
        ).first()

        if manager is None:
            return "manager_not_found"

        if manager.id == user.id:
            return "manager_self"

        if manager.role != "manager":
            return "manager_invalid"

    if user_data.department_id is not None:
        department = db.query(
            Department
        ).filter(
            Department.id == user_data.department_id
        ).first()

        if department is None:
            return "department_not_found"

    user.full_name = user_data.full_name
    user.email = user_data.email
    user.role = user_data.role
    user.department_id = user_data.department_id
    user.manager_id = user_data.manager_id
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


def update_user_password(
    db: Session,
    user: User,
    password: str
):
    hashed_password = hash_password(password)

    user.password_hash = hashed_password

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User
):
    task_reference = db.query(Task).filter(
        (Task.created_by == user.id) |
        (Task.assigned_to == user.id) |
        (Task.approved_by == user.id)
    ).first()

    if task_reference:
        return False

    notification_reference = db.query(
        Notification
    ).filter(
        Notification.user_id == user.id
    ).first()

    if notification_reference:
        return False

    manager_reference = db.query(User).filter(
        User.manager_id == user.id
    ).first()

    if manager_reference:
        return False

    db.delete(user)
    db.commit()

    return True
