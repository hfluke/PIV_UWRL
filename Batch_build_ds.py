import glob
import numpy as np
import xarray as xr
from datetime import datetime, timedelta
from UWRL_sun import UWRL_sun
from UWRL_spacial_location import UWRL_spacial_location
from UWRL_LRO import UWRL_LRO
from UWRL_weather import UWRL_weather
from UWRL_vegetation import UWRL_vegetation


def main():

    vector_files = [f for f in glob.glob('nc_old/*.nc')]

    for vec_file in vector_files:
        
        UWRL_dict = make_UWRL_dict(vec_file)
        UWRL_dict['ds'] = xr.open_dataset(UWRL_dict['vector_file'])

        UWRL_dict['ds'] = UWRL_dict['ds'].mean(dim="time", keep_attrs=True)
        UWRL_dict['ds']['datetime'] = UWRL_dict['dt']
        UWRL_dict['ds']['v_len'] = np.sqrt(UWRL_dict['ds']['v_x']**2 + UWRL_dict['ds']['v_y']**2)

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


main()
