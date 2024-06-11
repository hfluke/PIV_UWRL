import glob
import xarray as xr
import pandas as pd

# vector_files = [f for f in glob.glob('nc_new/*.nc')]

# n = 0
# while vector_files != []:
#     print(n)
#     dfs = []
#     for i in range(8):
#         dfs.append(xr.open_dataset(vector_files.pop()).to_dataframe().reset_index())
#     pd.concat(dfs).to_csv(f'temp2/temp_{n}.csv', index=False)
#     n += 1

# vector_files = [f for f in glob.glob('nc_new/*.nc')]

# n = 0
# while vector_files != []:
#     print(n)
#     dfs = []
#     ds = xr.open_dataset(vector_files.pop())
#     ds = ds.mean(dim="time", keep_attrs=True)
#     dfs.append(ds.to_dataframe().reset_index())
# pd.concat(dfs).to_csv(f'temp2/temp_{n}.csv', index=False)


# vector_files = [f for f in glob.glob('nc_new/*.nc')]

# n = 0
# dfs = []
# while vector_files != []:
#     n += 1; print(n)
#     dfs.append(xr.open_dataset(vector_files.pop()).to_dataframe().reset_index()[[
#         'y', 'x', 'v_x', 'v_y', 's2n', 'corr', 'sun_altitude', 'sun_azimuth', 'spacial_location',
#         'LRO_discharge', 'LRO_site', 'vegetation', 'windspeed', 'winddir', 'visibility',
#         'cloudcover', 'solarradiation', 'uvindex','conditions', 'name','month'
#     ]])
# pd.concat(dfs).to_csv(f'temp2/temp_2.csv', index=False)


vector_files = [f for f in glob.glob('nc_new/*.nc')]

n = 0
dfs = []
while vector_files != []:
    n += 1; print(n)
    dfs.append(xr.open_dataset(vector_files.pop()).to_dataframe().reset_index()[[
        'y', 'x', 'v_x', 'v_y', 's2n', 'corr', 'sun_altitude', 'sun_azimuth', 'spacial_location',
        'LRO_discharge', 'LRO_discharge_site', 'BGA', 'Chlorophyll', 'ODO', 'fDOM', 'pH', 
        'vegetation', 'windspeed', 'winddir', 'visibility','cloudcover', 'solarradiation',
        'uvindex', 'conditions', 'name', 'month'
    ]])
pd.concat(dfs).to_csv(f'temp2/temp_1.csv', index=False)
