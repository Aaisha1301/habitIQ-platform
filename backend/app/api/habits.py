from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.habit import HabitCreate,HabitUpdate, HabitResponse
from app.services.habit_service import (
    create_habit,
    get_user_habits,
    update_habit,
    delete_habit,
)

router = APIRouter(
    prefix="/api/habits",
    tags=["Habits"],
)


@router.post(
    "/",
    response_model=HabitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_habit(
    habit_data: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_habit(
        habit_data=habit_data,
        user_id=current_user.id,
        db=db,
    )
@router.get(
    "/",
    response_model=list[HabitResponse],
    status_code=status.HTTP_200_OK,
)
def read_user_habits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_habits(
        user_id=current_user.id,
        db=db,
    )

@router.put(
    "/{habit_id}",
    response_model=HabitResponse,
    status_code=status.HTTP_200_OK,
)
def update_existing_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_habit(
        habit_id=habit_id,
        user_id=current_user.id,
        habit_data=habit_data,
        db=db,
    )

@router.delete(
    "/{habit_id}",
    status_code=status.HTTP_200_OK,
)
def delete_existing_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_habit(
        habit_id=habit_id,
        user_id=current_user.id,
        db=db,
    )