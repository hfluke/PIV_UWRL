import ephem
import numpy as np
import xarray as xr


def UWRL_sun(v):

    # ephem expects UTC time
    observer = ephem.Observer()
    observer.lat, observer.lon = '41.739034', '-111.795742'
    observer.date = f"{v['dt_utc'].year}/{v['dt_utc'].month}/{v['dt_utc'].day} {v['dt_utc'].hour}:{v['dt_utc'].minute}:{v['dt_utc'].second}"

    sun = ephem.Sun(observer)

    sun_altitude = xr.DataArray(
        data=sun.alt * np.ones_like(v['ds']['time']),
        dims=['time'],
        coords={'time': v['ds']['time']}
    )
    v['ds']['sun_altitude'] = sun_altitude

    sun_azimuth = xr.DataArray(
        data=sun.az * np.ones_like(v['ds']['time']),
        dims=['time'],
        coords={'time': v['ds']['time']}
    )
    v['ds']['sun_azimuth'] = sun_azimuth

    return v
