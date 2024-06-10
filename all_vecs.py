import glob
import xarray as xr
import pandas as pd

vector_files = [f for f in glob.glob('nc_new/*.nc')]
df = xr.open_dataset(vector_files.pop()).to_dataframe().reset_index()
i=0
for f in vector_files:
    i+=1; print(i)
    temp = xr.open_dataset(f).to_dataframe().reset_index()
    df = pd.concat([df, temp])
df.to_csv('all_vecs.csv', index=False)
