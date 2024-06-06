import copy
import ephem
import pyorc
import numpy as np
import xarray as xr

MONTHS = ['January', 'February', 'March', 'April', 'May']

def UWRL_sun(video_file):

    month = MONTHS[int(video_file.split('-')[1]) - 1]
    name = video_file.split(".")[0]
    video_file = f"{month}/{video_file}"
    vector_file = f"{month}/results/{name}_velocimetry_results.nc"

    ds = xr.open_dataset(vector_file)

    video = pyorc.Video(video_file, start_frame=0, end_frame=125)
    video.camera_config = ds.velocimetry.camera_config

    date = name.split('_')[2]
    time = name.split('_')[3].split('.')[0]
    year, month, day = date.split('-')
    hour, minute, second = time.split('-')
    hour = (int(hour) + 7) % 24

    observer = ephem.Observer()
    observer.lat, observer.lon = '41.739203', '-111.795694'
    observer.date = f'{year}/{month}/{day} {hour}:{minute}:{second}'

    sun = ephem.Sun(observer)

    sun_altitude = xr.DataArray(
        data=sun.alt * np.ones_like(ds['time']),
        dims=['time'],
        coords={'time': ds['time']}
    )
    ds['sun_altitude'] = sun_altitude

    sun_azimuth = xr.DataArray(
        data=sun.az * np.ones_like(ds['time']),
        dims=['time'],
        coords={'time': ds['time']}
    )
    ds['sun_azimuth'] = sun_azimuth

    save_file = f"temp/{name}_velocimetry_results.nc"
    save_file = str(save_file)

    ds.to_netcdf(save_file)
    ds.close()

