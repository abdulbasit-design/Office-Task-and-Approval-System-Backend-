from fastapi import (
    APIRouter,
    Depends,
    status
)
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dependencies.auth import (
    get_current_user,
    require_role
)
from app.models.user_model import User
from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskSubmit,
    TaskReject,
    TaskResponse
)
from app.controllers.task_controller import (
    create_task_controller,
    get_tasks_controller,
    get_task_controller,
    update_task_controller,
    submit_task_controller,
    approve_task_controller,
    reject_task_controller
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    return create_task_controller(
        task_data,
        current_user,
        db
    )


@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_tasks_controller(
        current_user,
        db
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_one(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_task_controller(
        task_id,
        current_user,
        db
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    return update_task_controller(
        task_id,
        task_data,
        current_user,
        db
    )


@router.post(
    "/{task_id}/submit",
    response_model=TaskResponse
)
def submit(
    task_id: int,
    task_data: TaskSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("employee")
    )
):
    return submit_task_controller(
        task_id,
        task_data,
        current_user,
        db
    )


@router.post(
    "/{task_id}/approve",
    response_model=TaskResponse
)
def approve(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    return approve_task_controller(
        task_id,
        current_user,
        db
    )


@router.post(
    "/{task_id}/reject",
    response_model=TaskResponse
)
def reject(
    task_id: int,
    task_data: TaskReject,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    return reject_task_controller(
        task_id,
        task_data,
        current_user,
        db
    )
