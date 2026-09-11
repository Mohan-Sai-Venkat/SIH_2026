import pandas as pd
import joblib


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = joblib.load("models/priority_model.pkl")

department_encoder = joblib.load(
    "models/department_encoder.pkl"
)


# ============================================================
# AI PRIORITY PREDICTION
# ============================================================

def predict_priority(task):

    # Copy so original task is not modified
    task = task.copy()

    # Encode department
    task["department"] = department_encoder.transform(
        [task["department"]]
    )[0]

    # Features MUST match training order
    features = [
        "department",
        "maintenance_duration",
        "days_to_due",
        "is_overdue",
        "severity_score",
        "urgency_score",
        "train_activity_score",
        "high_priority_train_score"
    ]

    # Create input dataframe
    input_data = pd.DataFrame(
        [[task[feature] for feature in features]],
        columns=features
    )

    # Prediction
    prediction = model.predict(input_data)[0]

    # Probability
    probabilities = model.predict_proba(input_data)[0]

    priority_score = float(max(probabilities))

    return prediction, priority_score


# ============================================================
# TEST THE MODEL
# ============================================================

if __name__ == "__main__":

    task = {
        "task_id": "TEST001",
        "department": "Engineering",
        "maintenance_duration": 2,
        "days_to_due": 5,
        "is_overdue": 0,
        "severity_score": 4,
        "urgency_score": 0.75,
        "train_activity_score": 0.60,
        "high_priority_train_score": 0.50
    }

    prediction, score = predict_priority(task)

    print()
    print("=" * 50)
    print("RAILWAY AI PRIORITY PREDICTION")
    print("=" * 50)

    print("Task ID:", task["task_id"])
    print("Predicted Priority:", prediction)
    print("Priority Confidence:", round(score, 2))

    print("=" * 50)