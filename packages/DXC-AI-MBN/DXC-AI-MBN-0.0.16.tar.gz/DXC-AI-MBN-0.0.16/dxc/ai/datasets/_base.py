import pandas as pd

def load_abdata():
    df = pd.read_csv("dxc/ai/datasets/data/ABDATA.csv")
    return df


