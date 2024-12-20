import cv2
import glob
import pyorc
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from dask.diagnostics import ProgressBar

from Radar import Radar
from Transform import transform


def PyCam_Implementation(video_file):
    
    titlestr = "_velocimetry_results"

    camera = "temp.json"
    name = video_file.rsplit(".", maxsplit=1)[0]
    vector_file = f"Velocimetry_Results/{name}{titlestr}.nc"
    video_file = f"Videos/December/{video_file}"
    
    start_frame = 0
    end_frame = 120

    # cap = cv2.VideoCapture(video_file)
    # end_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
    # print("fps:", cap.get(cv2.CAP_PROP_FPS))
    # cap.release()

    video = pyorc.api.video.Video(
        video_file, 
        start_frame=start_frame, 
        end_frame=end_frame
    )

    gcps = dict(
        src=[
            [2452, 1358], # 3 UL Blue
            [2308, 1051], # 4 DL Green
            [666, 879],   # 2 DR Orange
            [91, 1786]    # 1 UR Purple
        ]
    )

    # TODO: pass in points from Ausust survey, rotation angle
    #       return new points

    gcps["dst"] = transform(
        anchor=[9.416, 2.321],
        points=[
            [4.291, 5.064],   # P3
            [2.230, 7.569],   # P4
            [10.259, 16.125], # P2
            [12.257, 5.852]   # P1
        ],
        theta=-25
    )

    gcps["z_0"] = 0.00
    height, width = video.get_frame(0).shape[0:2]

    cam_config = pyorc.CameraConfig(height=height, width=width, gcps=gcps)

    corners = [
        [2559, 1919],
        [1752, 680],
        [940, 680],
        [200, 1919]
    ]
    cam_config.set_bbox_from_corners(corners)
    cam_config.resolution = 0.01
    cam_config.window_size = 25
    
    cam_config.to_file(camera)


    stabilize = [
        [2559, 1919],
        [1752, 680],
        [940, 680],
        [200, 1919]
    ]

    # TODO: need to reopen cam_config file?
    cam_config = pyorc.load_camera_config(camera)

    video = pyorc.Video(
        video_file,
        camera_config=cam_config,
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

    # radar = Radar()

    ds = xr.open_dataset(vector_file)

    ds.velocimetry.mask.corr(inplace=True)
    ds.velocimetry.mask.minmax(inplace=True)
    ds.velocimetry.mask.rolling(inplace=True)
    ds.velocimetry.mask.outliers(inplace=True)
    ds.velocimetry.mask.variance(inplace=True)
    ds.velocimetry.mask.angle(angle_tolerance=0.5*np.pi)
    ds.velocimetry.mask.count(inplace=True)
    ds.velocimetry.mask.window_mean(wdw=2, inplace=True, tolerance=0.5, reduce_time=True)
    
    # ds = ds.where(radar.filter_point(ds.xs, ds.ys), drop=True)
    # ds.to_dataframe().reset_index()[[
    #     'time', 'y', 'x', 'v_x', 'v_y', 's2n', 'corr', 'xp', 'yp', 'xs', 'ys'
    # ]].to_csv(f"Results/{name}{titlestr}_mask.csv")
    # ds.to_netcdf(f"Results/{name}{titlestr}.nc")
    
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
    plt.savefig(f"Results/December/{name}{titlestr}.png", bbox_inches="tight", dpi=600)
    plt.close()
    ds.close()


def batch():

    analyzed = []
    for image in sorted(glob.glob("*.png", root_dir=f"Results/")):
        analyzed.append(f"{image.rsplit('_', maxsplit=2)[0]}.mp4")

    videos = []
    for video in sorted(glob.glob("*.mp4", root_dir=f"Videos/December/")):
        video not in analyzed and videos.append(video)

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Video {i} of {vid_length}")
        print(f"{video}")

        PyCam_Implementation(video)

        print()


batch()
