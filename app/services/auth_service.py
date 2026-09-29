from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.password import hash_password, verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token
)


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
