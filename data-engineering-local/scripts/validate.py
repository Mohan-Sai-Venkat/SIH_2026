import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input file
INPUT_FILE = BASE_DIR / "processed" / "maintenance_tasks.csv"


def validate_maintenance_data():

    # Read cleaned maintenance data
    df = pd.read_csv(INPUT_FILE)

    print("Starting data validation...")
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
        "status"
    ]

    # Check for missing columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("VALIDATION FAILED")
        print("Missing columns:", missing_columns)
        return

    print("✓ All required columns are present.")

    # Check for missing values
    missing_values = df[required_columns].isnull().sum()

    if missing_values.sum() > 0:
        print("VALIDATION FAILED")
        print("Missing values found:")
        print(missing_values[missing_values > 0])
        return

    print("✓ No missing values found.")

    # Check duplicate task IDs
    duplicate_tasks = df["task_id"].duplicated().sum()

    if duplicate_tasks > 0:
        print("VALIDATION FAILED")
        print(f"Duplicate task IDs found: {duplicate_tasks}")
        return

    print("✓ No duplicate task IDs found.")

    # Check maintenance duration
    invalid_duration = (df["maintenance_duration"] <= 0).sum()

    if invalid_duration > 0:
        print("VALIDATION FAILED")
        print(f"Invalid maintenance durations: {invalid_duration}")
        return

    print("✓ Maintenance durations are valid.")

    # Check allowed severity values
    valid_severity = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    invalid_severity = ~df["severity"].isin(valid_severity)

    if invalid_severity.any():
        print("VALIDATION FAILED")
        print("Invalid severity values found.")
        return

    print("✓ Severity values are valid.")

    # Check allowed departments
    valid_departments = [
        "Engineering",
        "S&T",
        "TRD"
    ]

    invalid_departments = ~df["department"].isin(valid_departments)

    if invalid_departments.any():
        print("VALIDATION FAILED")
        print("Invalid department values found.")
        return

    print("✓ Department values are valid.")

    print("-----------------------------------")
    print("DATA VALIDATION PASSED ✓")
    print("-----------------------------------")
    print(f"Total valid records: {len(df)}")


if __name__ == "__main__":
    validate_maintenance_data()