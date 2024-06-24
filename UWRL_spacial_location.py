import numpy as np


def UWRL_spacial_location(v):

    # spac_loc_3 = spacial_location_wrapper(v['ds'].y.values, 3)
    # spac_loc_3 = np.broadcast_to(spac_loc_3, (len(v['ds'].y)))

    # v['ds']['spacial_location_3'] = (['y'], spac_loc_3)

    spac_loc_5 = spacial_location_wrapper(v['ds'].y.values, 5)
    spac_loc_5 = np.broadcast_to(spac_loc_5, (len(v['ds'].y)))

    v['ds']['spacial_location'] = (['y'], spac_loc_5)

    return v


def spacial_location_wrapper(y_vals, n):
    m = min(y_vals)
    subdiv = ( max(y_vals) - m) / n

    spac_loc = []
    # if n == 3:
    #     for y in y_vals:
    #         spac_loc.append(spacial_location_3(y, m, subdiv))
    if n == 5:
        for y in y_vals:
            spac_loc.append(spacial_location_5(y, m, subdiv))
    else:
        for y in y_vals:
            spac_loc.append(np.nan)
    
    return spac_loc


def spacial_location_3(y, m, subdiv):
    if y < m + subdiv:
        return 0
    elif (y >= m + subdiv) and (y < m + 2 * subdiv):
        return 1
    else:
        return 2


def spacial_location_5(y, m, subdiv):
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
