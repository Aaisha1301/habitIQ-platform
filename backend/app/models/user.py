from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False, default="user")
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    habits = relationship("Habit", back_populates="user")
    habit_logs = relationship("HabitLog", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    analytics = relationship("Analytics", back_populates="user")
    ai_predictions = relationship("AIPrediction", back_populates="user")