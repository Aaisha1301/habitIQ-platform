from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.habit_log import HabitLogCreate, HabitLogResponse, HabitLogUpdate
from app.services.habit_log_service import create_habit_log,get_user_habit_logs,update_habit_log,delete_habit_log
from app.models.category import Category


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

@router.put("/logs/{log_id}", response_model=HabitLogResponse)
def edit_habit_log(
    log_id: int,
    log_data: HabitLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_habit_log(
        log_id=log_id,
        user_id=current_user.id,
        log_data=log_data,
        db=db,
    )

@router.delete("/logs/{log_id}")
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_habit_log(
        log_id=log_id,
        user_id=current_user.id,
        db=db,
    )