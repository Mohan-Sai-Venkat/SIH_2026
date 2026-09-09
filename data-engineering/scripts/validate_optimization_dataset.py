import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_dataset.csv"


def validate_optimization_dataset():

    df = pd.read_csv(INPUT_FILE)

    print("Starting railway optimization dataset validation...")
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
        "block_request_id",
        "requested_date",
        "requested_start",
        "requested_end",
        "duration",
        "reason",
        "train_count",
        "high_priority_train_count",
        "first_train_arrival",
        "last_train_departure",
        "section_name",
        "start_location",
        "end_location",
        "distance_km",
        "days_to_due",
        "is_overdue",
        "severity_score",
        "urgency_score",
        "train_activity_score",
        "high_priority_train_score",
        "priority_score",
        "priority_level"
    ]

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("VALIDATION FAILED")
        print("Missing columns:", missing_columns)
        return

    print("✓ All required optimization columns are present.")

    # Check task IDs
    if df["task_id"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing task IDs found.")
        return

    print("✓ All task IDs are present.")

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

    # Check departments
    valid_departments = [
        "Engineering",
        "S&T",
        "TRD"
    ]

    if not df["department"].isin(valid_departments).all():
        print("VALIDATION FAILED")
        print("Invalid department values found.")
        return

    print("✓ Department values are valid.")

    # Check severity
    valid_severity = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    if not df["severity"].isin(valid_severity).all():
        print("VALIDATION FAILED")
        print("Invalid severity values found.")
        return

    print("✓ Severity values are valid.")

    # Check maintenance duration
    if (df["maintenance_duration"] <= 0).any():
        print("VALIDATION FAILED")
        print("Invalid maintenance durations found.")
        return

    print("✓ Maintenance durations are valid.")

    # Check priority levels
    valid_priority_levels = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    if not df["priority_level"].isin(valid_priority_levels).all():
        print("VALIDATION FAILED")
        print("Invalid priority levels found.")
        return

    print("✓ Priority levels are valid.")

    # Check priority scores
    if df["priority_score"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing priority scores found.")
        return

    if (df["priority_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative priority scores found.")
        return

    print("✓ Priority scores are valid.")

    # Check train counts
    if (df["train_count"] < 0).any():
        print("VALIDATION FAILED")
        print("Invalid train counts found.")
        return

    if (df["high_priority_train_count"] < 0).any():
        print("VALIDATION FAILED")
        print("Invalid high-priority train counts found.")
        return

    print("✓ Train activity data is valid.")

    # Check corridor distances
    if df["distance_km"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing corridor distances found.")
        return

    if (df["distance_km"] <= 0).any():
        print("VALIDATION FAILED")
        print("Invalid corridor distances found.")
        return

    print("✓ Corridor information is valid.")

    print("-----------------------------------")
    print("RAILWAY OPTIMIZATION DATASET VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total records: {len(df)}")
    print(f"Total features: {len(df.columns)}")

    print("-----------------------------------")


if __name__ == "__main__":
    validate_optimization_dataset()