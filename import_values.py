import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
import os.path
import sys


# local_path = 'Tables/PNA.xlsx'
local_path = 'DUMMY.xlsx'
cloud_path = "/Users/davidbaxter//Dropbox (MIT)/2.705/PNA.xlsx"

def get_PNA_weights():
    try:
        df = pd.read_excel(local_path, sheet_name='Sheet1')
        print ("Data file in local path!!!")
    except:
        try:
            df = pd.read_excel(cloud_path, sheet_name='Sheet1')
            print ("Data file in cloud path!!!")
        except:
            # print(sys.stderr, "does not exist")
            print ("Data file does not exist at any path given")
            print(f'Local Path: {local_path}')
            print(f'Cloud Path: {cloud_path}')
            sys.exit(1)

    df.set_index("Component", inplace=True)
    weight_df = df[['Total Weight']].replace(0, np.NaN).dropna()
    weight_df = weight_df.astype(float)
    return weight_df.dropna().sum()


    # print(weight_df)
    # print('Sum: ', weight_df.dropna().sum())
    # print(type(weight_df['Total Weight']))
    # weight_df = weight_df.astype(float)

    # weight_df.plot.bar()
    # plt.xlabel('xlabel')
    # plt.ylabel('ylabel')

    # # ax.set_xlabel("x label")
    # # ax.set_xlabel("y label")
    # plt.show()


def get_PNA_loads():
    try:
        df = pd.read_excel(local_path, sheet_name='Sheet1')
    except:
        try:
            df = pd.read_excel(cloud_path, sheet_name='Sheet1')
        except:
            # print(sys.stderr, "does not exist")
            print ("Data file does not exist at any path given")
            print(f'Local Path: {local_path}')
            print(f'Cloud Path: {cloud_path}')
            sys.exit(1)

    df.set_index("Component", inplace=True)
    load_df = df[['Avg Power']].replace(0, np.NaN).dropna()
    load_df = load_df.astype(float)
    return load_df.dropna().sum()
