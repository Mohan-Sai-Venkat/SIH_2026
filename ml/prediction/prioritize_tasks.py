import pandas as pd
import joblib


# ============================================================
# LOAD TRAINED AI MODEL
# ============================================================

model = joblib.load("models/priority_model.pkl")

department_encoder = joblib.load(
    "models/department_encoder.pkl"
)


# ============================================================
# AI PRIORITIZATION
# ============================================================

def prioritize_tasks():

    # Load Data Engineering AI-ready dataset
    data = pd.read_csv("data/ai_ready_dataset.csv")

    print("\nAI-ready dataset loaded successfully!")
    print("Total tasks:", len(data))

    # Features used during model training
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

    # Keep task IDs
    task_ids = data["task_id"].copy()

    # Prepare model input
    X = data[features].copy()

    # Encode department
    X["department"] = department_encoder.transform(
        X["department"]
    )

    # AI prediction
    predictions = model.predict(X)

    # Prediction confidence
    probabilities = model.predict_proba(X)
    scores = probabilities.max(axis=1)

    # Create result table
    results = pd.DataFrame({
        "task_id": task_ids,
        "priority_level": predictions,
        "priority_score": scores
    })

    # Round confidence
    results["priority_score"] = results[
        "priority_score"
    ].round(2)

    # Highest confidence first
    results = results.sort_values(
        by="priority_score",
        ascending=False
    )

    # Reset index
    results = results.reset_index(drop=True)

    # Add rank
    results.insert(
        0,
        "rank",
        results.index + 1
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    results = prioritize_tasks()

    print("\n")
    print("=" * 70)
    print("RAILWAY AI MAINTENANCE PRIORITIZATION")
    print("=" * 70)

    print("\nTop Priority Tasks")
    print("-" * 70)

    print(
        results.head(10).to_string(index=False)
    )

    print("\nTotal tasks analyzed:", len(results))

    print("\nAI prioritization completed successfully!")