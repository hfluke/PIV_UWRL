import cv2
import glob
import pyorc
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from dask.diagnostics import ProgressBar

from Radar import Radar


def PyCam_Implementation(video_file):
    
    titlestr = "_radar_results_1"

    camera = "NEW_cam-config-UWRL.json"
    name = video_file.rsplit(".", maxsplit=1)[0]
    video_file = f"Videos/{video_file}"
    vector_file = f"Velocimetry_Results/{name}_velocimetry_results.nc"
    # vector_file = f"Treat.nc"

    cap = cv2.VideoCapture(video_file)
    end_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 2
    start_frame = end_frame // 4 - 1
    end_frame = 2 * (end_frame // 4)
    cap.release()

    stabilize = [
        [2559, 1919],
        [1752, 680],
        [940, 680],
        [200, 1919]
    ]

    cam_config = pyorc.load_camera_config(camera)

    video = pyorc.Video(
        video_file,
        camera_config=cam_config,
        # start_frame=0,
        # end_frame=125,
        # end_frame=1171,
        start_frame=start_frame,
        end_frame=end_frame,
        stabilize=stabilize,
        h_a=0.
    )

    da = video.get_frames()
    da = da.frames.normalize()
    da = da.frames.project()
    piv = da.frames.get_piv().to_netcdf(vector_file, compute=False)
    with ProgressBar():
        piv.compute()

    # return

    radar = Radar()

    ds = xr.open_dataset(vector_file)

    ds.velocimetry.mask.corr(inplace=True)
    ds.velocimetry.mask.minmax(inplace=True)
    ds.velocimetry.mask.rolling(inplace=True)
    ds.velocimetry.mask.outliers(inplace=True)
    ds.velocimetry.mask.variance(inplace=True)
    ds.velocimetry.mask.angle(angle_tolerance=0.5*np.pi)
    ds.velocimetry.mask.count(inplace=True)
    ds.velocimetry.mask.window_mean(wdw=2, inplace=True, tolerance=0.5, reduce_time=True)
    
    ds = ds.where(radar.filter_point(ds.xs, ds.ys), drop=True)
    ds.to_dataframe().reset_index()[[
        'time', 'y', 'x', 'v_x', 'v_y', 's2n', 'corr', 'xp', 'yp', 'xs', 'ys'
    ]].to_csv(f"Results/{name}{titlestr}_mask.csv")
    ds.to_netcdf(f"Results/{name}{titlestr}_mask.nc")
    
    video = pyorc.Video(video_file, start_frame=0, end_frame=125)
    video.camera_config = ds.velocimetry.camera_config
    
    ds = ds.mean(dim="time", keep_attrs=True)

    ds.velocimetry.plot(
        ax=video.get_frames(method="rgb")[0].frames.plot(mode="camera").axes,
        mode="camera",
        alpha=1.0,
        cmap="rainbow",
        scale=200,
        width=0.0015,
        norm=Normalize(vmin=0., vmax=1.0, clip=False),
        add_colorbar=True
    )
    plt.savefig(f"Results/{name}{titlestr}_mask.png", bbox_inches="tight", dpi=600)
    plt.close()
    ds.close()


def batch():

    analyzed = []
    for image in sorted(glob.glob("*.png", root_dir=f"Results/")):
        analyzed.append(f"{image.rsplit('_', maxsplit=2)[0]}.mp4")

    videos = []
    for video in sorted(glob.glob("*.mp4", root_dir=f"Videos/")):
        video not in analyzed and videos.append(video)

    # videos = ["video_capture_2024-09-12_13-00-08.mp4"]
    # videos = ["Treat.mp4"]

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Video {i} of {vid_length}")
        print(f"{video}")

        PyCam_Implementation(video)

        print()


batch()
