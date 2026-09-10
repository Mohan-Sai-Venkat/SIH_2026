import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_candidates.csv"


def validate_optimization_candidates():

    df = pd.read_csv(INPUT_FILE)

    print("Starting optimization candidate validation...")
    print("-----------------------------------")

    required_columns = [
        "task_id",
        "section_id",
        "priority_score",
        "priority_level",
        "maintenance_duration",
        "window_duration",
        "unused_window_minutes",
        "window_efficiency_score",
        "priority_bonus",
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

    # Check missing values
    if df[required_columns].isnull().any().any():
        print("VALIDATION FAILED")
        print("Missing values found.")
        return

    print("✓ No missing values found.")

    # Check candidate count
    if len(df) != 12:
        print("VALIDATION FAILED")
        print("Unexpected number of candidates:", len(df))
        return

    print("✓ Total candidate count is correct.")

    # Check duration compatibility
    if (
        df["window_duration"]
        < df["maintenance_duration"]
    ).any():

        print("VALIDATION FAILED")
        print("Incompatible window durations found.")
        return

    print("✓ All windows can accommodate maintenance.")

    # Check unused window time
    if (df["unused_window_minutes"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative unused window time found.")
        return

    print("✓ Unused window times are valid.")

    # Check efficiency score
    if (
        (df["window_efficiency_score"] <= 0)
        | (df["window_efficiency_score"] > 1)
    ).any():

        print("VALIDATION FAILED")
        print("Invalid window efficiency scores found.")
        return

    print("✓ Window efficiency scores are valid.")

    # Check priority bonus
    valid_bonuses = [5, 10, 15, 20]

    if not df["priority_bonus"].isin(valid_bonuses).all():
        print("VALIDATION FAILED")
        print("Invalid priority bonuses found.")
        return

    print("✓ Priority bonuses are valid.")

    # Check matching score
    if df["matching_score"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing matching scores found.")
        return

    if (df["matching_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative matching scores found.")
        return

    print("✓ Matching scores are valid.")

    # Check sorting
    if not df["matching_score"].is_monotonic_decreasing:
        print("VALIDATION FAILED")
        print("Candidates are not sorted by matching score.")
        return

    print("✓ Candidates are sorted by matching score.")

    print("-----------------------------------")
    print("OPTIMIZATION CANDIDATE VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total candidates: {len(df)}")
    print(
        f"Highest matching score: "
        f"{df['matching_score'].max():.2f}"
    )
    print(
        f"Lowest matching score: "
        f"{df['matching_score'].min():.2f}"
    )

    print("-----------------------------------")


if __name__ == "__main__":
    validate_optimization_candidates()