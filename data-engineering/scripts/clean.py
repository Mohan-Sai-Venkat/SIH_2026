import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output files
INPUT_FILE = BASE_DIR / "processed" / "maintenance_tasks.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "maintenance_tasks.csv"


def clean_maintenance_data():

    # Read the integrated maintenance data
    df = pd.read_csv(INPUT_FILE)

    print("Starting data cleaning...")
    print(f"Records before cleaning: {len(df)}")

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate records
    df = df.drop_duplicates(subset=["task_id"])

    # Remove extra spaces from text columns
    text_columns = [
        "task_id",
        "source_system",
        "department",
        "asset_id",
        "section_id",
        "maintenance_type",
        "severity",
        "status"
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # Standardize department names
    df["department"] = df["department"].replace({
        "engineering": "Engineering",
        "ENG": "Engineering",
        "Engg": "Engineering",
        "S&T": "S&T",
        "s&t": "S&T",
        "ST": "S&T",
        "Signalling": "S&T",
        "Signaling": "S&T",
        "TRD": "TRD",
        "trd": "TRD",
        "Traction": "TRD",
        "traction": "TRD"
    })

    # Standardize section IDs
    df["section_id"] = df["section_id"].str.upper()

    # Convert date columns into proper date format
    df["reported_date"] = pd.to_datetime(
        df["reported_date"],
        errors="coerce"
    )

    df["due_date"] = pd.to_datetime(
        df["due_date"],
        errors="coerce"
    )

    # Convert maintenance duration into numeric values
    df["maintenance_duration"] = pd.to_numeric(
        df["maintenance_duration"],
        errors="coerce"
    )

    # Remove records with invalid essential values
    df = df.dropna(
        subset=[
            "task_id",
            "section_id",
            "reported_date",
            "due_date",
            "maintenance_duration"
        ]
    )

    # Make sure maintenance duration is positive
    df = df[df["maintenance_duration"] > 0]

    # Convert dates back to YYYY-MM-DD format
    df["reported_date"] = df["reported_date"].dt.strftime("%Y-%m-%d")
    df["due_date"] = df["due_date"].dt.strftime("%Y-%m-%d")

    # Save cleaned data
    df.to_csv(OUTPUT_FILE, index=False)

    print("-----------------------------------")
    print("DATA CLEANING COMPLETED")
    print("-----------------------------------")
    print(f"Records after cleaning: {len(df)}")
    print(f"Cleaned file: {OUTPUT_FILE}")
    print("-----------------------------------")


if __name__ == "__main__":
    clean_maintenance_data()