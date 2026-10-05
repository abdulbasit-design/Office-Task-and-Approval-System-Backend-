from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.password import hash_password, verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token
)
from app.services.notification_service import create_notification



def signup_user(
    db: Session,
    user_data: UserCreate
):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        return None

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hashed_password,
        role="employee"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(
    db: Session,
    user_data: UserLogin
):
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user:
        return None

    password_correct = verify_password(
        user_data.password,
        user.password_hash
    )

    if password_correct == False:
        return None

    if user.is_active == False:
        return None

    access_token = create_access_token(
        user.id
    )

    refresh_token = create_refresh_token(
        user.id
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def forgot_password_service(
    db: Session,
    email: str
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if user:
        user.password_reset_status = "pending"
        user.password_reset_requested_at = datetime.now(timezone.utc)

        admin_user = db.query(User).filter(
            User.email == "admin@test.com"
        ).first()

        if not admin_user:
            admin_user = db.query(User).filter(
                User.role == "admin"
            ).first()

        if admin_user:
            create_notification(
                db=db,
                user_id=admin_user.id,
                task_id=None,
                notification_type="PASSWORD_RESET_REQUEST",
                title="Password Reset Request",
                message=f"{user.full_name} has requested a password reset."
            )
        else:
            db.commit()

    return {
        "message": "If the account exists, a password reset request has been submitted to the administrator."
    }


def get_pending_password_reset_requests_service(
    db: Session
):
    users = db.query(User).filter(
        User.password_reset_status == "pending"
    ).order_by(
        User.password_reset_requested_at.desc()
    ).all()

    return [
        {
            "id": u.id,
            "user_id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role,
            "status": u.password_reset_status,
            "requested_at": u.password_reset_requested_at
        }
        for u in users
    ]


def admin_reset_user_password_service(
    db: Session,
    request_id: int,
    new_password: str
):
    user = db.query(User).filter(
        User.id == request_id
    ).first()

    if not user:
        return "not_found"

    if user.password_reset_status != "pending":
        return "not_pending"

    hashed_password = hash_password(new_password)
    user.password_hash = hashed_password
    user.password_reset_status = "completed"
    db.commit()

    return {
        "message": f"Password for user {user.full_name} has been successfully reset."
    }

