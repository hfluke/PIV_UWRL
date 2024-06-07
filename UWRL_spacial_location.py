import numpy as np
import xarray as xr


def UWRL_spacial_location(video_file):
    name = video_file.split(".")[0]
    vector_file = f"temp/{name}_velocimetry_results.nc"
    vector_file2 = f"temp/{name}_velocimetry_results_1.nc"

    ds = xr.open_dataset(vector_file)

    spac_loc = spacial_location_wrapper(ds.y.values)
    spac_loc = np.broadcast_to(spac_loc, (len(ds.time), len(ds.y)))

    ds['spacial_location'] = (['time', 'y'], spac_loc)

    ds.to_netcdf(vector_file2)
    ds.close()


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
