import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "processed" / "block_windows.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "available_block_windows.csv"


def create_available_windows():

    df = pd.read_csv(INPUT_FILE)

    print("Starting available block-window creation...")
    print("-----------------------------------")

    # Keep only available windows
    available = df[
        df["availability_status"].astype(str).str.strip().str.lower()
        == "available"
    ].copy()

    # Required columns
    columns = [
        "section_id",
        "date",
        "window_start",
        "window_end",
        "window_duration",
        "availability_status"
    ]

    available = available[columns]

    # Standardize section IDs
    available["section_id"] = (
        available["section_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Convert date to standard format
    available["date"] = pd.to_datetime(
        available["date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Convert duration to numeric
    available["window_duration"] = pd.to_numeric(
        available["window_duration"],
        errors="coerce"
    )

    # Save the available windows
    available.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✓ Block-window data loaded.")
    print("✓ Available windows filtered.")
    print("✓ Section IDs standardized.")
    print("✓ Dates standardized.")
    print("✓ Window durations validated.")
    print("✓ Available block-window dataset created.")

    print("-----------------------------------")
    print("AVAILABLE BLOCK-WINDOW CREATION COMPLETED")
    print("-----------------------------------")

    print(f"Available windows: {len(available)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("-----------------------------------")


if __name__ == "__main__":
    create_available_windows()