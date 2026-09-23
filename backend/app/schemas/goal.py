from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GoalCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

    target_value: int = Field(..., gt=0)
    current_value: int = Field(default=0, ge=0)

    start_date: date
    end_date: date | None = None

    habit_id: int | None = None

    @model_validator(mode="after")
    def validate_goal_dates(self):
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")

        if self.current_value > self.target_value:
            raise ValueError("current_value cannot exceed target_value")

        return self


class GoalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None

    target_value: int | None = Field(default=None, gt=0)
    current_value: int | None = Field(default=None, ge=0)

    start_date: date | None = None
    end_date: date | None = None

    habit_id: int | None = None
    status: str | None = Field(default=None, max_length=20)

    @model_validator(mode="after")
    def validate_goal_values(self):
        if (
            self.target_value is not None
            and self.current_value is not None
            and self.current_value > self.target_value
        ):
            raise ValueError("current_value cannot exceed target_value")

        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError("end_date cannot be earlier than start_date")

        return self


class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    habit_id: int | None = None

    title: str
    description: str | None = None

    target_value: int
    current_value: int

    start_date: date
    end_date: date | None = None

    status: str
    created_at: datetime | None = None