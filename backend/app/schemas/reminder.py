
from datetime import datetime, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReminderCreate(BaseModel):
    habit_id: int = Field(gt=0)
    reminder_time: time
    frequency: Literal["daily", "weekly"] = "daily"
    is_enabled: bool = True


class ReminderUpdate(BaseModel):
    reminder_time: time | None = None
    frequency: Literal["daily", "weekly"] | None = None
    is_enabled: bool | None = None


class ReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    habit_id: int
    reminder_time: time
    frequency: str
    is_enabled: bool
    created_at: datetime | None = None
