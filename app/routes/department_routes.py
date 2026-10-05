from fastapi import (
    APIRouter,
    Depends,
    status
)
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user_model import User
from app.schemas.department_schema import (
    DepartmentCreate,
    DepartmentResponse
)
from app.controllers.department_controller import (
    create_department_controller,
    get_departments_controller,
    get_department_controller,
    update_department_controller,
    delete_department_controller
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    return create_department_controller(
        department_data,
        db
    )


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_departments_controller(db)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_one(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_department_controller(
        department_id,
        db
    )


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update(
    department_id: int,
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    return update_department_controller(
        department_id,
        department_data,
        db
    )


@router.delete(
    "/{department_id}"
)
def delete(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    return delete_department_controller(
        department_id,
        db
    )
