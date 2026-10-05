from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user_model import User
from app.schemas.user_schema import (
    UserAdminUpdate,
    UserResponse
)
from app.controllers.user_controller import (
    get_users_controller,
    get_user_controller,
    update_user_controller,
    delete_user_controller
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_users_controller(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_one(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_user_controller(
        user_id,
        db
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update(
    user_id: int,
    user_data: UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    return update_user_controller(
        user_id,
        user_data,
        db
    )


@router.delete(
    "/{user_id}"
)
def delete(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    return delete_user_controller(
        user_id,
        current_user,
        db
    )
