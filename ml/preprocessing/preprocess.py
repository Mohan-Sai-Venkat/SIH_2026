import pandas as pd


def load_data(file_path):
    data = pd.read_csv(file_path)

    print("Dataset loaded successfully!")

    print("\nFirst 5 rows:")
    print(data.head())

    print("\nDataset shape:")
    print(data.shape)

    print("\nMissing values:")
    print(data.isnull().sum())

    return data


if __name__ == "__main__":

    file_path = "data/training_data.csv"

    data = load_data(file_path)