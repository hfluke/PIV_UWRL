import numpy as np
import pandas as pd
import xarray as xr
from datetime import timedelta


def UWRL_discharge(v):
  
    rounded_minute = 15 * round(int(v['dt_utc'].minute) / 15)
    offset = rounded_minute - v['dt_utc'].minute
    v['dt_utc'] = (v['dt_utc'] + timedelta(minutes=offset)).replace(second=0)
    date = v['dt_utc'].strftime('%Y-%m-%d %H:%M:%S')
    
    df = pd.read_csv('LR_WaterLab_AA_SourceID_1_QC_0_Year_2024.csv')
    df = df[['DateTimeUTC', 'Discharge_cms']]
    df = df[df.Discharge_cms >= 0]

    if date in df.DateTimeUTC.values:
        discharge_cms = df[df.DateTimeUTC == date].Discharge_cms.values[0]
    else:
        discharge_cms = np.nan

    discharge = xr.DataArray(
        data=discharge_cms * np.ones_like(v['ds']['time']),
        dims=['time'],
        coords={'time': v['ds']['time']}
    )
    v['ds']['discharge'] = discharge

    return v
