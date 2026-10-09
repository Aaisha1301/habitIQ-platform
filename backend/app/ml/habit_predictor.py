
import numpy as np
from sklearn.ensemble import RandomForestClassifier


class HabitPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced"
        )
        self.is_trained = False

    def train(self, X, y):
        """Train using numeric habit features and completion labels."""
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=int)

        if len(X) < 2 or len(X) != len(y):
            raise ValueError("Provide at least 2 matching feature rows and labels.")

        if len(np.unique(y)) < 2:
            raise ValueError(
                "Training data must contain both completion classes: 0 and 1."
            )

        self.model.fit(X, y)
        self.is_trained = True

    def predict_completion_probability(self, features):
        """Return the predicted probability of completing a habit."""
        if not self.is_trained:
            raise RuntimeError("Train the model before making predictions.")

        features = np.asarray(features, dtype=float).reshape(1, -1)
        probabilities = self.model.predict_proba(features)[0]
        completed_index = list(self.model.classes_).index(1)

        return round(float(probabilities[completed_index]) * 100, 2)


def validate_training_data(X, y):
    """Check whether the dataset is suitable for basic model training."""
    if len(X) != len(y):
        return False, "Features and labels have different lengths."

    if len(X) < 20:
        return False, "Need at least 20 training examples."

    if len(set(y)) < 2:
        return False, "Training data must contain both classes: 0 and 1."

    return True, "Training data passed basic validation."


def train_if_sufficient_data(X, y):
    """Train the model only when basic dataset checks pass."""
    is_valid, message = validate_training_data(X, y)

    if not is_valid:
        return None, message

    predictor = HabitPredictor()

    try:
        predictor.train(X, y)
    except ValueError as error:
        return None, str(error)

    return predictor, "Model training successful."


def train_from_database(db, user_id):
    """Train from a user's historical habit logs when data is sufficient."""
    from app.ml.training_data import build_training_dataset

    X, y = build_training_dataset(db, user_id)
    return train_if_sufficient_data(X, y)

