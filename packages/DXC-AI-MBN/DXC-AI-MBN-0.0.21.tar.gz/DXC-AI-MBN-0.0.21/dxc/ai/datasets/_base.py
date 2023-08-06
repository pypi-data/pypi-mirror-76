# import pandas as pd

# def load_abdata():
#     df = pd.read_csv("data/ABDATA.csv")
#     return df

from os.path import dirname, join
import csv

def load_data(module_path, data_file_name):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    with open(join(module_path, 'data', data_file_name)) as csv_file:
        data_file = csv.reader(csv_file)
        for i, ir in enumerate(data_file):
            if i == 0:
                header = ir
                df = pd.DataFrame(columns = header)
            else:
                df1 = pd.DataFrame([ir],columns = header)
            df = df.append(df1, ignore_index = True)
    return df


def load_abdata():
    module_path = dirname(__file__)
    df = load_data(module_path, 'ABDATA.csv')
    return df
    





