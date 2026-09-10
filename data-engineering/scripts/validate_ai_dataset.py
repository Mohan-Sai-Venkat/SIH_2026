import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "ai_ready_dataset.csv"


def validate_ai_dataset():

    df = pd.read_csv(INPUT_FILE)

    print("Starting AI-ready dataset validation...")
    print("-----------------------------------")

    required_columns = [
        "task_id",
        "source_system",
        "department",
        "asset_id",
        "section_id",
        "maintenance_type",
        "severity",
        "maintenance_duration",
        "status",
        "days_to_due",
        "is_overdue",
        "severity_score",
        "urgency_score",
        "train_activity_score",
        "high_priority_train_score",
        "priority_score",
        "priority_level"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("VALIDATION FAILED")
        print("Missing columns:", missing_columns)
        return

    print("✓ All required AI/ML columns are present.")

    # Check missing values
    if df[required_columns].isnull().any().any():
        print("VALIDATION FAILED")
        print("Missing values found in AI-ready dataset.")
        return

    print("✓ No missing values found.")

    # Check task IDs
    if df["task_id"].duplicated().any():
        print("VALIDATION FAILED")
        print("Duplicate task IDs found.")
        return

    print("✓ Task IDs are unique.")

    # Check record count
    if len(df) != 36:
        print("VALIDATION FAILED")
        print("Unexpected number of records:", len(df))
        return

    print("✓ Total record count is correct.")

    # Check severity scores
    if not df["severity_score"].isin([1, 2, 3, 4]).all():
        print("VALIDATION FAILED")
        print("Invalid severity scores found.")
        return

    print("✓ Severity scores are valid.")

    # Check urgency scores
    if not df["urgency_score"].isin([0, 2, 3, 4]).all():
        print("VALIDATION FAILED")
        print("Invalid urgency scores found.")
        return

    print("✓ Urgency scores are valid.")

    # Check overdue indicators
    if not df["is_overdue"].isin([0, 1]).all():
        print("VALIDATION FAILED")
        print("Invalid overdue indicators found.")
        return

    print("✓ Overdue indicators are valid.")

    # Check priority levels
    valid_levels = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    if not df["priority_level"].isin(valid_levels).all():
        print("VALIDATION FAILED")
        print("Invalid priority levels found.")
        return

    print("✓ Priority levels are valid.")

    # Check priority scores
    if (df["priority_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative priority scores found.")
        return

    print("✓ Priority scores are valid.")

    print("-----------------------------------")
    print("AI-READY DATASET VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total records: {len(df)}")
    print(f"Total features: {len(df.columns)}")

    print("-----------------------------------")


if __name__ == "__main__":
    validate_ai_dataset()