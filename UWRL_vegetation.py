import numpy as np


def UWRL_vegetation(v):

    if v['dt'].month in [1, 2, 3, 4]:
        veg = 'none'
    elif v['dt'].month == 5:
        veg = 'light'
    else:
        veg = np.nan

    v['ds']['vegetation'] = veg

    return v
