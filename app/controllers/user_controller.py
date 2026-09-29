from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserAdminUpdate
from app.services.user_service import (
    get_users,
    get_user,
    update_user,
    delete_user
)


def get_users_controller(
    db: Session
):
    return get_users(db)


def get_user_controller(
    user_id: int,
    db: Session
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def update_user_controller(
    user_id: int,
    user_data: UserAdminUpdate,
    db: Session
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    updated_user = update_user(
        db,
        user,
        user_data
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    if updated_user == "manager_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found"
        )

    if updated_user == "manager_self":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User cannot be their own manager"
        )

    if updated_user == "manager_invalid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assigned manager must have the manager role"
        )

    if updated_user == "department_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    return updated_user


def delete_user_controller(
    user_id: int,
    current_user: User,
    db: Session
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account"
        )

    deleted = delete_user(
        db,
        user
    )

    if deleted == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User cannot be deleted because they are referenced by existing records"
        )

    return {
        "message": "User deleted successfully"
    }
