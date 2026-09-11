import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("data/training_data.csv")


# Remove unnecessary columns
data = data.drop(columns=["task_id", "location"])


# Encode department
department_encoder = LabelEncoder()
data["department"] = department_encoder.fit_transform(data["department"])


# Encode asset type
asset_encoder = LabelEncoder()
data["asset_type"] = asset_encoder.fit_transform(data["asset_type"])


# Separate input and output
X = data.drop(columns=["priority_level"])
y = data["priority_level"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Load trained model
model = joblib.load("models/priority_model.pkl")


# Predict test data
predictions = model.predict(X_test)


# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)


print()
print("Model Evaluation")
print("============================")
print("Test Samples:", len(X_test))
print("Accuracy:", round(accuracy, 2))


print()
print("Classification Report")
print("----------------------------")
print(classification_report(y_test, predictions, zero_division=0))