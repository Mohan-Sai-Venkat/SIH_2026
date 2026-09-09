import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "available_block_windows.csv"


def validate_available_windows():

    df = pd.read_csv(INPUT_FILE)

    print("Starting available block-window validation...")
    print("-----------------------------------")

    required_columns = [
        "section_id",
        "date",
        "window_start",
        "window_end",
        "window_duration",
        "availability_status"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("VALIDATION FAILED")
        print("Missing columns:", missing_columns)
        return

    print("✓ All required columns are present.")

    # Check missing values
    if df[required_columns].isnull().any().any():
        print("VALIDATION FAILED")
        print("Missing values found.")
        return

    print("✓ No missing values found.")

    # Check sections
    valid_sections = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6"
    ]

    if not df["section_id"].isin(valid_sections).all():
        print("VALIDATION FAILED")
        print("Invalid section IDs found.")
        return

    print("✓ Section IDs are valid.")

    # Check dates
    dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    if dates.isnull().any():
        print("VALIDATION FAILED")
        print("Invalid dates found.")
        return

    print("✓ Dates are valid.")

    # Check duration
    df["window_duration"] = pd.to_numeric(
        df["window_duration"],
        errors="coerce"
    )

    if df["window_duration"].isnull().any():
        print("VALIDATION FAILED")
        print("Invalid window durations found.")
        return

    if (df["window_duration"] <= 0).any():
        print("VALIDATION FAILED")
        print("Non-positive window durations found.")
        return

    print("✓ Window durations are valid.")

    # Check availability status
    if not (
        df["availability_status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("available")
        .all()
    ):
        print("VALIDATION FAILED")
        print("Non-available windows found.")
        return

    print("✓ All windows have Available status.")

    # Check record count
    if len(df) != 18:
        print("VALIDATION FAILED")
        print("Unexpected number of windows:", len(df))
        return

    print("✓ Total window count is correct.")

    print("-----------------------------------")
    print("AVAILABLE BLOCK-WINDOW VALIDATION PASSED ✓")
    print("-----------------------------------")

    print(f"Total available windows: {len(df)}")
    print(
        f"Total available minutes: "
        f"{df['window_duration'].sum()}"
    )

    print("-----------------------------------")


if __name__ == "__main__":
    validate_available_windows()