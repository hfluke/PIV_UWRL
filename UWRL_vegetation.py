import numpy as np


def UWRL_vegetation(v):

    if v['dt'].month in [1, 2, 3, 4]:
        veg = 'none'
    elif v['dt'].month in [5, 6]:
        veg = 'light'
    elif v['dt'].month in [7, 8]:
        veg = 'dense'
    else:
        veg = np.nan

    v['ds']['vegetation'] = veg

    return v
