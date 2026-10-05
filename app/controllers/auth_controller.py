from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
import jwt

from app.models.user_model import User
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    ForgotPasswordRequest,
    AdminResetPasswordRequest
)
from app.services.auth_service import (
    signup_user,
    login_user,
    forgot_password_service,
    get_pending_password_reset_requests_service,
    admin_reset_user_password_service
)
from app.utils.jwt import decode_access_token, create_access_token



def signup_controller(
    user_data: UserCreate,
    db: Session
):
    new_user = signup_user(
        db,
        user_data
    )

    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    return new_user


def login_controller(
    user_data: UserLogin,
    response: Response,
    db: Session
):
    result = login_user(
        db,
        user_data
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax"
    )

    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"]
    }


def refresh_token_controller(
    refresh_token: str
):
    try:
        payload = decode_access_token(
            refresh_token
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    try:
        user_id = int(user_id)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    access_token = create_access_token(
        user_id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def logout_controller(
    response: Response
):
    response.delete_cookie(
        key="refresh_token"
    )

    return {
        "message": "Logged out successfully"
    }


def get_my_profile_controller(
    current_user: User
):
    return current_user


def employee_test_controller(
    current_user: User
):
    return {
        "message": "Employee access granted",
        "user": current_user.full_name,
        "role": current_user.role
    }


def manager_test_controller(
    current_user: User
):
    return {
        "message": "Manager access granted",
        "user": current_user.full_name,
        "role": current_user.role
    }


def admin_test_controller(
    current_user: User
):
    return {
        "message": "Admin access granted",
        "user": current_user.full_name,
        "role": current_user.role
    }


def forgot_password_controller(
    request_data: ForgotPasswordRequest,
    db: Session
):
    return forgot_password_service(
        db,
        request_data.email
    )


def get_password_reset_requests_controller(
    db: Session
):
    return get_pending_password_reset_requests_service(
        db
    )


def admin_reset_password_controller(
    request_id: int,
    reset_data: AdminResetPasswordRequest,
    db: Session
):
    result = admin_reset_user_password_service(
        db,
        request_id,
        reset_data.new_password
    )

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password reset request not found"
        )

    if result == "not_pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset request is not pending or has already been completed"
        )

    return result

