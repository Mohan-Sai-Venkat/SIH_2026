import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input files
BLOCK_FILE = BASE_DIR / "processed" / "block_requests.csv"
MAINTENANCE_FILE = BASE_DIR / "processed" / "maintenance_tasks.csv"


def validate_bdms_data():

    # Read files
    blocks = pd.read_csv(BLOCK_FILE)
    maintenance = pd.read_csv(MAINTENANCE_FILE)

    print("Starting BDMS validation...")
    print("-----------------------------------")

    # Required columns
    required_columns = [
        "block_request_id",
        "task_id",
        "department",
        "section_id",
        "requested_date",
        "requested_start",
        "requested_end",
        "duration",
        "reason"
    ]

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in blocks.columns
    ]

    if missing_columns:
        print("VALIDATION FAILED")
        print("Missing columns:", missing_columns)
        return

    print("✓ All BDMS columns are present.")

    # Check missing values
    if blocks[required_columns].isnull().sum().sum() > 0:
        print("VALIDATION FAILED")
        print("Missing values found.")
        return

    print("✓ No missing values found.")

    # Check duplicate block request IDs
    duplicate_ids = blocks["block_request_id"].duplicated().sum()

    if duplicate_ids > 0:
        print("VALIDATION FAILED")
        print(f"Duplicate block request IDs: {duplicate_ids}")
        return

    print("✓ No duplicate block request IDs found.")

    # Check whether task IDs exist in maintenance data
    maintenance_task_ids = set(maintenance["task_id"])

    invalid_tasks = blocks[
        ~blocks["task_id"].isin(maintenance_task_ids)
    ]

    if len(invalid_tasks) > 0:
        print("VALIDATION FAILED")
        print("BDMS contains task IDs that do not exist in maintenance data.")
        print(invalid_tasks["task_id"].tolist())
        return

    print("✓ All BDMS task IDs match maintenance tasks.")

    # Check duration
    blocks["duration"] = pd.to_numeric(
        blocks["duration"],
        errors="coerce"
    )

    if blocks["duration"].isnull().any():
        print("VALIDATION FAILED")
        print("Invalid duration values found.")
        return

    if (blocks["duration"] <= 0).any():
        print("VALIDATION FAILED")
        print("Duration must be greater than zero.")
        return

    print("✓ Block durations are valid.")

    # Check departments
    valid_departments = [
        "Engineering",
        "S&T",
        "TRD"
    ]

    invalid_departments = ~blocks["department"].isin(
        valid_departments
    )

    if invalid_departments.any():
        print("VALIDATION FAILED")
        print("Invalid department values found.")
        return

    print("✓ Department values are valid.")

    # Check section IDs
    valid_sections = set(maintenance["section_id"])

    invalid_sections = blocks[
        ~blocks["section_id"].isin(valid_sections)
    ]

    if len(invalid_sections) > 0:
        print("VALIDATION FAILED")
        print("Invalid section IDs found.")
        print(invalid_sections["section_id"].tolist())
        return

    print("✓ Section IDs are valid.")

    print("-----------------------------------")
    print("BDMS VALIDATION PASSED ✓")
    print("-----------------------------------")
    print(f"Total valid block requests: {len(blocks)}")


if __name__ == "__main__":
    validate_bdms_data()