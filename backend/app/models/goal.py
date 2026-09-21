from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Goal(Base):
    __tablename__ = "goals"

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

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    target_value = Column(Integer, nullable=False)
    current_value = Column(Integer, nullable=False, default=0)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    status = Column(String(20), nullable=False, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="goals")
    habit = relationship("Habit", back_populates="goals")