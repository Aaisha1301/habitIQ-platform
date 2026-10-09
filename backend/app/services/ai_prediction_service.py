
from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ai_prediction import AIPrediction
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.ml.habit_predictor import train_from_database


def generate_habit_prediction(
    db: Session,
    user_id: int,
    habit_id: int,
) -> AIPrediction:
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

    today = date.today()
    start_date = today - timedelta(days=29)

    logs = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == user_id,
            HabitLog.log_date >= start_date,
            HabitLog.log_date <= today,
            HabitLog.status.in_(["completed", "skipped"]),
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
        prediction_type = "insufficient_data"
        result = (
            "Not enough habit history to make a prediction. "
            "Record more habit logs to build a useful estimate."
        )
    else:
        # Keep the existing estimate as the safe default.
        predicted_rate = round(
            (completed_logs / total_logs) * 100, 2
        )
        confidence = round(min(total_logs / 30, 1.0), 2)
        prediction_type = "rule_based_30_day"

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

        # Use ML only if the user's historical dataset passes validation.
        try:
            model, message = train_from_database(db, user_id)

            if model is not None:
                recent_dates = {
                    log.log_date
                    for log in logs
                    if log.status == "completed"
                }

                streak = 0
                check_date = today

                while check_date in recent_dates:
                    streak += 1
                    check_date -= timedelta(days=1)

                features = [
                    predicted_rate,
                    streak,
                    total_logs,
                ]

                predicted_rate = model.predict_completion_probability(
                    features
                )
                prediction_type = "random_forest_historical"
                result = (
                    "ML estimate based on historical habit-log patterns. "
                    "This is an estimate, not a guarantee."
                )
            else:
                # Insufficient or unsuitable data: retain rule-based estimate.
                result = f"{result} ML model not used: {message}"
        except (ValueError, RuntimeError):
            # Keep the API usable if model training or prediction fails.
            result = (
                f"{result} ML model unavailable; using the rule-based estimate."
            )

    prediction = AIPrediction(
        user_id=user_id,
        habit_id=habit_id,
        prediction_date=today,
        predicted_completion_rate=predicted_rate,
        confidence_score=confidence,
        prediction_type=prediction_type,
        prediction_result=result,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction
