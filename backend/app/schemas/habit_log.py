from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HabitLogCreate(BaseModel):
    log_date: date
    status: Literal["completed", "skipped", "missed"] = "completed"
    notes: str | None = Field(default=None, max_length=500)


class HabitLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    user_id: int
    log_date: date
    status: str
    notes: str | None = None
    created_at: datetime | None = None