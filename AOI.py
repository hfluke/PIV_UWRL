import pandas as pd
import xarray as xr
import glob
# from Dataset.Batch_build_ds import main

MONTHS = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    # 'August',
    # 'September',
    # 'October',
    # 'November',
    # 'December'
]

files_new, files_original = [], []
for month in MONTHS:
    for file in sorted(glob.glob("*velocimetry_velocimetry_results.nc*", root_dir="AOI/new/")):
        files_new.append(f"AOI/new/{file}")
    for file in sorted(glob.glob("*velocimetry_results.nc*", root_dir="AOI/new/")):
        file not in files_new and files_original.append(f"AOI/new/{file}")

dfs = []
for file in files_new:
    # df = xr.open_dataset(file).mean(dim="time", keep_attrs=True).to_dataframe().reset_index()
    df = xr.open_dataset(file).to_dataframe().reset_index()
    df['AOI'] = ['new' for _ in range(len(df))]
    dfs.append(df)
for file in files_original:
    # df = xr.open_dataset(file).mean(dim="time", keep_attrs=True).to_dataframe().reset_index()
    df = xr.open_dataset(file).to_dataframe().reset_index()
    df['AOI'] = ['original' for _ in range(len(df))]
    dfs.append(df)

pd.concat(dfs).to_csv(f'AOI_bounded.csv', index=False)
