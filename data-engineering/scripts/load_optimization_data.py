import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "processed"
    / "optimization_handoff.csv"
)


def load_optimization_data():

    df = pd.read_csv(INPUT_FILE)

    print("Optimization handoff data loaded.")
    print("-----------------------------------")
    print(f"Tasks: {len(df)}")
    print(f"Features: {len(df.columns)}")
    print("-----------------------------------")

    return df


if __name__ == "__main__":

    data = load_optimization_data()

    print()
    print("Preview:")
    print(data.head())