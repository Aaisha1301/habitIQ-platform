from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Float, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    habit_id = Column(
        Integer,
        ForeignKey("habits.id"),
        nullable=True,
        index=True,
    )

    prediction_date = Column(Date, nullable=False)

    predicted_completion_rate = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)

    prediction_type = Column(String(50), nullable=False)
    prediction_result = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="ai_predictions")
    habit = relationship("Habit", back_populates="ai_predictions")