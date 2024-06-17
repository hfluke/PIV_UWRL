import glob
import xarray as xr
import pandas as pd


def one():
    vector_files = [f for f in glob.glob('nc_new/*.nc')]

    n = 0
    dfs = []
    while vector_files != []:
        n += 1; print(n)
        dfs.append(xr.open_dataset(vector_files.pop()).to_dataframe().reset_index()[[
            'datetime', 'y', 'x', 'v_x', 'v_y', 'v_len', 's2n', 'corr',
            'sun_altitude', 'sun_azimuth', 'spacial_location', 'LRO_discharge',
            'LRO_discharge_site', 'vegetation', 'visibility','cloudcover',
            'solarradiation', 'uvindex', 'conditions'
        ]])
    pd.concat(dfs).to_csv(f'UWRL_river_velocimetry_dataset.csv', index=False)


def two():
    files = ['January_weather.csv', 'February_weather.csv', 'March_weather.csv', 'April_weather.csv', 'May_weather.csv']
    dfs = []
    for file in files:
        dfs.append(pd.read_csv(file))
    pd.concat(dfs).to_csv(f'Weather.csv', index=False)


one()
# two()
