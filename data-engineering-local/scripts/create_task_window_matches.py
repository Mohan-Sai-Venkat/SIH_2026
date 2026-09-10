import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TASK_FILE = BASE_DIR / "processed" / "optimization_dataset.csv"
WINDOW_FILE = BASE_DIR / "processed" / "available_block_windows.csv"
TRAIN_FILE = BASE_DIR / "processed" / "train_movements.csv"

OUTPUT_FILE = BASE_DIR / "processed" / "task_window_matches.csv"


def time_to_minutes(time_value):
    """
    Convert HH:MM time into minutes from midnight.
    """

    hour, minute = map(
        int,
        str(time_value).split(":")
    )

    return hour * 60 + minute


def minutes_to_time(total_minutes):
    """
    Convert minutes from midnight back to HH:MM.
    """

    hour = total_minutes // 60
    minute = total_minutes % 60

    return f"{hour:02d}:{minute:02d}"


def check_train_conflict(
    section_id,
    window_date,
    maintenance_start,
    maintenance_end,
    trains
):
    """
    Check whether the maintenance period overlaps
    with any train movement in the same section and date.
    """

    maintenance_start_minutes = time_to_minutes(
        maintenance_start
    )

    maintenance_end_minutes = time_to_minutes(
        maintenance_end
    )

    section_trains = trains[
        (trains["section_id"] == section_id)
        & (trains["date"] == window_date)
    ]

    for _, train in section_trains.iterrows():

        train_arrival = time_to_minutes(
            train["arrival_time"]
        )

        train_departure = time_to_minutes(
            train["departure_time"]
        )

        overlap = (
            maintenance_start_minutes < train_departure
            and
            maintenance_end_minutes > train_arrival
        )

        if overlap:
            return True

    return False


def create_task_window_matches():

    tasks = pd.read_csv(TASK_FILE)
    windows = pd.read_csv(WINDOW_FILE)
    trains = pd.read_csv(TRAIN_FILE)

    print("Starting task-to-window matching...")
    print("-----------------------------------")

    # -----------------------------------
    # Standardize section IDs
    # -----------------------------------

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

    trains["section_id"] = (
        trains["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # -----------------------------------
    # Standardize dates
    # -----------------------------------

    tasks["requested_date"] = pd.to_datetime(
        tasks["requested_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    windows["date"] = pd.to_datetime(
        windows["date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    trains["date"] = pd.to_datetime(
        trains["date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # -----------------------------------
    # Convert durations to numbers
    # -----------------------------------

    tasks["maintenance_duration"] = pd.to_numeric(
        tasks["maintenance_duration"],
        errors="coerce"
    )

    windows["window_duration"] = pd.to_numeric(
        windows["window_duration"],
        errors="coerce"
    )

    matches = []

    rejected_train_conflicts = 0

    # -----------------------------------
    # Compare every task with every
    # available window
    # -----------------------------------

    for _, task in tasks.iterrows():

        for _, window in windows.iterrows():

            # Condition 1:
            # Same railway section
            same_section = (
                task["section_id"]
                == window["section_id"]
            )

            # Condition 2:
            # Same date
            same_date = (
                task["requested_date"]
                == window["date"]
            )

            # Condition 3:
            # Window is long enough
            enough_time = (
                window["window_duration"]
                >= task["maintenance_duration"]
            )

            # Continue only if the first three
            # conditions are satisfied.
            if (
                same_section
                and same_date
                and enough_time
            ):

                # -----------------------------------
                # Calculate actual maintenance period
                # -----------------------------------

                maintenance_start = (
                    window["window_start"]
                )

                start_minutes = time_to_minutes(
                    maintenance_start
                )

                maintenance_end_minutes = (
                    start_minutes
                    + int(task["maintenance_duration"])
                )

                maintenance_end = minutes_to_time(
                    maintenance_end_minutes
                )

                # -----------------------------------
                # Check train conflict
                # -----------------------------------

                train_conflict = check_train_conflict(
                    task["section_id"],
                    window["date"],
                    maintenance_start,
                    maintenance_end,
                    trains
                )

                if train_conflict:

                    rejected_train_conflicts += 1
                    continue

                # -----------------------------------
                # Calculate unused window time
                # -----------------------------------

                unused_window_minutes = (
                    window["window_duration"]
                    - task["maintenance_duration"]
                )

                # -----------------------------------
                # Valid task-window match
                # -----------------------------------

                matches.append({

                    "task_id":
                        task["task_id"],

                    "department":
                        task["department"],

                    "section_id":
                        task["section_id"],

                    "priority_score":
                        task["priority_score"],

                    "priority_level":
                        task["priority_level"],

                    "maintenance_duration":
                        task["maintenance_duration"],

                    "window_date":
                        window["date"],

                    "window_start":
                        window["window_start"],

                    "window_end":
                        window["window_end"],

                    "window_duration":
                        window["window_duration"],

                    "maintenance_start":
                        maintenance_start,

                    "maintenance_end":
                        maintenance_end,

                    "unused_window_minutes":
                        unused_window_minutes
                })

    result = pd.DataFrame(matches)

    # -----------------------------------
    # Save matching dataset
    # -----------------------------------

    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # -----------------------------------
    # Display results
    # -----------------------------------

    print("✓ Tasks loaded.")
    print("✓ Available windows loaded.")
    print("✓ Train movement data loaded.")

    print("✓ Section matching completed.")
    print("✓ Date matching completed.")
    print("✓ Duration compatibility checked.")
    print("✓ Maintenance start/end times calculated.")
    print("✓ Train conflict checking completed.")
    print("✓ Unused window time calculated.")
    print("✓ Feasible task-to-window matches created.")

    print("-----------------------------------")
    print("TASK-TO-WINDOW MATCHING COMPLETED")
    print("-----------------------------------")

    print(
        f"Total possible matches: {len(result)}"
    )

    print(
        f"Rejected due to train conflicts: "
        f"{rejected_train_conflicts}"
    )

    print(
        f"Output file: {OUTPUT_FILE}"
    )

    print("-----------------------------------")


if __name__ == "__main__":
    create_task_window_matches()