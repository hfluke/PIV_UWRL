import copy
import pyorc
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


def filter(file):

    month = MONTHS[int(file.split('-')[1]) - 1]
    # video_file = f"{month}/videos/{file}.mp4"
    vector_file = f"{month}/results/{file}_velocimetry_results.nc"

    ds = xr.open_dataset(vector_file)

    ds.velocimetry.mask.corr(inplace=True)
    ds.velocimetry.mask.minmax(inplace=True)
    ds.velocimetry.mask.rolling(inplace=True)
    ds.velocimetry.mask.outliers(inplace=True)
    ds.velocimetry.mask.variance(inplace=True)
    ds.velocimetry.mask.angle(angle_tolerance=0.5*np.pi)
    ds.velocimetry.mask.count(inplace=True)
    ds.velocimetry.mask.window_mean(wdw=2, inplace=True, tolerance=0.5, reduce_time=True)

    # video = pyorc.Video(video_file, start_frame=0, end_frame=125)
    # video.camera_config = ds.velocimetry.camera_config
    
    # ds = ds.mean(dim="time", keep_attrs=True)

    # ds.velocimetry.plot(
    #     ax=video.get_frames(method="rgb")[0].frames.plot(mode="camera").axes,
    #     mode="camera",
    #     alpha=0.4,
    #     cmap="rainbow",
    #     scale=200,
    #     width=0.0015,
    #     norm=Normalize(vmin=0., vmax=1.0, clip=False),
    #     add_colorbar=True
    # )
    # plt.title(f"{file} velocimetry results")
    # plt.savefig(f"{month}/results/{file}_velocimetry_results.png", bbox_inches="tight", dpi=600)
    # plt.close() # thank you Haley

    ds.to_netcdf(f"Mask/{file}_velocimetry_results_masked.nc")
    ds.close()


files = []
with open('filter_explore.txt') as f:
    for line in f:
        files.append(line.strip())

for file in files:
    print(file)
    filter(file)
    print()
