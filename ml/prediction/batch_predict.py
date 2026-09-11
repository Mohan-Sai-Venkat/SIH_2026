import pandas as pd
import joblib


# Load trained model
model = joblib.load("models/priority_model.pkl")

# Load encoders
department_encoder = joblib.load("models/department_encoder.pkl")
asset_encoder = joblib.load("models/asset_encoder.pkl")


def predict_batch():

    # Load maintenance tasks
    data = pd.read_csv("data/training_data.csv")

    # Keep task IDs
    task_ids = data["task_id"]

    # Remove columns not used by the model
    data = data.drop(columns=["task_id", "location", "priority_level"])

    # Encode categorical columns
    data["department"] = department_encoder.transform(data["department"])
    data["asset_type"] = asset_encoder.transform(data["asset_type"])

    # Predict priorities
    predictions = model.predict(data)

    # Get prediction probabilities
    probabilities = model.predict_proba(data)

    # Highest probability for each task
    scores = probabilities.max(axis=1)

    # Create result table
    results = pd.DataFrame({
        "task_id": task_ids,
        "priority_level": predictions,
        "priority_score": scores.round(2)
    })

    return results


if __name__ == "__main__":

    results = predict_batch()

    print("\nBatch AI Prediction")
    print("============================")
    print(results.to_string(index=False))