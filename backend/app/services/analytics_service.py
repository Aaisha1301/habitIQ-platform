from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.analytics import Analytics
from app.models.habit import Habit
from app.models.habit_log import HabitLog


def calculate_habit_analytics(
    db: Session,
    user_id: int,
    habit_id: int,
) -> Analytics:
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == user_id,
        )
        .first()
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    logs = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == user_id,
        )
        .order_by(HabitLog.log_date.asc())
        .all()
    )

    total_logs = len(logs)
    total_completions = sum(
        1 for log in logs if log.status == "completed"
    )

    completion_rate = (
        (total_completions / total_logs) * 100
        if total_logs > 0
        else 0.0
    )

    completed_dates = {
        log.log_date
        for log in logs
        if log.status == "completed"
    }

    longest_streak = 0
    current_streak = 0

    if completed_dates:
        sorted_dates = sorted(completed_dates)

        streak = 1
        longest_streak = 1

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] == sorted_dates[i - 1] + timedelta(days=1):
                streak += 1
            else:
                streak = 1

            longest_streak = max(longest_streak, streak)

        today = date.today()

        if today in completed_dates:
            current_date = today

            while current_date in completed_dates:
                current_streak += 1
                current_date -= timedelta(days=1)
        else:
            current_streak = 0

    existing = (
        db.query(Analytics)
        .filter(
            Analytics.user_id == user_id,
            Analytics.habit_id == habit_id,
            Analytics.analysis_date == date.today(),
        )
        .first()
    )

    if existing:
        existing.completion_rate = completion_rate
        existing.current_streak = current_streak
        existing.longest_streak = longest_streak
        existing.total_completions = total_completions

        db.commit()
        db.refresh(existing)

        return existing

    analytics = Analytics(
        user_id=user_id,
        habit_id=habit_id,
        analysis_date=date.today(),
        completion_rate=completion_rate,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_completions=total_completions,
    )

    db.add(analytics)
    db.commit()
    db.refresh(analytics)

    return analytics
