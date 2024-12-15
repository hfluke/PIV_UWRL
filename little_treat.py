import cv2
import numpy as np
from glob import glob

import pyorc
import xarray as xr
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt


def main():

    frames = []
    for image in sorted(glob("*.png", root_dir=f"Treat/")):
        frames.append(f"Treat/{image}")
    path_out = f"Treat.mp4"

    cap = cv2.imread(frames[0])

    print(len(cap), len(cap[0]))

    frame_height = len(cap)
    frame_width = len(cap[0])

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path_out, fourcc, 20, (frame_width, frame_height))

    for frame in frames:
        out.write(cv2.imread(frame))

    out.release()
    cv2.destroyAllWindows()


def filter():
    ds = xr.open_dataset("Velocimetry_Results/video_capture_2024-09-12_12-00-04_velocimetry_results.nc")
    video = pyorc.Video("Videos/video_capture_2024-09-12_12-00-04.mp4", start_frame=0, end_frame=125)
    video.camera_config = ds.velocimetry.camera_config

    t = ds.time.values
    for i in range(len(t)):
        if i > 124:
            ds_time = ds.where(ds.time == t[i], drop=True)
            ds_time = ds_time.mean(dim="time", keep_attrs=True)

            ds_time.velocimetry.plot(
                ax=video.get_frames(method="rgb")[i].frames.plot(mode="camera").axes,
                mode="camera",
                alpha=1.0,
                cmap="rainbow",
                scale=200,
                width=0.0015,
                norm=Normalize(vmin=0., vmax=1.0, clip=False),
                add_colorbar=True
            )
            plt.savefig(f"Treat/frame{i}.png")
            plt.close()

main()
# filter()