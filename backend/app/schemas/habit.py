from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    frequency: str = Field(default="daily", max_length=20)
    category_id: int | None = None


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    frequency: str | None = Field(default=None, max_length=20)
    category_id: int | None = None
    is_active: bool | None = None


class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    category_id: int | None = None
    name: str
    description: str | None = None
    frequency: str
    is_active: bool
    created_at: datetime | None = None