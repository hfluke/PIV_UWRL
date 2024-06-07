import ephem
import numpy as np
import xarray as xr


def UWRL_sun(v):

    observer = ephem.Observer()
    observer.lat, observer.lon = '41.739034', '-111.795742'
    observer.date = f"{v['year']}/{v['month']}/{v['day']} {v['hour']}:{v['minute']}:{v['second']}"

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
