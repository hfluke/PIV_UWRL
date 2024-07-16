import glob
import xarray as xr
import pandas as pd


def one():
    vector_files = [f for f in glob.glob('nc_new/*.nc')]
    # vector_files = [f for f in glob.glob('Mask/new/*.nc')]

    n = 0
    dfs = []
    while vector_files != []:
        n += 1; print(n)
        
        df = xr.open_dataset(vector_files.pop()).to_dataframe().reset_index()[[
            'datetime', 'x', 'y', 'v_x', 'v_y', 'v_len', 's2n', 'corr',
            'sun_altitude', 'sun_azimuth', 'spacial_location',
            'LRO_discharge', 'LRO_discharge_site', 'turbidity', 'vegetation', 'visibility',
            'cloudcover', 'solarradiation', 'uvindex', 'conditions'
        ]]
        df['v_pos'] =  [0 if pd.isna(x) else (-1 if x < 0 else 1) for x in df['v_x']]
        df.datetime = pd.to_datetime(df.datetime)
        
        dfs.append(df)
    # pd.concat(dfs).to_csv(f'UWRL_river_velocimetry_dataset.csv', index=False)
    pd.concat(dfs).to_csv(f'Mask/dataset_og.csv', index=False)


def two():
    files = ['January_weather.csv', 'February_weather.csv', 'March_weather.csv', 'April_weather.csv', 'May_weather.csv', 'June_weather.csv', 'July_weather.csv']
    dfs = []
    for file in files:
        dfs.append(pd.read_csv(f'Weather/{file}'))
    pd.concat(dfs).to_csv(f'Weather/Weather.csv', index=False)


one()
# two()
