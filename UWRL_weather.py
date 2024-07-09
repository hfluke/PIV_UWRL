import pandas as pd
from datetime import timedelta


def UWRL_weather(v):
    
    # local time
    rounded_minute = 60 * round(int(v['dt'].minute) / 60)
    offset = rounded_minute - v['dt'].minute
    offset_time = (v['dt'] + timedelta(minutes=offset)).replace(second=0)
    date = offset_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    df = pd.read_csv('Weather/Weather.csv')
    df = df[['datetime', 'windspeed', 'winddir', 'visibility', 'cloudcover', 'solarradiation', 'uvindex', 'conditions']]

    if date in df.datetime.values:
        df = df[df.datetime == date]

        v['ds']['visibility'] = df.visibility.values[0]
        v['ds']['cloudcover'] = df.cloudcover.values[0]
        v['ds']['solarradiation'] = df.solarradiation.values[0]
        v['ds']['uvindex'] = df.uvindex.values[0]
        v['ds']['conditions'] = df.conditions.values[0]
        
    return v
