import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "task_window_matches.csv"


def validate_task_window_matches():

    df = pd.read_csv(INPUT_FILE)

    print("Starting task-to-window match validation...")
    print("-----------------------------------")

    required_columns = [
        "task_id",
        "department",
        "section_id",
        "priority_score",
        "priority_level",
        "maintenance_duration",
        "window_date",
        "window_start",
        "window_end",
        "window_duration"
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

    # Check missing values
    if df[required_columns].isnull().any().any():
        print("VALIDATION FAILED")
        print("Missing values found.")
        return

    print("✓ No missing values found.")

    # Check task IDs
    if df["task_id"].duplicated().any():
        # A task may have multiple compatible windows,
        # so duplicate task IDs are allowed.
        print("✓ Multiple windows per task are allowed.")
    else:
        print("✓ Task IDs are present.")

    # Check sections
    valid_sections = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6"
    ]

    if not df["section_id"].isin(valid_sections).all():
        print("VALIDATION FAILED")
        print("Invalid section IDs found.")
        return

    print("✓ Section IDs are valid.")

    # Check priority levels
    valid_priority_levels = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    if not df["priority_level"].isin(
        valid_priority_levels
    ).all():
        print("VALIDATION FAILED")
        print("Invalid priority levels found.")
        return

    print("✓ Priority levels are valid.")

    # Convert durations to numeric
    df["maintenance_duration"] = pd.to_numeric(
        df["maintenance_duration"],
        errors="coerce"
    )

    df["window_duration"] = pd.to_numeric(
        df["window_duration"],
        errors="coerce"
    )

    if df["maintenance_duration"].isnull().any():
        print("VALIDATION FAILED")
        print("Invalid maintenance durations found.")
        return

    if df["window_duration"].isnull().any():
        print("VALIDATION FAILED")
        print("Invalid window durations found.")
        return

    print("✓ Duration values are valid.")

    # Check that every matched window has enough time
    if (
        df["window_duration"]
        < df["maintenance_duration"]
    ).any():

        print("VALIDATION FAILED")
        print("Incompatible duration matches found.")
        return

    print("✓ All matched windows have sufficient duration.")

    # Check match count
    if len(df) != 12:
        print("VALIDATION FAILED")
        print("Unexpected number of matches:", len(df))
        return

    print("✓ Total match count is correct.")

    print("-----------------------------------")
    print("TASK-TO-WINDOW MATCH VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total possible matches: {len(df)}")
    print(
        f"Unique tasks with matches: "
        f"{df['task_id'].nunique()}"
    )

    print("-----------------------------------")


if __name__ == "__main__":
    validate_task_window_matches()