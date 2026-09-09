import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TASK_FILE = BASE_DIR / "processed" / "optimization_dataset.csv"
WINDOW_FILE = BASE_DIR / "processed" / "available_block_windows.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "task_window_matches.csv"


def create_task_window_matches():

    tasks = pd.read_csv(TASK_FILE)
    windows = pd.read_csv(WINDOW_FILE)

    print("Starting task-to-window matching...")
    print("-----------------------------------")

    # Standardize section IDs
    tasks["section_id"] = (
        tasks["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    windows["section_id"] = (
        windows["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Standardize dates
    tasks["requested_date"] = pd.to_datetime(
        tasks["requested_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    windows["date"] = pd.to_datetime(
        windows["date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Convert durations to numbers
    tasks["maintenance_duration"] = pd.to_numeric(
        tasks["maintenance_duration"],
        errors="coerce"
    )

    windows["window_duration"] = pd.to_numeric(
        windows["window_duration"],
        errors="coerce"
    )

    matches = []

    # Compare every task with every available window
    for _, task in tasks.iterrows():

        for _, window in windows.iterrows():

            same_section = (
                task["section_id"] == window["section_id"]
            )

            same_date = (
                task["requested_date"] == window["date"]
            )

            enough_time = (
                window["window_duration"]
                >= task["maintenance_duration"]
            )

            if same_section and same_date and enough_time:

                matches.append({
                    "task_id": task["task_id"],
                    "department": task["department"],
                    "section_id": task["section_id"],
                    "priority_score": task["priority_score"],
                    "priority_level": task["priority_level"],
                    "maintenance_duration": task["maintenance_duration"],
                    "window_date": window["date"],
                    "window_start": window["window_start"],
                    "window_end": window["window_end"],
                    "window_duration": window["window_duration"]
                })

    result = pd.DataFrame(matches)

    # Save the matching dataset
    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Tasks loaded.")
    print("✓ Available windows loaded.")
    print("✓ Section matching completed.")
    print("✓ Date matching completed.")
    print("✓ Duration compatibility checked.")
    print("✓ Task-to-window matches created.")

    print("-----------------------------------")
    print("TASK-TO-WINDOW MATCHING COMPLETED")
    print("-----------------------------------")

    print(f"Total possible matches: {len(result)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    create_task_window_matches()