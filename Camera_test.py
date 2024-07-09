import pyorc
import xarray as xr
import pandas as pd
from matplotlib import patches
import matplotlib.pyplot as plt
import glob
import os
from matplotlib.colors import Normalize
import numpy as np


def main():

    months = [
        'January', 
        'February', 
        # 'March', 
        # 'April', 
        # 'May', 
        # 'June'
    ]

    videos = []
    for month in months:
        for video in sorted(glob.glob("*.mp4", root_dir=f"{month}/")):
            videos.append({
                'video': f'{month}/{video}',
                'vec': f'{month}/results/{video.split('.')[0]}_velocimetry_results.nc',
                'name': video.split('.')[0]
            })

    i = 0
    l = len(videos)
    for v in videos:

        os.system('clear')
        i += 1; print(f'video {i} of {l}. {i/l:.2%} complete\n') 

        rock_box(v)

        # break


def control_points(v):
    video_file = v['video']
    video_name = v['name']
    video = pyorc.api.video.Video(video_file, start_frame=0, end_frame=125)
    frame = video.get_frame(0, method="rgb")

    gcps = dict(
        src=[
            [2434, 1397], #Blue
            [2304, 1001], #Green
            [525, 879],   #Orange
            [77, 1779]    #Purple
        ]
    )

    plt.plot(1613, 40, "o", color="#FF0000", markersize=1)
    plt.imshow(frame)
    plt.plot(*zip(*gcps["src"]), "o", color="#FF0000", markersize=3, markeredgewidth=0.4, markeredgecolor="#FFFFFF")
    plt.savefig(f"Camera_test/Control/{video_name}_control.png", bbox_inches="tight", dpi=600)
    plt.clf()


def rock_box(v):
    video_file = v['video']
    vector_file = v['vec']
    video_name = v['name']

    ds = xr.open_dataset(vector_file)

    ds.velocimetry.mask.corr(inplace=True)
    ds.velocimetry.mask.minmax(inplace=True)
    ds.velocimetry.mask.rolling(inplace=True)
    ds.velocimetry.mask.outliers(inplace=True)
    ds.velocimetry.mask.variance(inplace=True)
    ds.velocimetry.mask.angle(angle_tolerance=0.5*np.pi)
    ds.velocimetry.mask.count(inplace=True)
    ds.velocimetry.mask.window_mean(wdw=2, inplace=True, tolerance=0.5, reduce_time=True)

    video = pyorc.Video(video_file, start_frame=0, end_frame=125)
    video.camera_config = ds.velocimetry.camera_config

    ds = ds.mean(dim="time", keep_attrs=True)

    ds.velocimetry.plot(
        ax=video.get_frames(method="rgb")[0].frames.plot(mode="camera").axes,
        mode="camera",
        alpha=0.4,
        cmap="rainbow",
        scale=200,
        width=0.0015,
        norm=Normalize(vmin=0., vmax=1.0, clip=False),
        add_colorbar=True
    )

    t, r, b, l = 0, 2350, 0, 500
    upstream, downstream = 800, 1200

    x = [l, r, r, l, l]
    y = [downstream, downstream, upstream, upstream, downstream]
    plt.plot(x, y, color="black")

    plt.savefig(f"Camera_test/Rock_Box/{video_name}_rock_box.png", bbox_inches="tight", dpi=600)
    # plt.savefig(f"Camera_test/test.png", bbox_inches="tight", dpi=600)
    plt.close()

    ds.close()

main()
