import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "task_window_matches.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "optimization_candidates.csv"


def calculate_matching_score():

    df = pd.read_csv(INPUT_FILE)

    print("Starting optimization candidate scoring...")
    print("-----------------------------------")

    # Convert numeric fields
    df["priority_score"] = pd.to_numeric(
        df["priority_score"],
        errors="coerce"
    )

    df["maintenance_duration"] = pd.to_numeric(
        df["maintenance_duration"],
        errors="coerce"
    )

    df["window_duration"] = pd.to_numeric(
        df["window_duration"],
        errors="coerce"
    )

    # Calculate unused time in the block window
    df["unused_window_minutes"] = (
        df["window_duration"]
        - df["maintenance_duration"]
    )

    # Efficiency score:
    # Higher value means less unused block time.
    df["window_efficiency_score"] = (
        df["maintenance_duration"]
        / df["window_duration"]
    )

    # Priority-level bonus
    priority_bonus = {
        "Critical": 20,
        "High": 15,
        "Medium": 10,
        "Low": 5
    }

    df["priority_bonus"] = df["priority_level"].map(
        priority_bonus
    )

    # Final matching score
    df["matching_score"] = (
        df["priority_score"]
        + df["priority_bonus"]
        + df["window_efficiency_score"] * 10
    )

    # Sort highest score first
    df = df.sort_values(
        by="matching_score",
        ascending=False
    )

    # Save candidates
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Priority information processed.")
    print("✓ Window efficiency calculated.")
    print("✓ Priority bonuses added.")
    print("✓ Matching scores calculated.")
    print("✓ Optimization candidates created.")

    print("-----------------------------------")
    print("OPTIMIZATION CANDIDATE SCORING COMPLETED")
    print("-----------------------------------")

    print(f"Total candidates: {len(df)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    calculate_matching_score()