
from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ai_prediction import AIPrediction
from app.models.habit import Habit
from app.models.habit_log import HabitLog


def generate_habit_prediction(
    db: Session,
    user_id: int,
    habit_id: int,
) -> AIPrediction:
    # Verify that the habit belongs to the current user.
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

    # Use the most recent 30 days of habit logs.
    today = date.today()
    start_date = today - timedelta(days=29)

    logs = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == user_id,
            HabitLog.log_date >= start_date,
            HabitLog.log_date <= today,
        )
        .all()
    )

    total_logs = len(logs)
    completed_logs = sum(
        1 for log in logs if log.status == "completed"
    )

    if total_logs == 0:
        predicted_rate = None
        confidence = 0.0
        result = (
            "Not enough habit history to make a prediction. "
            "Record habit logs to build a useful estimate."
        )
    else:
        predicted_rate = round(
            (completed_logs / total_logs) * 100, 2
        )
        confidence = round(min(total_logs / 30, 1.0), 2)

        if predicted_rate >= 80:
            result = (
                "Strong recent consistency. Keep following "
                "your current routine."
            )
        elif predicted_rate >= 50:
            result = (
                "Moderate recent consistency. A regular "
                "schedule may help improve completion."
            )
        else:
            result = (
                "Low recent consistency. Try setting a smaller "
                "daily target and a reminder."
            )

    prediction = AIPrediction(
        user_id=user_id,
        habit_id=habit_id,
        prediction_date=today,
        predicted_completion_rate=predicted_rate,
        confidence_score=confidence,
        prediction_type="rule_based_30_day",
        prediction_result=result,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction