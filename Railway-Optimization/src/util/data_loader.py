import pandas as pd


def load_tasks(path):
    return pd.read_csv(path)


def load_blocks(path):
    return pd.read_csv(path)


def load_trains(path):
    return pd.read_csv(path)


def load_goods_forecast(path):
    return pd.read_csv(path)

def load_optimization_handoff(path):
    return pd.read_csv(path)