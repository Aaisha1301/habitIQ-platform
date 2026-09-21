from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate


def create_habit(
    habit_data: HabitCreate,
    user_id: int,
    db: Session,
) -> Habit:

    new_habit = Habit(
        user_id=user_id,
        category_id=habit_data.category_id,
        name=habit_data.name,
        description=habit_data.description,
        frequency=habit_data.frequency,
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit

def get_user_habits(
    user_id: int,
    db: Session,
) -> list[Habit]:

    habits = (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .order_by(Habit.created_at.desc())
        .all()
    )

    return habits
def update_habit(
    habit_id: int,
    user_id: int,
    habit_data: HabitUpdate,
    db: Session,
) -> Habit:

    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == user_id,
        )
        .first()
    )

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    update_data = habit_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(habit, key, value)

    db.commit()
    db.refresh(habit)

    return habit


def delete_habit(
    habit_id: int,
    user_id: int,
    db: Session,
) -> dict:

    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == user_id,
        )
        .first()
    )

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    db.delete(habit)
    db.commit()

    return {
        "success": True,
        "message": "Habit deleted successfully",
    }