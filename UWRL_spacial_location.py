import numpy as np


def UWRL_spacial_location(v):

    spac_loc = spacial_location_wrapper(v['ds'].y.values)
    spac_loc = np.broadcast_to(spac_loc, (len(v['ds'].time), len(v['ds'].y)))

    v['ds']['spacial_location'] = (['time', 'y'], spac_loc)

    return v


def spacial_location_wrapper(y_vals):
    m = min(y_vals)
    subdiv = ( max(y_vals) - m) / 5

    spac_loc = []
    for y in y_vals:
        spac_loc.append(spacial_location(y, m, subdiv))
    return spac_loc


def spacial_location(y, m, subdiv):
    if y < m + subdiv:
        return 0
    elif (y >= m + subdiv) and (y < m + 2 * subdiv):
        return 1
    elif (y >= m + subdiv) and (y < m + 3 * subdiv):
        return 2
    elif (y >= m + subdiv) and (y < m + 4 * subdiv):
        return 3
    else:
        return 4
