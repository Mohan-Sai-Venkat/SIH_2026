import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input file
TRAIN_FILE = BASE_DIR / "processed" / "train_movements.csv"

# Output file
OUTPUT_FILE = BASE_DIR / "processed" / "train_summary.csv"


def create_train_summary():

    # Read train movement data
    trains = pd.read_csv(TRAIN_FILE)

    print("Starting train movement processing...")
    print("-----------------------------------")

    # Standardize section IDs
    trains["section_id"] = (
        trains["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Standardize dates
    trains["date"] = pd.to_datetime(
        trains["date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Create summary for each section and date
    summary = (
        trains
        .groupby(["section_id", "date"])
        .agg(
            train_count=("train_id", "count"),
            high_priority_train_count=(
                "train_priority",
                lambda x: (x == "High").sum()
            ),
            first_train_arrival=("arrival_time", "min"),
            last_train_departure=("departure_time", "max")
        )
        .reset_index()
    )

    # Save summary
    summary.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Train movement data loaded.")
    print(f"Train records: {len(trains)}")

    print("✓ Train movement summary created.")

    print("-----------------------------------")
    print("TRAIN SUMMARY COMPLETED")
    print("-----------------------------------")
    print(f"Summary records: {len(summary)}")
    print(f"Output file: {OUTPUT_FILE}")
    print("-----------------------------------")


if __name__ == "__main__":
    create_train_summary()