import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_handoff.csv"


def validate_optimization_handoff():

    df = pd.read_csv(INPUT_FILE)

    print("Starting final optimization handoff validation...")
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
        "matching_score",
        "optimization_rank"
    ]

    missing_columns = [
        column
        for column in required_columns
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

    print("✓ Task IDs are unique.")

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
        print("Some windows cannot accommodate maintenance.")
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

    # Check optimization ranks
    expected_ranks = list(range(1, len(df) + 1))

    if sorted(df["optimization_rank"].tolist()) != expected_ranks:
        print("VALIDATION FAILED")
        print("Invalid optimization ranks found.")
        return

    print("✓ Optimization ranks are valid.")

    print("-----------------------------------")
    print("FINAL OPTIMIZATION HANDOFF VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total tasks: {len(df)}")
    print(f"Total features: {len(df.columns)}")

    print("-----------------------------------")


if __name__ == "__main__":
    validate_optimization_handoff()