from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.habit_log import HabitLogCreate, HabitLogResponse
from app.services.habit_log_service import create_habit_log,get_user_habit_logs


router = APIRouter(
    prefix="/api/habits",
    tags=["Habit Logs"],
)


@router.post(
    "/{habit_id}/logs",
    response_model=HabitLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_habit_log(
    habit_id: int,
    log_data: HabitLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_habit_log(
        habit_id=habit_id,
        user_id=current_user.id,
        log_data=log_data,
        db=db,
    )

@router.get("/logs", response_model=list[HabitLogResponse])
def read_habit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_habit_logs(
        user_id=current_user.id,
        db=db,
    )