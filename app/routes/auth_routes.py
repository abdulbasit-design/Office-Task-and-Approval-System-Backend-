from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Cookie
)
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dependencies.auth import (
    get_current_user,
    require_role
)
from app.models.user_model import User
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    ForgotPasswordRequest,
    MessageResponse,
    PasswordResetRequestItem,
    AdminResetPasswordRequest
)
from app.controllers.auth_controller import (
    signup_controller,
    login_controller,
    refresh_token_controller,
    logout_controller,
    get_my_profile_controller,
    employee_test_controller,
    manager_test_controller,
    admin_test_controller,
    forgot_password_controller,
    get_password_reset_requests_controller,
    admin_reset_password_controller
)



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return signup_controller(
        user_data,
        db
    )


@router.post("/login")
def login(
    user_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    return login_controller(
        user_data,
        response,
        db
    )


@router.post("/refresh")
def refresh_token(
    refresh_token: str = Cookie(...)
):
    return refresh_token_controller(
        refresh_token
    )


@router.post("/logout")
def logout(
    response: Response
):
    return logout_controller(
        response
    )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):
    return get_my_profile_controller(
        current_user
    )


@router.get("/employee-test")
def employee_test(
    current_user: User = Depends(
        require_role("employee")
    )
):
    return employee_test_controller(
        current_user
    )


@router.get("/manager-test")
def manager_test(
    current_user: User = Depends(
        require_role("manager")
    )
):
    return manager_test_controller(
        current_user
    )


@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(
        require_role("admin")
    )
):
    return admin_test_controller(
        current_user
    )


@router.post(
    "/forgot-password",
    response_model=MessageResponse
)
def forgot_password(
    request_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    return forgot_password_controller(
        request_data,
        db
    )


@router.get(
    "/password-reset-requests",
    response_model=list[PasswordResetRequestItem]
)
def get_password_reset_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    return get_password_reset_requests_controller(
        db
    )


@router.post(
    "/password-reset-requests/{request_id}/reset",
    response_model=MessageResponse
)
def admin_reset_password(
    request_id: int,
    reset_data: AdminResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    return admin_reset_password_controller(
        request_id,
        reset_data,
        db
    )

