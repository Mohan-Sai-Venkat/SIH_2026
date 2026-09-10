import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "optimization_input.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "optimization_summary.csv"


def create_optimization_summary():

    df = pd.read_csv(INPUT_FILE)

    print("Creating optimization summary...")
    print("-----------------------------------")

    # Select the highest-scoring window for each task
    summary = (
        df.sort_values(
            by="matching_score",
            ascending=False
        )
        .groupby("task_id", as_index=False)
        .first()
    )

    summary_columns = [
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

    summary = summary[summary_columns]

    # Sort by priority and matching score
    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }

    summary["priority_order"] = (
        summary["priority_level"].map(priority_order)
    )

    summary = summary.sort_values(
        by=["priority_order", "matching_score"],
        ascending=[True, False]
    )

    summary = summary.drop(
        columns=["priority_order"]
    )

    summary.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Best window selected for each task.")
    print("✓ Summary sorted by priority and matching score.")
    print("✓ Optimization summary created.")

    print("-----------------------------------")
    print("OPTIMIZATION SUMMARY CREATED")
    print("-----------------------------------")

    print(f"Total tasks: {len(summary)}")
    print(f"Total features: {len(summary.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    create_optimization_summary()