from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True,
        index=True,
    )

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    frequency = Column(
        String(20),
        nullable=False,
        default="daily",
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="habits",
    )

    habit_logs = relationship(
        "HabitLog",
        back_populates="habit",
    )

    goals = relationship(
        "Goal",
        back_populates="habit",
    )

    reminders = relationship(
        "Reminder",
        back_populates="habit",
    )

    analytics = relationship(
        "Analytics",
        back_populates="habit",
    )

    ai_predictions = relationship(
        "AIPrediction",
        back_populates="habit",
    )

    category = relationship(
        "Category",
        back_populates="habits",
    )