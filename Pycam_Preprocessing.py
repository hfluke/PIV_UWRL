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

MINMAX = [
    {'min': 0, 'max': 255},
    {'min': 31, 'max': 255},
    {'min': 0, 'max': 223},
    {'min': 31, 'max': 223}
]

NORMALIZE = [7, 15, 31]

SMOOTH = [1, 2, 3]

TIME_DIFF = [
    {'thres': 0, 'abs': False},
    {'thres': 2, 'abs': False},
    {'thres': 4, 'abs': False},
    {'thres': 0, 'abs': True},
    {'thres': 2, 'abs': True},
    {'thres': 4, 'abs': True}
]

EDGE_DETECT = [
    {'wdw_1': 1, 'wdw_2': 2},
    {'wdw_1': 2, 'wdw_2': 4},
    {'wdw_1': 4, 'wdw_2': 8}
]


def PyCam_Implementation(video_name):

    month = MONTHS[int(video_name.split('-')[1]) - 1]
    camera = "cam-config-UWRL.json"
    name = video_name.split("#")[0]
    vector_file = f"Preprocessing/results/{video_name}.nc"
    id_str = video_name.split('#', maxsplit=1)[1].strip()
    video_file = f"{month}/videos/{name}.mp4"

    id = dict()
    for i in id_str.split('#'):
        tag = i.split('=')
        id[str(tag[0])] = int(tag[1])

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

    da = da.frames.minmax(min=id['min'], max=id['max'])
    # da = da.frames.normalize(samples=id['normalize'])
    # da = da.frames.smooth(wdw=id['smooth'])
    # da = da.frames.time_diff(thres=id['thres'], abs=bool(id['abs']))
    # da = da.frames.edge_detect(wdw_1=id['wdw1'], wdw_2=id['wdw2'])
    
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
    # plt.savefig(f"Preprocessing/results/{video_name}.png", bbox_inches="tight", dpi=600)
    plt.savefig(f"CLAHE/results/{name}.png", bbox_inches="tight", dpi=600)
    plt.close() # thank you Haley

    ds.close()


def write_todo(video_file):

    name = video_file.split(".")[0]

    nums = [0, 1, 2, 3, 4, 6, 8]

    for s in nums:
        for t in nums:

            id = f"#smooth={s}#thres={t}#abs=0"

            with open('prep.txt', 'a') as f:
                f.write(f'{name}{id}\n')
    
    # for minmax in MINMAX:
    #     for normalize in NORMALIZE:
    #         for smooth in SMOOTH:
    #             for time_diff in TIME_DIFF:
    #                 for edge_detect in EDGE_DETECT:

    #                     id = f"#min={minmax['min']}#max={minmax['max']}#normalize={normalize}#smooth={smooth}#thres={time_diff['thres']}#abs={0 if time_diff['abs'] == False else 1}#wdw1={edge_detect['wdw_1']}#wdw2={edge_detect['wdw_2']}"

    #                     with open('prep.txt', 'a') as f:
    #                         f.write(f'{name}{id}\n')
