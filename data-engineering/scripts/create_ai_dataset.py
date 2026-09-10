import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "priority_features.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "ai_ready_dataset.csv"


def create_ai_dataset():

    df = pd.read_csv(INPUT_FILE)

    print("Starting AI-ready dataset creation...")
    print("-----------------------------------")

    # Important features required by the AI/ML module
    ai_columns = [
        "task_id",
        "source_system",
        "department",
        "asset_id",
        "section_id",
        "maintenance_type",
        "severity",
        "maintenance_duration",
        "status",
        "days_to_due",
        "is_overdue",
        "severity_score",
        "urgency_score",
        "train_activity_score",
        "high_priority_train_score",
        "priority_score",
        "priority_level"
    ]

    # Check that all required columns exist
    missing_columns = [
        column for column in ai_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("DATASET CREATION FAILED")
        print("Missing columns:", missing_columns)
        return

    # Select AI/ML features
    ai_df = df[ai_columns].copy()

    # Check for missing task IDs
    if ai_df["task_id"].isnull().any():
        print("DATASET CREATION FAILED")
        print("Missing task IDs found.")
        return

    # Save AI-ready dataset
    ai_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ AI/ML features selected.")
    print("✓ Dataset structure verified.")
    print("✓ AI-ready dataset created.")

    print("-----------------------------------")
    print("AI-READY DATASET CREATION COMPLETED")
    print("-----------------------------------")

    print(f"Total records: {len(ai_df)}")
    print(f"Total features: {len(ai_df.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    create_ai_dataset()