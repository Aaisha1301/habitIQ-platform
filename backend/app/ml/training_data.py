
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_log import HabitLog


def build_training_dataset(db: Session, user_id: int):
    """
    Build one training example per habit-log record.

    Features:
    1. Previous completion rate for that habit
    2. Previous consecutive-day streak
    3. Number of previous logs in the last 30 days

    Label:
    1 = completed
    0 = skipped

    Only records belonging to the specified user are considered.
    """

    today = date.today()
    start_date = today - timedelta(days=365)

    habits = (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .all()
    )

    features = []
    labels = []

    for habit in habits:
        logs = (
            db.query(HabitLog)
            .filter(
                HabitLog.habit_id == habit.id,
                HabitLog.user_id == user_id,
                HabitLog.log_date >= start_date,
                HabitLog.log_date <= today,
                HabitLog.status.in_(["completed", "skipped"]),
            )
            .order_by(HabitLog.log_date.asc(), HabitLog.id.asc())
            .all()
        )

        previous_logs = []

        for log in logs:
            # Use only records before the target log to avoid leakage.
            if previous_logs:
                previous_30 = [
                    item for item in previous_logs
                    if item.log_date >= log.log_date - timedelta(days=29)
                ]

                if previous_30:
                    completion_rate = (
                        sum(item.status == "completed" for item in previous_30)
                        / len(previous_30)
                    ) * 100
                else:
                    completion_rate = 0.0

                completed_dates = {
                    item.log_date
                    for item in previous_logs
                    if item.status == "completed"
                }

                streak = 0
                check_date = log.log_date - timedelta(days=1)

                while check_date in completed_dates:
                    streak += 1
                    check_date -= timedelta(days=1)

                features.append([
                    completion_rate,
                    streak,
                    len(previous_30),
                ])
                labels.append(
                    1 if log.status == "completed" else 0
                )

            previous_logs.append(log)

    return features, labels
