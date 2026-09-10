import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input file
INPUT_FILE = BASE_DIR / "processed" / "priority_features.csv"

# Output file
OUTPUT_FILE = BASE_DIR / "processed" / "priority_features.csv"


def create_priority_levels():

    # Read priority feature data
    df = pd.read_csv(INPUT_FILE)

    print("Starting priority level generation...")
    print("-----------------------------------")

    # Convert priority score to numeric
    df["priority_score"] = pd.to_numeric(
        df["priority_score"],
        errors="coerce"
    )

    # Create priority level
    def get_priority_level(score):

        if score >= 60:
            return "Critical"

        elif score >= 45:
            return "High"

        elif score >= 30:
            return "Medium"

        else:
            return "Low"

    df["priority_level"] = df["priority_score"].apply(
        get_priority_level
    )

    # Save updated dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Priority levels generated.")

    print("-----------------------------------")
    print("PRIORITY LEVEL GENERATION COMPLETED")
    print("-----------------------------------")

    print(f"Total records: {len(df)}")

    print("Priority distribution:")
    print(
        df["priority_level"]
        .value_counts()
        .to_string()
    )

    print("-----------------------------------")
    print(f"Output file: {OUTPUT_FILE}")
    print("-----------------------------------")


if __name__ == "__main__":
    create_priority_levels()