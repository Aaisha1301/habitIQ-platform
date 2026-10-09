from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    habit_id: int | None = None
    analysis_date: date
    completion_rate: float
    current_streak: int
    longest_streak: int
    total_completions: int
    created_at: datetime | None = None