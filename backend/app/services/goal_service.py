from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.models.habit import Habit
from app.schemas.goal import GoalCreate, GoalUpdate


def create_goal(
    goal_data: GoalCreate,
    user_id: int,
    db: Session,
) -> Goal:

    # Validate the habit if one was provided
    if goal_data.habit_id is not None:
        habit = (
            db.query(Habit)
            .filter(
                Habit.id == goal_data.habit_id,
                Habit.user_id == user_id,
            )
            .first()
        )

        if habit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habit not found",
            )

    new_goal = Goal(
        user_id=user_id,
        habit_id=goal_data.habit_id,
        title=goal_data.title,
        description=goal_data.description,
        target_value=goal_data.target_value,
        current_value=goal_data.current_value,
        start_date=goal_data.start_date,
        end_date=goal_data.end_date,
        status="active",
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


def get_user_goals(
    user_id: int,
    db: Session,
) -> list[Goal]:

    return (
        db.query(Goal)
        .filter(Goal.user_id == user_id)
        .order_by(Goal.created_at.desc())
        .all()
    )


def update_goal(
    goal_id: int,
    user_id: int,
    goal_data: GoalUpdate,
    db: Session,
) -> Goal:

    goal = (
        db.query(Goal)
        .filter(
            Goal.id == goal_id,
            Goal.user_id == user_id,
        )
        .first()
    )

    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    # Validate habit if a new habit_id was provided
    if (
        "habit_id" in goal_data.model_fields_set
        and goal_data.habit_id is not None
    ):
        habit = (
            db.query(Habit)
            .filter(
                Habit.id == goal_data.habit_id,
                Habit.user_id == user_id,
            )
            .first()
        )

        if habit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habit not found",
            )

    update_data = goal_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(goal, key, value)

    db.commit()
    db.refresh(goal)

    return goal


def delete_goal(
    goal_id: int,
    user_id: int,
    db: Session,
) -> dict:

    goal = (
        db.query(Goal)
        .filter(
            Goal.id == goal_id,
            Goal.user_id == user_id,
        )
        .first()
    )

    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    db.delete(goal)
    db.commit()

    return {
        "success": True,
        "message": "Goal deleted successfully",
    }