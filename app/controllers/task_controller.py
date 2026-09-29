from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskSubmit,
    TaskReject
)
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    submit_task,
    approve_task,
    reject_task
)


def create_task_controller(
    task_data: TaskCreate,
    current_user: User,
    db: Session
):
    task = create_task(
        db,
        task_data,
        current_user
    )

    if task == "user_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )

    if task == "user_inactive":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign a task to an inactive user"
        )

    return task


def get_tasks_controller(
    current_user: User,
    db: Session
):
    return get_tasks(
        db,
        current_user
    )


def get_task_controller(
    task_id: int,
    current_user: User,
    db: Session
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


def update_task_controller(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User,
    db: Session
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    updated_task = update_task(
        db,
        task,
        task_data,
        current_user
    )

    if updated_task == "user_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )

    if updated_task == "user_inactive":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign a task to an inactive user"
        )

    return updated_task


def submit_task_controller(
    task_id: int,
    task_data: TaskSubmit,
    current_user: User,
    db: Session
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    submitted_task = submit_task(
        db,
        task,
        task_data,
        current_user
    )

    if submitted_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task cannot be submitted in its current status"
        )

    return submitted_task


def approve_task_controller(
    task_id: int,
    current_user: User,
    db: Session
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    approved_task = approve_task(
        db,
        task,
        current_user
    )

    if approved_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted tasks can be approved"
        )

    return approved_task


def reject_task_controller(
    task_id: int,
    task_data: TaskReject,
    current_user: User,
    db: Session
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    rejected_task = reject_task(
        db,
        task,
        task_data,
        current_user
    )

    if rejected_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted tasks can be rejected"
        )

    return rejected_task
