from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.habits import router as habits_router
from app.api.habit_logs import router as habit_logs_router
from app.api.categories import router as categories_router


app = FastAPI(
    title="HabitIQ API",
    description="Personal Habit Analytics & Prediction Platform",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "success": True,
        "data": {
            "project": "HabitIQ",
            "status": "running",
        },
        "message": "HabitIQ API is running",
    }


@app.get("/api/health")
def health_check():
    return {
        "success": True,
        "data": {
            "status": "OK",
        },
        "message": "Service is healthy",
    }


# Register API routers
app.include_router(users_router)
app.include_router(habits_router)
app.include_router(habit_logs_router)
app.include_router(categories_router)