import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_candidates.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "optimization_input.csv"


def create_optimization_input():

    df = pd.read_csv(INPUT_FILE)

    print("Creating final optimization input dataset...")
    print("-----------------------------------")

    selected_columns = [
        "task_id",
        "department",
        "section_id",
        "priority_score",
        "priority_level",
        "maintenance_duration",
        "window_date",
        "window_start",
        "window_end",
        "window_duration",
        "unused_window_minutes",
        "window_efficiency_score",
        "priority_bonus",
        "matching_score"
    ]

    df = df[selected_columns]

    # Sort by section and matching score
    df = df.sort_values(
        by=["section_id", "matching_score"],
        ascending=[True, False]
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Required optimization fields selected.")
    print("✓ Candidates sorted by section and matching score.")
    print("✓ Final optimization input dataset created.")

    print("-----------------------------------")
    print("OPTIMIZATION INPUT DATASET CREATED")
    print("-----------------------------------")

    print(f"Total candidates: {len(df)}")
    print(f"Total features: {len(df.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    create_optimization_input()