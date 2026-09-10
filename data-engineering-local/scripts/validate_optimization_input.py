import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_input.csv"


def validate_optimization_input():

    df = pd.read_csv(INPUT_FILE)

    print("Starting final optimization input validation...")
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
        "window_duration",
        "unused_window_minutes",
        "window_efficiency_score",
        "priority_bonus",
        "matching_score"
    ]

    # Check columns
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

    # Check record count
    if len(df) != 12:
        print("VALIDATION FAILED")
        print(f"Unexpected record count: {len(df)}")
        return

    print("✓ Total candidate count is correct.")

    # Check task-window combinations
    duplicate_combinations = df[
        ["task_id", "window_date", "window_start", "window_end"]
    ].duplicated()

    if duplicate_combinations.any():
        print("VALIDATION FAILED")
        print("Duplicate task-window combinations found.")
        return

    print("✓ Task-window combinations are unique.")

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

    # Check durations
    if (df["maintenance_duration"] <= 0).any():
        print("VALIDATION FAILED")
        print("Invalid maintenance duration found.")
        return

    if (df["window_duration"] <= 0).any():
        print("VALIDATION FAILED")
        print("Invalid window duration found.")
        return

    print("✓ Duration values are valid.")

    # Check window capacity
    if (
        df["window_duration"]
        < df["maintenance_duration"]
    ).any():
        print("VALIDATION FAILED")
        print("Some windows cannot accommodate maintenance.")
        return

    print("✓ All windows can accommodate maintenance.")

    # Check unused time
    if (df["unused_window_minutes"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative unused window time found.")
        return

    print("✓ Unused window times are valid.")

    # Check efficiency
    if (
        (df["window_efficiency_score"] <= 0)
        | (df["window_efficiency_score"] > 1)
    ).any():
        print("VALIDATION FAILED")
        print("Invalid efficiency scores found.")
        return

    print("✓ Window efficiency scores are valid.")

    # Check matching score
    if (df["matching_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative matching scores found.")
        return

    print("✓ Matching scores are valid.")

    # Check sorting within each section
    sorted_check = True

    for section in df["section_id"].unique():

        section_scores = df[
            df["section_id"] == section
        ]["matching_score"]

        if not section_scores.is_monotonic_decreasing:
            sorted_check = False
            break

    if not sorted_check:
        print("VALIDATION FAILED")
        print(
            "Candidates are not sorted by matching score "
            "within sections."
        )
        return

    print(
        "✓ Candidates are sorted by matching score "
        "within each section."
    )

    print("-----------------------------------")
    print("FINAL OPTIMIZATION INPUT VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total candidates: {len(df)}")
    print(f"Total features: {len(df.columns)}")

    print("-----------------------------------")


if __name__ == "__main__":
    validate_optimization_input()