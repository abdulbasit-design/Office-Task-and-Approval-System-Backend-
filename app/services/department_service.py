from sqlalchemy.orm import Session

from app.models.department_model import Department
from app.models.user_model import User
from app.schemas.department_schema import DepartmentCreate


def create_department(
    db: Session,
    department_data: DepartmentCreate
):
    existing_department = db.query(
        Department
    ).filter(
        Department.name == department_data.name
    ).first()

    if existing_department:
        return None

    new_department = Department(
        name=department_data.name,
        description=department_data.description
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


def get_departments(
    db: Session
):
    return db.query(
        Department
    ).all()


def get_department(
    db: Session,
    department_id: int
):
    return db.query(
        Department
    ).filter(
        Department.id == department_id
    ).first()


def update_department(
    db: Session,
    department: Department,
    department_data: DepartmentCreate
):
    existing_department = db.query(
        Department
    ).filter(
        Department.name == department_data.name,
        Department.id != department.id
    ).first()

    if existing_department:
        return None

    department.name = department_data.name
    department.description = department_data.description

    db.commit()
    db.refresh(department)

    return department


def delete_department(
    db: Session,
    department: Department
):
    users_in_department = db.query(
        User
    ).filter(
        User.department_id == department.id
    ).count()

    if users_in_department > 0:
        return False

    db.delete(department)
    db.commit()

    return True
