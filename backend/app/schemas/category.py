from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    created_at: datetime | None = None