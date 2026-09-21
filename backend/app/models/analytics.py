from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Analytics(Base):
    __tablename__ = "analytics"

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

    analysis_date = Column(Date, nullable=False)

    completion_rate = Column(Float, nullable=False, default=0.0)
    current_streak = Column(Integer, nullable=False, default=0)
    longest_streak = Column(Integer, nullable=False, default=0)
    total_completions = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="analytics")
    habit = relationship("Habit", back_populates="analytics")