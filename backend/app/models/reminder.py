from sqlalchemy import Column, Boolean, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

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
        nullable=False,
        index=True,
    )

    reminder_time = Column(Time, nullable=False)
    frequency = Column(String(20), nullable=False, default="daily")
    is_enabled = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="reminders")
    habit = relationship("Habit", back_populates="reminders")