import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_summary.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "optimization_handoff.csv"


def create_optimization_handoff():

    df = pd.read_csv(INPUT_FILE)

    print("Creating final optimization handoff dataset...")
    print("-----------------------------------")

    handoff_columns = [
        "task_id",
        "department",
        "section_id",
        "priority_level",
        "priority_score",
        "maintenance_duration",
        "window_date",
        "window_start",
        "window_end",
        "window_duration",
        "unused_window_minutes",
        "matching_score"
    ]

    handoff = df[handoff_columns].copy()

    # Add a simple optimization rank
    handoff["optimization_rank"] = range(
        1,
        len(handoff) + 1
    )

    handoff.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Required scheduling fields selected.")
    print("✓ Optimization ranks assigned.")
    print("✓ Final handoff dataset created.")

    print("-----------------------------------")
    print("OPTIMIZATION HANDOFF DATASET CREATED")
    print("-----------------------------------")

    print(f"Total tasks: {len(handoff)}")
    print(f"Total features: {len(handoff.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    create_optimization_handoff()