
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate


def create_reminder(
    db: Session,
    user_id: int,
    reminder_data: ReminderCreate,
) -> Reminder:
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == reminder_data.habit_id,
            Habit.user_id == user_id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    reminder = Reminder(
        user_id=user_id,
        habit_id=reminder_data.habit_id,
        reminder_time=reminder_data.reminder_time,
        frequency=reminder_data.frequency,
        is_enabled=reminder_data.is_enabled,
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def get_user_reminders(db: Session, user_id: int) -> list[Reminder]:
    return (
        db.query(Reminder)
        .filter(Reminder.user_id == user_id)
        .order_by(Reminder.reminder_time.asc())
        .all()
    )


def update_reminder(
    db: Session,
    user_id: int,
    reminder_id: int,
    reminder_data: ReminderUpdate,
) -> Reminder:
    reminder = (
        db.query(Reminder)
        .filter(
            Reminder.id == reminder_id,
            Reminder.user_id == user_id,
        )
        .first()
    )

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    for field, value in reminder_data.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)

    db.commit()
    db.refresh(reminder)
    return reminder


def delete_reminder(
    db: Session,
    user_id: int,
    reminder_id: int,
) -> dict:
    reminder = (
        db.query(Reminder)
        .filter(
            Reminder.id == reminder_id,
            Reminder.user_id == user_id,
        )
        .first()
    )

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    db.delete(reminder)
    db.commit()

    return {
        "success": True,
        "message": "Reminder deleted successfully",
    }
