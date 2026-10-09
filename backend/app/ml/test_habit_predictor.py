
from app.ml.habit_predictor import HabitPredictor


def main():
    # Synthetic sample data for testing only.
    # Features: completion rate, current streak, logs in the last 30 days.
    X = [
        [95, 12, 28],
        [85, 8, 25],
        [75, 5, 22],
        [60, 3, 18],
        [30, 1, 10],
        [20, 0, 6],
        [90, 10, 27],
        [40, 1, 12],
    ]

    # 1 = completed, 0 = not completed
    y = [1, 1, 1, 1, 0, 0, 1, 0]

    predictor = HabitPredictor()
    predictor.train(X, y)

    sample_habit = [80, 6, 24]
    probability = predictor.predict_completion_probability(sample_habit)

    print("Model training: SUCCESS")
    print(f"Predicted completion probability: {probability}%")
    print("Note: This is a synthetic-data demonstration, not a validated forecast.")


if __name__ == "__main__":
    main()
