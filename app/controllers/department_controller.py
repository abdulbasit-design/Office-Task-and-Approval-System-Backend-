from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.department_schema import DepartmentCreate
from app.services.department_service import (
    create_department,
    get_departments,
    get_department,
    update_department,
    delete_department
)


def create_department_controller(
    department_data: DepartmentCreate,
    db: Session
):
    department = create_department(
        db,
        department_data
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department already exists"
        )

    return department


def get_departments_controller(
    db: Session
):
    return get_departments(db)


def get_department_controller(
    department_id: int,
    db: Session
):
    department = get_department(
        db,
        department_id
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    return department


def update_department_controller(
    department_id: int,
    department_data: DepartmentCreate,
    db: Session
):
    department = get_department(
        db,
        department_id
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    updated_department = update_department(
        db,
        department,
        department_data
    )

    if updated_department is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department name already exists"
        )

    return updated_department


def delete_department_controller(
    department_id: int,
    db: Session
):
    department = get_department(
        db,
        department_id
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    deleted = delete_department(
        db,
        department
    )

    if deleted == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department cannot be deleted because users are assigned to it"
        )

    return {
        "message": "Department deleted successfully"
    }
