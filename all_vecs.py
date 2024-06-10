import glob
import xarray as xr
import pandas as pd

vector_files = [f for f in glob.glob('nc_new/*.nc')]

n = 0
while vector_files != []:
    print(n)
    dfs = []
    for i in range(8):
        dfs.append(xr.open_dataset(vector_files.pop()).to_dataframe().reset_index())
    pd.concat(dfs).to_csv(f'temp2/temp_{n}.csv', index=False)
    n += 1

