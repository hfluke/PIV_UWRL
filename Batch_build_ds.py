import glob
import xarray as xr
from UWRL_sun import UWRL_sun
from UWRL_spacial_location import UWRL_spacial_location


def main():

    vector_files = [f for f in glob.glob('nc_old/*.nc')]
    for vec_file in vector_files:

        UWRL_dict = make_UWRL_dict(vec_file)
        UWRL_dict['ds'] = xr.open_dataset(UWRL_dict['vector_file'])

        UWRL_dict = UWRL_sun(UWRL_dict)
        # UWRL_dict['ds'] = UWRL_spacial_location(UWRL_dict)
        # UWRL_dict['ds'] = UWRL_discharge(UWRL_dict)
        # UWRL_dict['ds'] = UWRL_weather(UWRL_dict)
        # UWRL_dict['ds'] = UWRL_vegatation(UWRL_dict)

        # UWRL_dict['ds'].to_netcdf(f"nc_new/{UWRL_dict['name']}_velocimetry_results.nc")

        print(UWRL_dict['ds'])

        UWRL_dict['ds'].close()

        break
        


def make_UWRL_dict(v):

    name = v.split('/')[-1].rsplit('_', maxsplit=2)[0]
    year, month, day = name.split('_')[2].split('-')
    hour, minute, second = name.split('_')[3].split('-')

    UWRL_dict = {
            'vector_file': v,
            'name': name,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'second': second,
        }
    
    return UWRL_dict


# def batch():
#     # UWRL_sun(video)
#     # UWRL_spacial_location(video)

#     return


main()
