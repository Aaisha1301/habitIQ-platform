from app.core.database import Base, engine
from app.models import User, Habit, Category, HabitLog, Goal, Reminder, Analytics
from sqlalchemy.orm import configure_mappers

configure_mappers()
print("SQLAlchemy relationships configured successfully!")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")