import numpy as np
import pandas as pd
from datetime import timedelta


def UWRL_LRO(v):
  
    rounded_minute = 15 * round(int(v['dt_utc'].minute) / 15)
    offset = rounded_minute - v['dt_utc'].minute
    v['dt_utc'] = (v['dt_utc'] + timedelta(minutes=offset)).replace(second=0)
    date = v['dt_utc'].strftime('%Y-%m-%d %H:%M:%S')
    
    df_lab = pd.read_csv('LR_WaterLab_AA_SourceID_1_QC_0_Year_2024.csv')
    df_lab = df_lab[['DateTimeUTC', 'Discharge_cms']]
    df_lab = df_lab[df_lab.Discharge_cms >= 0]

    df_main = pd.read_csv('LR_MainStreet_BA_SourceID_1_QC_0_Year_2024.csv')
    df_main = df_main[['DateTimeUTC', 'Discharge_cms']]

    if date in df_lab.DateTimeUTC.values:
        discharge_cms = df_lab[df_lab.DateTimeUTC == date].Discharge_cms.values[0]
        site = 'WaterLab'
    elif date in df_main.DateTimeUTC.values:
        discharge_cms = df_main[df_main.DateTimeUTC == date].Discharge_cms.values[0]
        site = 'MainStreet'
    else:
        discharge_cms = np.nan
        site = np.nan

    v['ds']['LRO_discharge'] = discharge_cms
    v['ds']['LRO_site'] = site

    return v
