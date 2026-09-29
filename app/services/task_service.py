from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskSubmit,
    TaskReject
)
from app.services.notification_service import create_notification


def create_task(
    db: Session,
    task_data: TaskCreate,
    current_user: User
):
    assigned_user = db.query(User).filter(
        User.id == task_data.assigned_to
    ).first()

    if assigned_user is None:
        return "user_not_found"

    if assigned_user.is_active == False:
        return "user_inactive"

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        created_by=current_user.id,
        assigned_to=task_data.assigned_to,
        deadline=task_data.deadline,
        priority=task_data.priority,
        status="PENDING",
        activity_log=[
            {
                "action": "created",
                "user_id": current_user.id
            }
        ]
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    create_notification(
        db,
        user_id=new_task.assigned_to,
        task_id=new_task.id,
        notification_type="TASK_ASSIGNED",
        title="New Task Assigned",
        message=f"You have been assigned the task '{new_task.title}'."
    )

    return new_task


def get_tasks(
    db: Session,
    current_user: User
):
    if current_user.role == "admin":
        tasks = db.query(Task).all()

    elif current_user.role == "manager":
        tasks = db.query(Task).filter(
            Task.created_by == current_user.id
        ).all()

    else:
        tasks = db.query(Task).filter(
            Task.assigned_to == current_user.id
        ).all()

    return tasks


def get_task(
    db: Session,
    task_id: int,
    current_user: User
):
    if current_user.role == "admin":
        task = db.query(Task).filter(
            Task.id == task_id
        ).first()

    elif current_user.role == "manager":
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.created_by == current_user.id
        ).first()

    else:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.assigned_to == current_user.id
        ).first()

    return task


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
    current_user: User
):
    assigned_user = db.query(User).filter(
        User.id == task_data.assigned_to
    ).first()

    if assigned_user is None:
        return "user_not_found"

    if assigned_user.is_active == False:
        return "user_inactive"

    task.title = task_data.title
    task.description = task_data.description
    task.assigned_to = task_data.assigned_to
    task.deadline = task_data.deadline
    task.priority = task_data.priority

    task.activity_log.append(
        {
            "action": "updated",
            "user_id": current_user.id
        }
    )

    db.commit()
    db.refresh(task)

    return task


def submit_task(
    db: Session,
    task: Task,
    task_data: TaskSubmit,
    current_user: User
):
    if task.status not in [
        "PENDING",
        "REJECTED"
    ]:
        return None

    was_rejected = task.status == "REJECTED"

    task.status = "SUBMITTED"
    task.submitted_at = datetime.now(timezone.utc)
    task.submission_note = task_data.submission_note
    task.rejection_reason = None

    task.activity_log.append(
        {
            "action": "submitted",
            "user_id": current_user.id
        }
    )

    db.commit()
    db.refresh(task)

    if was_rejected:
        notification_type = "TASK_RESUBMITTED"
        notification_title = "Task Resubmitted"
        notification_message = (
            f"The task '{task.title}' has been resubmitted."
        )

    else:
        notification_type = "TASK_SUBMITTED"
        notification_title = "Task Submitted"
        notification_message = (
            f"The task '{task.title}' has been submitted for review."
        )

    create_notification(
        db,
        user_id=task.created_by,
        task_id=task.id,
        notification_type=notification_type,
        title=notification_title,
        message=notification_message
    )

    return task


def approve_task(
    db: Session,
    task: Task,
    current_user: User
):
    if task.status != "SUBMITTED":
        return None

    task.status = "APPROVED"
    task.approved_at = datetime.now(timezone.utc)
    task.approved_by = current_user.id
    task.rejection_reason = None

    task.activity_log.append(
        {
            "action": "approved",
            "user_id": current_user.id
        }
    )

    db.commit()
    db.refresh(task)

    create_notification(
        db,
        user_id=task.assigned_to,
        task_id=task.id,
        notification_type="TASK_APPROVED",
        title="Task Approved",
        message=f"Your task '{task.title}' has been approved."
    )

    return task


def reject_task(
    db: Session,
    task: Task,
    task_data: TaskReject,
    current_user: User
):
    if task.status != "SUBMITTED":
        return None

    task.status = "REJECTED"
    task.rejection_reason = task_data.rejection_reason
    task.approved_at = None
    task.approved_by = None

    task.activity_log.append(
        {
            "action": "rejected",
            "user_id": current_user.id
        }
    )

    db.commit()
    db.refresh(task)

    create_notification(
        db,
        user_id=task.assigned_to,
        task_id=task.id,
        notification_type="TASK_REJECTED",
        title="Task Rejected",
        message=(
            f"Your task '{task.title}' was rejected. "
            f"Reason: {task.rejection_reason}"
        )
    )

    return task
