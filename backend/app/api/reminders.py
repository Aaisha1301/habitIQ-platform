
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.reminder import (
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse,
)
from app.services.reminder_service import (
    create_reminder,
    get_user_reminders,
    update_reminder,
    delete_reminder,
)

router = APIRouter(prefix="/api/reminders", tags=["Reminders"])


@router.post("/", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder_endpoint(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_reminder(db, current_user.id, reminder_data)


@router.get("/", response_model=list[ReminderResponse])
def get_reminders_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_reminders(db, current_user.id)


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder_endpoint(
    reminder_id: int,
    reminder_data: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_reminder(
        db, current_user.id, reminder_id, reminder_data
    )


@router.delete("/{reminder_id}")
def delete_reminder_endpoint(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_reminder(db, current_user.id, reminder_id)
