import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ============================================================
# 1. LOAD DATA ENGINEERING DATASET
# ============================================================

DATA_PATH = "data/ai_ready_dataset.csv"

data = pd.read_csv(DATA_PATH)

print("=" * 70)
print("RAILWAY AI/ML PRIORITY MODEL TRAINING")
print("=" * 70)

print("\nDataset loaded successfully!")
print("Dataset shape:", data.shape)

print("\nColumns:")
print(data.columns.tolist())

print("\nMissing values:")
print(data.isnull().sum())


# ============================================================
# 2. SELECT FEATURES
# ============================================================

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

target = "priority_level"

X = data[features].copy()
y = data[target].copy()

print("\n" + "=" * 70)
print("FEATURES USED BY AI")
print("=" * 70)

for feature in features:
    print("-", feature)

print("\nTarget:", target)


# ============================================================
# 3. ENCODE DEPARTMENT
# ============================================================

department_encoder = LabelEncoder()

X["department"] = department_encoder.fit_transform(
    X["department"]
)

print("\nDepartment encoding:")
for label, value in zip(
    department_encoder.classes_,
    range(len(department_encoder.classes_))
):
    print(f"{label} -> {value}")


# ============================================================
# 4. CHECK TARGET DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("PRIORITY DISTRIBUTION")
print("=" * 70)

print(y.value_counts())


# ============================================================
# 5. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 6. TRAIN RANDOM FOREST
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("\nModel trained successfully!")


# ============================================================
# 7. EVALUATE MODEL
# ============================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 70)
print("MODEL EVALUATION")
print("=" * 70)

print("\nAccuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))


# ============================================================
# 8. FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\n" + "=" * 70)
print("FEATURE IMPORTANCE")
print("=" * 70)

print(importance.to_string(index=False))


# ============================================================
# 9. SAVE MODEL
# ============================================================

joblib.dump(
    model,
    "models/priority_model.pkl"
)

joblib.dump(
    department_encoder,
    "models/department_encoder.pkl"
)

print("\n" + "=" * 70)
print("MODEL SAVED")
print("=" * 70)

print("models/priority_model.pkl")
print("models/department_encoder.pkl")

print("\nAI/ML training completed successfully!")