import pandas as pd

def load_abdata():
    df = pd.read_csv("data/ABDATA.csv")
    return df


