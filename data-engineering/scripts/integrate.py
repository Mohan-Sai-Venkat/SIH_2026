import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input files
MAINTENANCE_FILE = BASE_DIR / "processed" / "maintenance_tasks.csv"
BLOCK_FILE = BASE_DIR / "processed" / "block_requests.csv"
TRAIN_SUMMARY_FILE = BASE_DIR / "processed" / "train_summary.csv"
CORRIDOR_FILE = BASE_DIR / "processed" / "corridors.csv"

# Output file
OUTPUT_FILE = BASE_DIR / "processed" / "integrated_maintenance.csv"


def integrate_data():

    # Read input files
    maintenance = pd.read_csv(MAINTENANCE_FILE)
    blocks = pd.read_csv(BLOCK_FILE)
    train_summary = pd.read_csv(TRAIN_SUMMARY_FILE)
    corridors = pd.read_csv(CORRIDOR_FILE)

    print("Starting complete data integration...")
    print("-----------------------------------")

    # Select maintenance columns
    maintenance_columns = [
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

    maintenance = maintenance[maintenance_columns]

    # Select BDMS columns
    block_columns = [
        "block_request_id",
        "task_id",
        "requested_date",
        "requested_start",
        "requested_end",
        "duration",
        "reason"
    ]

    blocks = blocks[block_columns]

    # Merge maintenance with BDMS
    integrated = pd.merge(
        maintenance,
        blocks,
        on="task_id",
        how="left"
    )

    # Prepare dates for train summary matching
    integrated["requested_date"] = pd.to_datetime(
        integrated["requested_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    train_summary["date"] = pd.to_datetime(
        train_summary["date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Standardize section IDs
    integrated["section_id"] = (
        integrated["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    train_summary["section_id"] = (
        train_summary["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    corridors["section_id"] = (
        corridors["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Merge train summary using section + requested date
    integrated = pd.merge(
        integrated,
        train_summary,
        left_on=["section_id", "requested_date"],
        right_on=["section_id", "date"],
        how="left"
    )

    # Remove duplicate date column
    integrated = integrated.drop(
        columns=["date"],
        errors="ignore"
    )

    # Merge corridor information using section ID
    integrated = pd.merge(
        integrated,
        corridors,
        on="section_id",
        how="left"
    )

    # Save final integrated dataset
    integrated.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Maintenance data loaded.")
    print(f"Maintenance records: {len(maintenance)}")

    print("✓ BDMS block request data loaded.")
    print(f"BDMS records: {len(blocks)}")

    print("✓ Train summary data loaded.")
    print(f"Train summary records: {len(train_summary)}")

    print("✓ Corridor data loaded.")
    print(f"Corridor records: {len(corridors)}")

    print("✓ All datasets integrated.")

    print("-----------------------------------")
    print("COMPLETE DATA INTEGRATION FINISHED")
    print("-----------------------------------")
    print(f"Final records: {len(integrated)}")
    print(f"Output file: {OUTPUT_FILE}")
    print("-----------------------------------")


if __name__ == "__main__":
    integrate_data()