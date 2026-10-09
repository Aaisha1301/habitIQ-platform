
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AIPredictionResponse(BaseModel):
    id: int
    user_id: int
    habit_id: Optional[int] = None
    prediction_date: date
    predicted_completion_rate: Optional[float] = None
    confidence_score: Optional[float] = None
    prediction_type: str
    prediction_result: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)