import pandas as pd
from pathlib import Path


# Get the data-engineering folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Input files
TMS_FILE = BASE_DIR / "raw" / "tms.csv"
SMMS_FILE = BASE_DIR / "raw" / "smms.csv"
TDMS_FILE = BASE_DIR / "raw" / "tdms.csv"
COA_FILE = BASE_DIR / "raw" / "coa.csv"
BDMS_FILE = BASE_DIR / "raw" / "bdms.csv"

# Output files
MAINTENANCE_OUTPUT = BASE_DIR / "processed" / "maintenance_tasks.csv"
TRAIN_OUTPUT = BASE_DIR / "processed" / "train_movements.csv"
BLOCK_REQUEST_OUTPUT = BASE_DIR / "processed" / "block_requests.csv"


def transform_tms():
    """Transform TMS data into the common maintenance format."""

    tms = pd.read_csv(TMS_FILE)

    return pd.DataFrame({
        "task_id": tms["task_id"],
        "source_system": "TMS",
        "department": "Engineering",
        "asset_id": tms["asset_id"],
        "section_id": tms["section_id"],
        "maintenance_type": tms["defect_type"],
        "severity": tms["severity"],
        "reported_date": tms["reported_date"],
        "due_date": tms["due_date"],
        "maintenance_duration": tms["maintenance_duration"],
        "status": tms["status"]
    })


def transform_smms():
    """Transform SMMS data into the common maintenance format."""

    smms = pd.read_csv(SMMS_FILE)

    return pd.DataFrame({
        "task_id": smms["task_id"],
        "source_system": "SMMS",
        "department": "S&T",
        "asset_id": smms["asset_id"],
        "section_id": smms["section_id"],
        "maintenance_type": smms["fault_type"],
        "severity": smms["severity"],
        "reported_date": smms["reported_date"],
        "due_date": smms["due_date"],
        "maintenance_duration": smms["maintenance_duration"],
        "status": smms["status"]
    })


def transform_tdms():
    """Transform TDMS data into the common maintenance format."""

    tdms = pd.read_csv(TDMS_FILE)

    return pd.DataFrame({
        "task_id": tdms["task_id"],
        "source_system": "TDMS",
        "department": "TRD",
        "asset_id": tdms["asset_id"],
        "section_id": tdms["section_id"],
        "maintenance_type": tdms["fault_type"],
        "severity": tdms["severity"],
        "reported_date": tdms["reported_date"],
        "due_date": tdms["due_date"],
        "maintenance_duration": tdms["maintenance_duration"],
        "status": tdms["status"]
    })


def transform_coa():
    """Transform COA train movement data."""

    coa = pd.read_csv(COA_FILE)

    return pd.DataFrame({
        "train_id": coa["train_id"],
        "train_type": coa["train_type"],
        "section_id": coa["section_id"],
        "arrival_time": coa["arrival_time"],
        "departure_time": coa["departure_time"],
        "train_priority": coa["train_priority"],
        "date": coa["date"]
    })


def transform_bdms():
    """Transform BDMS block request data."""

    bdms = pd.read_csv(BDMS_FILE)

    return pd.DataFrame({
        "block_request_id": bdms["block_request_id"],
        "task_id": bdms["task_id"],
        "department": bdms["department"],
        "section_id": bdms["section_id"],
        "requested_date": bdms["requested_date"],
        "requested_start": bdms["requested_start"],
        "requested_end": bdms["requested_end"],
        "duration": bdms["duration"],
        "reason": bdms["reason"]
    })


def main():

    # Transform maintenance systems
    tms_data = transform_tms()
    smms_data = transform_smms()
    tdms_data = transform_tdms()

    # Combine maintenance data
    maintenance_data = pd.concat(
        [tms_data, smms_data, tdms_data],
        ignore_index=True
    )

    # Save maintenance data
    maintenance_data.to_csv(
        MAINTENANCE_OUTPUT,
        index=False
    )

    # Transform COA
    train_data = transform_coa()

    # Save train movement data
    train_data.to_csv(
        TRAIN_OUTPUT,
        index=False
    )

    # Transform BDMS
    block_request_data = transform_bdms()

    # Save block request data
    block_request_data.to_csv(
        BLOCK_REQUEST_OUTPUT,
        index=False
    )

    print("===================================")
    print("ETL TRANSFORMATION COMPLETED")
    print("===================================")

    print(f"TMS records: {len(tms_data)}")
    print(f"SMMS records: {len(smms_data)}")
    print(f"TDMS records: {len(tdms_data)}")

    print(f"Total maintenance records: {len(maintenance_data)}")

    print(f"COA train records: {len(train_data)}")

    print(f"BDMS block request records: {len(block_request_data)}")

    print("-----------------------------------")
    print(f"Maintenance output: {MAINTENANCE_OUTPUT}")
    print(f"Train output: {TRAIN_OUTPUT}")
    print(f"Block request output: {BLOCK_REQUEST_OUTPUT}")
    print("===================================")


if __name__ == "__main__":
    main()