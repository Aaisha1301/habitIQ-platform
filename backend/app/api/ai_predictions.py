from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.ai_prediction import AIPrediction
from app.models.user import User
from app.schemas.ai_prediction import AIPredictionResponse
from app.services.ai_prediction_service import generate_habit_prediction


router = APIRouter(
    prefix="/api/ai-predictions",
    tags=["AI Predictions"],
)


@router.post(
    "/habits/{habit_id}",
    response_model=AIPredictionResponse,
)
def predict_habit_completion(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return generate_habit_prediction(
        db,
        current_user.id,
        habit_id,
    )


@router.get(
    "/",
    response_model=list[AIPredictionResponse],
)
def get_prediction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(AIPrediction)
        .filter(AIPrediction.user_id == current_user.id)
        .order_by(AIPrediction.created_at.desc())
        .all()
    )