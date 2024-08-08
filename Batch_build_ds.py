import os
import glob
import numpy as np
import pandas as pd
import xarray as xr
from datetime import datetime, timedelta
from Dataset.UWRL_sun import UWRL_sun
from Dataset.UWRL_spacial_location import UWRL_spacial_location
from Dataset.UWRL_LRO import UWRL_LRO
from Dataset.UWRL_vegetation import UWRL_vegetation
from Dataset.UWRL_weather import UWRL_weather


MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


def main():

    build_sets()
    build_csv()


def build_sets():

    vector_files = []
    for month in MONTHS:
        for file in sorted(glob.glob("*.nc", root_dir=f"{month}/results/")):
            vector_files.append(f"{month}/results/{file}")

    i = 0
    length = len(vector_files)
    for vec_file in vector_files:

        i += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f" Building individual datasets: {i/length:.2%} complete")

        
        UWRL_dict = make_UWRL_dict(vec_file)
        UWRL_dict['ds'] = xr.open_dataset(UWRL_dict['vector_file'])

        UWRL_dict['ds'] = UWRL_dict['ds'].mean(dim="time", keep_attrs=True)
        UWRL_dict['ds']['datetime'] = UWRL_dict['dt']
        UWRL_dict['ds']['velocity'] = np.sqrt(UWRL_dict['ds']['v_x']**2 + UWRL_dict['ds']['v_y']**2)

        UWRL_dict = UWRL_sun(UWRL_dict)
        UWRL_dict = UWRL_spacial_location(UWRL_dict)
        UWRL_dict = UWRL_LRO(UWRL_dict)
        UWRL_dict = UWRL_vegetation(UWRL_dict)
        UWRL_dict = UWRL_weather(UWRL_dict)

        UWRL_dict['ds'].to_netcdf(f"nc_new/{UWRL_dict['name']}_velocimetry_results.nc")
        UWRL_dict['ds'].close()

        # print(UWRL_dict['ds'])
        # UWRL_dict['ds'].close()
        # break
        

def make_UWRL_dict(v):

    name = v.split('/')[-1].rsplit('_', maxsplit=2)[0]
    year, month, day = name.split('_')[2].split('-')
    hour, minute, second = name.split('_')[3].split('-')

    dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    UWRL_dict = {
        'vector_file': v,
        'name': name,
        'dt': dt, # UTC-7
        'dt_utc': dt + timedelta(hours=7)
    }
    
    return UWRL_dict


def build_csv():
    vector_files = [f for f in glob.glob('nc_new/*.nc')]

    i = 0
    length = len(vector_files)
    dfs = []
    while vector_files != []:
        
        i += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f" Building .csv file: {i/length:.2%} complete")
        
        df = xr.open_dataset(vector_files.pop()).to_dataframe().reset_index()[[
            'datetime', 'x', 'y', 'v_x', 'v_y', 'velocity', 's2n', 'corr',
            'sun_altitude', 'sun_azimuth', 'spacial_location',
            'LRO_discharge', 'LRO_discharge_site', 'turbidity', 'vegetation', 'visibility',
            'cloudcover', 'solarradiation', 'uvindex', 'conditions'
        ]]
        df['angle'] = np.arctan2(df['v_y'], df['v_x'])
        df.datetime = pd.to_datetime(df.datetime)
        
        dfs.append(df)
    pd.concat(dfs).to_csv(f'trash2_UWRL_river_velocimetry_dataset.csv', index=False)


main()
