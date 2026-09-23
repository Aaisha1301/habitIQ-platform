from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogCreate


def create_habit_log(
    habit_id: int,
    user_id: int,
    log_data: HabitLogCreate,
    db: Session,
) -> HabitLog:

    # Check whether the habit exists and belongs to this user
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == user_id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    # Prevent duplicate logs for the same habit and date
    existing_log = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == user_id,
            HabitLog.log_date == log_data.log_date,
        )
        .first()
    )

    if existing_log:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A log already exists for this habit on this date",
        )

    # Create the habit log
    new_log = HabitLog(
        habit_id=habit_id,
        user_id=user_id,
        log_date=log_data.log_date,
        status=log_data.status,
        notes=log_data.notes,
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log

def get_user_habit_logs(user_id: int, db: Session):
    return (
        db.query(HabitLog)
        .filter(HabitLog.user_id == user_id)
        .order_by(HabitLog.log_date.desc())
        .all()
    )

def update_habit_log(log_id: int, user_id: int, log_data, db: Session):
    log = (
        db.query(HabitLog)
        .filter(
            HabitLog.id == log_id,
            HabitLog.user_id == user_id,
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Habit log not found",
        )

    update_data = log_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(log, field, value)

    db.commit()
    db.refresh(log)

    return log

def delete_habit_log(log_id: int, user_id: int, db: Session):
    log = (
        db.query(HabitLog)
        .filter(
            HabitLog.id == log_id,
            HabitLog.user_id == user_id,
        )
        .first()
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Habit log not found",
        )

    db.delete(log)
    db.commit()

    return {
        "message": "Habit log deleted successfully"
    }