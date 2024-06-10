import ephem


def UWRL_sun(v):

    # ephem expects UTC time
    observer = ephem.Observer()
    observer.lat, observer.lon = '41.739034', '-111.795742'
    observer.date = f"{v['dt_utc'].year}/{v['dt_utc'].month}/{v['dt_utc'].day} {v['dt_utc'].hour}:{v['dt_utc'].minute}:{v['dt_utc'].second}"

    sun = ephem.Sun(observer)

    v['ds']['sun_altitude'] = sun.alt
    v['ds']['sun_azimuth'] = sun.az

    return v
