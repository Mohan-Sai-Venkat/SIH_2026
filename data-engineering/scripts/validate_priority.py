import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input file
INPUT_FILE = BASE_DIR / "processed" / "priority_features.csv"


def validate_priority_features():

    df = pd.read_csv(INPUT_FILE)

    print("Starting priority feature validation...")
    print("-----------------------------------")

    # Required columns
    required_columns = [
        "task_id",
        "severity",
        "days_to_due",
        "is_overdue",
        "severity_score",
        "urgency_score",
        "train_activity_score",
        "high_priority_train_score",
        "priority_score"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("VALIDATION FAILED")
        print("Missing columns:", missing_columns)
        return

    print("✓ All priority feature columns are present.")

    # Check task IDs
    if df["task_id"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing task IDs found.")
        return

    print("✓ All task IDs are present.")

    # Check severity scores
    valid_severity_scores = [1, 2, 3, 4]

    if not df["severity_score"].isin(
        valid_severity_scores
    ).all():
        print("VALIDATION FAILED")
        print("Invalid severity scores found.")
        return

    print("✓ Severity scores are valid.")

    # Check urgency scores
    valid_urgency_scores = [0, 2, 3, 4]

    if not df["urgency_score"].isin(
        valid_urgency_scores
    ).all():
        print("VALIDATION FAILED")
        print("Invalid urgency scores found.")
        return

    print("✓ Urgency scores are valid.")

    # Check overdue indicator
    if not df["is_overdue"].isin([0, 1]).all():
        print("VALIDATION FAILED")
        print("Invalid overdue indicators found.")
        return

    print("✓ Overdue indicators are valid.")

    # Check train activity scores
    if (df["train_activity_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Invalid train activity scores found.")
        return

    print("✓ Train activity scores are valid.")

    # Check high-priority train scores
    if (df["high_priority_train_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Invalid high-priority train scores found.")
        return

    print("✓ High-priority train scores are valid.")

    # Check priority score
    if df["priority_score"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing priority scores found.")
        return

    if (df["priority_score"] < 0).any():
        print("VALIDATION FAILED")
        print("Negative priority scores found.")
        return

    print("✓ Priority scores are valid.")

    # Check total records
    print("-----------------------------------")
    print("PRIORITY FEATURE VALIDATION PASSED ✓")
    print("-----------------------------------")
    print(f"Total records: {len(df)}")
    print(
        f"Highest priority score: "
        f"{df['priority_score'].max()}"
    )
    print(
        f"Lowest priority score: "
        f"{df['priority_score'].min()}"
    )


if __name__ == "__main__":
    validate_priority_features()