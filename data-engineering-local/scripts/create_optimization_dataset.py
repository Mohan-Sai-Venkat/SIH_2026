import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "integrated_maintenance.csv"
PRIORITY_FILE = BASE_DIR / "processed" / "priority_features.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "optimization_dataset.csv"


def create_optimization_dataset():

    integrated = pd.read_csv(INPUT_FILE)
    priority = pd.read_csv(PRIORITY_FILE)

    print("Starting railway optimization dataset creation...")
    print("-----------------------------------")

    # Select important maintenance and block fields
    integrated_columns = [
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
        "distance_km"
    ]

    priority_columns = [
        "task_id",
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
    missing_integrated = [
        column for column in integrated_columns
        if column not in integrated.columns
    ]

    missing_priority = [
        column for column in priority_columns
        if column not in priority.columns
    ]

    if missing_integrated or missing_priority:
        print("DATASET CREATION FAILED")

        if missing_integrated:
            print("Missing integrated columns:", missing_integrated)

        if missing_priority:
            print("Missing priority columns:", missing_priority)

        return

    # Select required columns
    integrated_data = integrated[integrated_columns].copy()
    priority_data = priority[priority_columns].copy()

    # Merge priority information
    optimization = pd.merge(
        integrated_data,
        priority_data,
        on="task_id",
        how="left"
    )

    # Save optimization dataset
    optimization.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Maintenance data selected.")
    print("✓ Block request data selected.")
    print("✓ Train activity data selected.")
    print("✓ Corridor data selected.")
    print("✓ Priority data added.")
    print("✓ Railway optimization dataset created.")

    print("-----------------------------------")
    print("RAILWAY OPTIMIZATION DATASET CREATED")
    print("-----------------------------------")

    print(f"Total records: {len(optimization)}")
    print(f"Total features: {len(optimization.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    create_optimization_dataset()