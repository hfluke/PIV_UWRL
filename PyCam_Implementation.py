import pyorc
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from dask.diagnostics import ProgressBar

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


def PyCam_Implementation(video_file):

    month = MONTHS[int(video_file.split('-')[1]) - 1]
    camera = "cam-config-UWRL.json"
    name = video_file.split(".")[0]
    video_file = f"{month}/videos/{video_file}"
    vector_file = f"{month}/results/{name}_velocimetry_results.nc"

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
        start_frame=0,
        end_frame=125,
        stabilize=stabilize,
        h_a=0. # water level must be of type float
    )

    da = video.get_frames()
    da = da.frames.normalize()
    da = da.frames.project()
    piv = da.frames.get_piv().to_netcdf(vector_file, compute=False)
    with ProgressBar():
        piv.compute()

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
    plt.title(f"{name} velocimetry results")
    plt.savefig(f"{month}/results/{name}_velocimetry_results.png", bbox_inches="tight", dpi=600)
    plt.close() # thank you Haley

    ds.close()

    # return cam_config.bbox.area


def PyCam_Implementation2(video_file):

    month = MONTHS[int(video_file.split('-')[1]) - 1]
    camera = "cam-config-UWRL.json"
    name = video_file.split(".")[0]
    video_file = f"{month}/videos/{video_file}"
    vector_file = f"{month}/results/{name}_velocimetry_results_bounded.nc"

    # this is to check if processing videos with smaller aoi area is faster/better results
    cam_config = pyorc.load_camera_config(camera)
    cam_config.set_bbox_from_corners(corners(month))

    # return

    stabilize = [
        [2559, 1919],
        [1752, 680],
        [940, 680],
        [200, 1919]
    ]
    
    video = pyorc.Video(
        video_file,
        camera_config=cam_config,
        start_frame=0,
        end_frame=125,
        stabilize=stabilize,
        h_a=0. # water level must be of type float
    )

    da = video.get_frames()
    da = da.frames.normalize()
    da = da.frames.project()
    piv = da.frames.get_piv().to_netcdf(vector_file, compute=False)
    with ProgressBar():
        piv.compute()

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
    plt.title(f"{name} velocimetry results")
    plt.savefig(f"{month}/results/{name}_velocimetry_results_bounded.png", bbox_inches="tight", dpi=600)
    plt.close() # thank you Haley

    ds.close()

    return cam_config.bbox.area


def corners(month):
    if month in ['January', 'February', 'March']:
        corners = [
            [2375, 1100],
            [1752, 680],
            [940, 680],
            [475, 1100]
        ]
    elif month == 'April':
        corners = [
            [2475, 1125],
            [1752, 680],
            [940, 680],
            [475, 1125]
        ]
    elif month == 'May':
        corners = [
            [2500, 1000],
            [1752, 680],
            [940, 680],
            [500, 1000]
        ]
    elif month == 'June':
        corners = [
            [2550, 1750],
            [2550, 1250],
            [350, 1250],
            [0,1750]
        ]
    elif month == 'July':
        corners = [
            [2375, 975],
            [1925, 750],
            [875, 750],
            [525, 975]
        ]
    else:
        # default
        corners = [
            [2559, 1919],
            [1752, 680],
            [940, 680],
            [200, 1919]
        ]
    
    return corners


def filter_explore(video_file):

    month = MONTHS[int(video_file.split('-')[1]) - 1]
    # camera = "cam-config-UWRL.json"
    name = video_file.split(".")[0]
    video_file = f"{month}/videos/{video_file}"
    vector_file = f"{month}/results/{name}_velocimetry_results.nc"

    ds = xr.open_dataset(vector_file)

    # ds.velocimetry.mask.corr(inplace=True)
    # ds.velocimetry.mask.minmax(inplace=True)
    # ds.velocimetry.mask.rolling(inplace=True)
    # ds.velocimetry.mask.outliers(inplace=True)
    # ds.velocimetry.mask.variance(inplace=True)
    # ds.velocimetry.mask.angle(angle_tolerance=0.5*np.pi)
    # ds.velocimetry.mask.count(inplace=True)
    # ds.velocimetry.mask.window_mean(wdw=2, inplace=True, tolerance=0.5, reduce_time=True)

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
    # plt.title(f"{name} velocimetry results")
    plt.savefig(f"Mask/photos/{name}_velocimetry_results_no_mask.png", bbox_inches="tight", dpi=600)
    plt.close() # thank you Haley

    ds.close()
