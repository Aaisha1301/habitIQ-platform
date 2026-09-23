from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.services.goal_service import (
    create_goal,
    get_user_goals,
    update_goal,
    delete_goal,
)


router = APIRouter(
    prefix="/api/goals",
    tags=["Goals"],
)


@router.post(
    "/",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_goal(
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_goal(
        goal_data=goal_data,
        user_id=current_user.id,
        db=db,
    )


@router.get(
    "/",
    response_model=list[GoalResponse],
)
def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_goals(
        user_id=current_user.id,
        db=db,
    )


@router.put(
    "/{goal_id}",
    response_model=GoalResponse,
)
def update_existing_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_goal(
        goal_id=goal_id,
        user_id=current_user.id,
        goal_data=goal_data,
        db=db,
    )


@router.delete("/{goal_id}")
def delete_existing_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_goal(
        goal_id=goal_id,
        user_id=current_user.id,
        db=db,
    )