import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_summary.csv"


def validate_optimization_summary():

    df = pd.read_csv(INPUT_FILE)

    print("Starting optimization summary validation...")
    print("-----------------------------------")

    required_columns = [
        "task_id",
        "department",
        "section_id",
        "priority_level",
        "priority_score",
        "maintenance_duration",
        "window_date",
        "window_start",
        "window_end",
        "window_duration",
        "unused_window_minutes",
        "matching_score"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("VALIDATION FAILED")
        print("Missing columns:", missing_columns)
        return

    print("✓ All required columns are present.")

    if df[required_columns].isnull().any().any():
        print("VALIDATION FAILED")
        print("Missing values found.")
        return

    print("✓ No missing values found.")

    if len(df) != 6:
        print("VALIDATION FAILED")
        print(f"Unexpected task count: {len(df)}")
        return

    print("✓ Total task count is correct.")

    if df["task_id"].duplicated().any():
        print("VALIDATION FAILED")
        print("Duplicate task IDs found.")
        return

    print("✓ Each task appears only once.")

    if (df["maintenance_duration"] <= 0).any():
        print("VALIDATION FAILED")
        print("Invalid maintenance duration found.")
        return

    if (df["window_duration"] <= 0).any():
        print("VALIDATION FAILED")
        print("Invalid window duration found.")
        return

    print("✓ Duration values are valid.")

    if (
        df["window_duration"]
        < df["maintenance_duration"]
    ).any():
        print("VALIDATION FAILED")
        print("Some selected windows cannot accommodate maintenance.")
        return

    print("✓ All selected windows can accommodate maintenance.")

    if (df["unused_window_minutes"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative unused window time found.")
        return

    print("✓ Unused window times are valid.")

    if (df["matching_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Invalid matching scores found.")
        return

    print("✓ Matching scores are valid.")

    valid_priorities = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    if not df["priority_level"].isin(valid_priorities).all():
        print("VALIDATION FAILED")
        print("Invalid priority levels found.")
        return

    print("✓ Priority levels are valid.")

    print("-----------------------------------")
    print("OPTIMIZATION SUMMARY VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total tasks: {len(df)}")
    print(f"Total features: {len(df.columns)}")

    print("-----------------------------------")


if __name__ == "__main__":
    validate_optimization_summary()