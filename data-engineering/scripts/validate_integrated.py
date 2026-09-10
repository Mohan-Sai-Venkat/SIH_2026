import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input file
INPUT_FILE = BASE_DIR / "processed" / "integrated_maintenance.csv"


def validate_integrated_data():

    # Read integrated data
    df = pd.read_csv(INPUT_FILE)

    print("Starting complete integrated data validation...")
    print("-----------------------------------")

    # Required columns
    required_columns = [
        "task_id",
        "source_system",
        "department",
        "asset_id",
        "section_id",
        "maintenance_type",
        "severity",
        "reported_date",
        "due_date",
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
        "distance_km"
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

    print("✓ All required columns are present.")

    # Check task IDs
    if df["task_id"].isnull().any():
        print("VALIDATION FAILED")
        print("Missing task IDs found.")
        return

    print("✓ All maintenance tasks have task IDs.")

    # Check duplicate task IDs
    duplicate_tasks = df["task_id"].duplicated().sum()

    if duplicate_tasks > 0:
        print("VALIDATION FAILED")
        print(f"Duplicate task IDs found: {duplicate_tasks}")
        return

    print("✓ No duplicate task IDs found.")

    # Check departments
    valid_departments = [
        "Engineering",
        "S&T",
        "TRD"
    ]

    if (~df["department"].isin(valid_departments)).any():
        print("VALIDATION FAILED")
        print("Invalid departments found.")
        return

    print("✓ Department values are valid.")

    # Check severity
    valid_severity = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    if (~df["severity"].isin(valid_severity)).any():
        print("VALIDATION FAILED")
        print("Invalid severity values found.")
        return

    print("✓ Severity values are valid.")

    # Check maintenance duration
    maintenance_duration = pd.to_numeric(
        df["maintenance_duration"],
        errors="coerce"
    )

    if maintenance_duration.isnull().any() or (
        maintenance_duration <= 0
    ).any():
        print("VALIDATION FAILED")
        print("Invalid maintenance durations found.")
        return

    print("✓ Maintenance durations are valid.")

    # Check BDMS block duration
    block_duration = pd.to_numeric(
        df["duration"],
        errors="coerce"
    )

    invalid_block_duration = (
        df["block_request_id"].notna()
        & (
            block_duration.isnull()
            | (block_duration <= 0)
        )
    )

    if invalid_block_duration.any():
        print("VALIDATION FAILED")
        print("Invalid BDMS block durations found.")
        return

    print("✓ BDMS block durations are valid.")

    # Check train count
    train_count = pd.to_numeric(
        df["train_count"],
        errors="coerce"
    )

    invalid_train_count = (
        df["train_count"].notna()
        & (
            train_count.isnull()
            | (train_count < 0)
        )
    )

    if invalid_train_count.any():
        print("VALIDATION FAILED")
        print("Invalid train counts found.")
        return

    print("✓ Train counts are valid.")

    # Check high-priority train count
    high_priority_count = pd.to_numeric(
        df["high_priority_train_count"],
        errors="coerce"
    )

    invalid_high_priority = (
        df["high_priority_train_count"].notna()
        & (
            high_priority_count.isnull()
            | (high_priority_count < 0)
        )
    )

    if invalid_high_priority.any():
        print("VALIDATION FAILED")
        print("Invalid high-priority train counts found.")
        return

    print("✓ High-priority train counts are valid.")

    # Check train priority relation
    invalid_priority_relation = (
        df["train_count"].notna()
        & df["high_priority_train_count"].notna()
        & (high_priority_count > train_count)
    )

    if invalid_priority_relation.any():
        print("VALIDATION FAILED")
        print("High-priority train count exceeds total train count.")
        return

    print("✓ Train priority counts are consistent.")

    # Check corridor information
    corridor_columns = [
        "section_name",
        "start_location",
        "end_location",
        "distance_km"
    ]

    missing_corridor = df[corridor_columns].isnull().any(axis=1)

    if missing_corridor.any():
        print("VALIDATION FAILED")
        print("Missing corridor information found.")
        print(
            df.loc[
                missing_corridor,
                ["task_id", "section_id"]
            ]
        )
        return

    print("✓ Corridor information is available for all records.")

    # Check distance
    distance = pd.to_numeric(
        df["distance_km"],
        errors="coerce"
    )

    if distance.isnull().any() or (distance <= 0).any():
        print("VALIDATION FAILED")
        print("Invalid corridor distances found.")
        return

    print("✓ Corridor distances are valid.")

    # Summary information
    block_count = df["block_request_id"].notna().sum()
    train_info_count = df["train_count"].notna().sum()

    print(f"✓ Tasks with BDMS block requests: {block_count}")
    print(
        f"✓ Tasks without BDMS block requests: "
        f"{len(df) - block_count}"
    )

    print(
        f"✓ Records with train movement information: "
        f"{train_info_count}"
    )

    print("-----------------------------------")
    print("COMPLETE INTEGRATED DATA VALIDATION PASSED ✓")
    print("-----------------------------------")
    print(f"Total integrated records: {len(df)}")


if __name__ == "__main__":
    validate_integrated_data()