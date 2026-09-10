import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "priority_features.csv"


def validate_priority_levels():

    df = pd.read_csv(INPUT_FILE)

    print("Starting priority level validation...")
    print("-----------------------------------")

    # Check required columns
    required_columns = [
        "task_id",
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

    print("✓ Required priority columns are present.")

    # Check task IDs
    if df["task_id"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing task IDs found.")
        return

    print("✓ All task IDs are present.")

    # Check priority scores
    if df["priority_score"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing priority scores found.")
        return

    print("✓ All priority scores are present.")

    # Allowed priority levels
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

    print("✓ All priority levels are valid.")

    # Check number of records
    if len(df) != 36:
        print("VALIDATION FAILED")
        print("Unexpected number of records:", len(df))
        return

    print("✓ Total record count is correct.")

    print("-----------------------------------")
    print("PRIORITY LEVEL VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total records: {len(df)}")

    print("Priority distribution:")
    print(
        df["priority_level"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    validate_priority_levels()